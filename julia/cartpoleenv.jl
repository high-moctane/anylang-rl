module Env

export State, fps, newstate, step, reward

# この実験における定数
const g = 9.80665  # 重力加速度
const M = 1.0  # カートの質量
const m = 0.1  # ポールの質量
const l = 0.5  # ポールの半分の長さ
const actionrange = 100  # 行動出力の最大値
const fps = 50  # frames per sec
const τ = 1 / fps

# 最初の状態
# [x, theta, xdot, thetadot]
const initstate = [.0, .0, .0, .0]

# あとの計算で使う
const ml = m * l
const mass = M + m

const State = Vector{Float64}


function newstate()
    copy(initstate)
end

function step(s, u)
    abs(u) <= actionrange || throw("too large input")
    rungekuttasolve(s, u, τ)
end

function reward(s)
    # TODO: あとでいい感じの関数にする
    x, θ, xdot, θdot = s
    if abs(θdot) > 5.0
        return -2.0
    elseif abs(x) > 1.0
        return -2.0
    end

    c = cos(θ)
    if c > 0.85
        return 2.0
    end
    return c
end

# 状態 s のとき力 u を加えたときの dt 時間後の微分
function stateequation(s, u, dt)
    x, θ, xdot, θdot = s
    sinθ = sin(θ)
    cosθ = cos(θ)

    xddot = (4u / 3 + 4ml * (θdot^2)sinθ / 3 - m * g * sin(2θ) / 2) / (4mass - m * (cosθ^2))
    θddot = (mass * g * sinθ - ml * (θdot^2) * sinθ * cosθ - u * cosθ) /
        (4mass * l / 3 - ml * (cosθ^2))

    [xdot, θdot, xddot, θddot]
end

# オイラー法を用いて状態 s で sdot の傾きで dt 時間後の状態を計算する
function eulersolve(s, sdot, dt)
    s + sdot * dt
end

# ルンゲクッタで状態 s で力 u を加えて dt 時間後の状態を計算する
function rungekuttasolve(s, u, dt)
    k1 = stateequation(s, u, dt / 2)
    s1 = eulersolve(s, k1, dt / 2)
    k2 = stateequation(s1, u, dt / 2)
    s2 = eulersolve(s, k2, dt / 2)
    k3 = stateequation(s2, u, dt / 2)
    s3 = eulersolve(s, k3, dt)
    k4 = stateequation(s3, u, dt)

    nextstate = s + (k1 + 2k2 + 2k3 + k4) * dt / 6
    nextstate[2] = normalizetheta(nextstate[2])
    nextstate
end

function normalizetheta(theta)
    if theta >= π
        return theta - 2π
    elseif theta < -π
        return theta + 2π
    end
    theta
end

end