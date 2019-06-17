module Agent

export defaultparams, defaulttestparams ,newqtable, action, learn!

const initq = 10000.0  # Q-value の初期値
const actions = [-10., 10.]  # 行動の候補

# 状態分割の下限と上限
const xlimits = [-1.5, 1.5]
const thetalimits = [-pi, pi]
const xdotlimits = [-1.5, 1.5]
const thetadotlimits = [-10.0, 10.0]

# 状態の分割数
const xnum = 10
const thetanum = 120
const xdotnum = 10
const thetadotnum = 50

# 状態分割の bins を生成
const xbins = range(xlimits..., length = xnum-1)
const thetabins = range(thetalimits..., length = thetanum-1)
const xdotbins = range(xdotlimits..., length = xdotnum-1)
const thetadotbins = range(thetadotlimits..., length = thetadotnum-1)

# 学習に使うパラメータ
struct Params
    α::Float64  # 学習率
    γ::Float64  # 割引率
end

const defaultparams = Params(0.01, 0.999)
const defaulttestparams = Params(0.0, 0.999)

function newqtable()
    qtable = zeros(xnum, thetanum, xdotnum, thetadotnum, length(actions))
    fill!(qtable, initq)
    qtable
end

function action(temp, qtable, s)
    qs = qtable[digitizeall(s)..., :]
    boltzmann = [exp(q/temp/initq) for q in qs]
    probability = boltzmann / sum(boltzmann)
    bin = zeros(length(probability)-1)
    # なんかいい感じの左畳み込みないかなあ
    for (i, prob) = enumerate(probability)
        if i == 1
            bin[i] = probability[1]
            continue
        elseif i == length(probability)
            break
        end
        bin[i] = bin[i-1] + probability[i]
    end
    maxidx = searchsortedfirst(bin, rand())
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