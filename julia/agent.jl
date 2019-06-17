module Agent

export defaultparams, defaulttestparams ,newqtable, action, learn!

const initq = 1000.0  # Q-value の初期値
const actions = [-10., .0, 10.]  # 行動の候補

# 状態分割の下限と上限
const xlimits = [-2.0, 2.0]
const thetalimits = [-pi, pi]
const xdotlimits = [-2.0, 2.0]
const thetadotlimits = [-12.0, 12.0]

# 状態の分割数
const xnum = 10
const thetanum = 36
const xdotnum = 10
const thetadotnum = 10

# 状態分割の bins を生成
const xbins = range(xlimits..., length = xnum-1)
const thetabins = range(thetalimits..., length = thetanum-1)
const xdotbins = range(xdotlimits..., length = xdotnum-1)
const thetadotbins = range(thetadotlimits..., length = thetadotnum-1)

# 学習に使うパラメータ
struct Params
    α::Float64  # 学習率
    γ::Float64  # 割引率
    ϵ ::Float64  #ランダムに探索する割合
end

const defaultparams = Params(0.1, 0.99, 0.1)
const defaulttestparams = Params(0.0, 0.99, 0.0)

function newqtable()
    qtable = zeros(xnum, thetanum, xdotnum, thetadotnum, length(actions))
    fill!(qtable, initq)
    qtable
end

function action(params, qtable, s)
    if rand() < params.ϵ
        return rand(actions)
    end
    ids = digitizeall(s)
    maxidx = argmax(qtable[ids..., :])
    return actions[maxidx]
end

function learn!(params ,qtable, s0, a0, r, s1, a1)
    s0idx = digitizeall(s0)
    a0idx = findfirst(x->x==a0, actions)
    s1idx = digitizeall(s1)
    # a1idx = findfirst(x->x==a1, actions)

    qtable[s0idx..., a0idx] =
        (1 - params.α) * qtable[s0idx..., a0idx] +
        params.α * (r + params.γ* maximum(qtable[s1idx..., :]))
end

function digitizeall(s)
    xidx = searchsortedfirst(xbins, s[1])
    thetaidx = searchsortedfirst(thetabins, s[2])
    xdotidx = searchsortedfirst(xdotbins, s[3])
    thetadotidx = searchsortedfirst(thetadotbins, s[4])
    xidx, thetaidx, xdotidx, thetadotidx
end


end