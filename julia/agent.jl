module Agent

export QTable, newqtable, action, learn!

const α = 0.1  # 学習率
const γ = 0.99  # 割引率
const ϵ = 0.1  #ランダムに探索する割合
const initq = 10  # Q-value の初期値
const actions = [-100., .0, 100.]  # 行動の候補

# 状態分割の下限と上限
const xlimits = [-1.0, 1.0]
const thetalimits = [-pi, pi]
const xdotlimits = [-2.0, 2.0]
const thetadotlimits = [-10.0, 10.0]

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

# Q-table
const QTable = Array{Float64,5}

function newqtable()
    qtable = zeros(xnum, thetanum, xdotnum, thetadotnum, length(actions))
    fill!(qtable, initq)
    qtable
end

function action(qtable, s)
    if rand() < ϵ
        return rand(actions)
    end
    ids = digitizeall(s)
    maxidx = argmax(qtable[ids..., :])
    return actions[maxidx]
end

function learn!(qtable, s0, a0, r, s1, a1)
    s0idx = digitizeall(s0)
    a0idx = findfirst(x->x==a0, actions)
    s1idx = digitizeall(s1)
    # a1idx = findfirst(x->x==a1, actions)

    qtable[s0idx..., a0idx] =
        (1 - α) * qtable[s0idx..., a0idx] +
        α * (r + γ* maximum(qtable[s1idx..., :]))
end

function digitizeall(s)
    xidx = searchsortedfirst(xbins, s[1])
    thetaidx = searchsortedfirst(thetabins, s[2])
    xdotidx = searchsortedfirst(xdotbins, s[3])
    thetadotidx = searchsortedfirst(thetadotbins, s[4])
    xidx, thetaidx, xdotidx, thetadotidx
end


end