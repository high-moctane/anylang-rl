module Env

export State, newstate, onestep, reward

# この実験における定数
const g = 9.80665   # 重力加速度
const M = 1.0       # カートの質量
const m = 0.1       # ポールの質量
const l = 0.5       # ポールの半分の長さ
const fps = 50      # frames per second
const tau = 1 / fps # 制御周期

const State = Vector{Float64}

# 最初の状態
# [x, theta, xdot, thetadot]
const initstate = [0.0, -pi, 0.0, 0.0]

# あとの計算で使う
const ml = m * l
const mass = M + m


function newstate()
    copy(initstate)
end

function onestep(s, a)
    rungekuttasolve(s, a, tau)
end

function reward(s, a)
    x, θ, xdot, θdot = s
    if abs(x) > 2.0
        return -2.0
    end
    -abs(θ) + pi / 2
end

# 状態 s で力 u を加えたときの微分
function differential(s, u)
    x, θ, xdot, θdot = s
    sinθ = sin(θ)
    cosθ = cos(θ)

    xddot = (4u / 3 + 4ml * θdot^2 * sinθ / 3 - m * g * sin(2θ) / 2) / (4mass - m * cosθ^2)
    θddot = (mass * g * sinθ - ml * θdot^2 * sinθ * cosθ - u * cosθ) /
        (4mass * l / 3 - ml * cosθ^2)

    [xdot, θdot, xddot, θddot]
end

# オイラー法を用いて微分方程式を解く
function eulersolve(s, sdot, dt)
    s + sdot * dt
end

# ルンゲクッタ法を用いて微分方程式を解く
function rungekuttasolve(s, u, dt)
    k1 = differential(s, u)
    s1 = eulersolve(s, k1, dt / 2)
    k2 = differential(s1, u)
    s2 = eulersolve(s, k2, dt / 2)
    k3 = differential(s2, u)
    s3 = eulersolve(s, k3, dt)
    k4 = differential(s3, u)

    snext = s + (k1 + 2k2 + 2k3 + k4) * dt / 6
    snext[2] = normalizetheta(snext[2])
    snext
end

function normalizetheta(theta)
    if theta >= pi
        return theta - 2pi
    elseif theta < -pi
        return theta + 2pi
    end
    theta
end

end