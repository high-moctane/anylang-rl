module Agent

const initqvalue = 10000.0  # Q-value の初期値
const actions = [-10.0, 10.0]  # 行動の候補

# 状態分割の下限と上限
const xlimits = [-2.0, 2.0]
const thetalimits = [-pi, pi]
const xdotlimits = [-2.0, 2.0]
const thetadotlimits = [-10.0, 10.0]

# 状態の分割数
const xnum = 4
const thetanum = 90
const xdotnum = 10
const thetadotnum = 50

# 状態分割の bins を生成
const xbins = range(xlimits..., length = xnum - 1)
const thetabins = range(thetalimits..., length = thetanum - 1)
const xdotbins = range(xdotlimits..., length = xdotnum - 1)
const thetadotbins = range(thetadotlimits..., length = thetadotnum - 1)

# 学習に使うパラメータ
mutable struct Params
    α::Float64  # 学習率
    γ::Float64  # 割引率
    ε::Float64  # ランダムに探索する割合
end

const defaultparams = Params(0.1, 0.999, 0.1)
const defaulttestparams = Params(0.0, 0.999, 0.0)


function newqtable()
    qtable = zeros(xnum, thetanum, xdotnum, thetadotnum, length(actions))
    fill!(qtable, initqvalue)
    qtable
end

function action(params, qtable, s)
    if rand() < params.ε
        return rand(actions)
    end
    idx = digitizeall(s)
    maxidx = argmax(qtable[idx..., :])
    actions[maxidx]
end

function learn!(params, qtable, s0, a0, r, s1)
    s0idx = digitizeall(s0)
    a0idx = findfirst(x->x == a0, actions)
    s1idx = digitizeall(s1)

    qtable[s0idx..., a0idx] =
        (1 - params.α) * qtable[s0idx..., a0idx] +
        params.α * (r + params.γ * maximum(qtable[s1idx..., :]))

end

function digitizeall(s)
    xidx = searchsortedfirst(xbins, s[1])
    thetaidx = searchsortedfirst(thetabins, s[2])
    xdotidx = searchsortedfirst(xdotbins, s[3])
    thetadotidx = searchsortedfirst(thetadotbins, s[4])
    xidx, thetaidx, xdotidx, thetadotidx
end

end