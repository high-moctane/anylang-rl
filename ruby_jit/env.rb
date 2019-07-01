class Env
  attr_reader :fps

  def initialize
    @g = 9.80665  # 重力加速度
    @M = 1.0  # カートの質量
    @m = 0.1  # ポールの質量
    @l = 0.5  # ポールの半分の長さ
    @fps = 50  # frames per second
    @tau = 1.0 / @fps  # 制御周期

    # 後の計算で使う
    @ml = @m * @l
    @mass = @M + @m

    # ここで @s をつくる
    # [x, theta, xdot, thetadot]
    reset_state
  end

  def reset_state
    @s = [0.0, Math::PI, 0.0, 0.0]
  end

  def state
    @s
  end

  def reward
    x, theta, xdot, thetadot = @s
    if x.abs > 2.0
      return -2.0
    end
    -(theta.abs) + Math::PI / 2
  end

  def step(a)
    @s = runge_kutta_solve(@s, a, @tau)
  end

  # 状態 s で力 u を加えたときの微分
  def differential(s, u)
    x, theta, xdot, thetadot = s
    sintheta = Math.sin(theta)
    costheta = Math.cos(theta)

    xddot = (4 * u / 3 + 4 * @ml * thetadot**2 * sintheta / 3 - @m * @g * Math.sin(2*theta) / 2) / \
      (4 * @mass - @m * costheta**2)
    thetaddot = (@mass * @g * sintheta - @ml * thetadot**2 * sintheta * costheta - u * costheta) / \
      (4 * @mass * @l / 3 - @ml * costheta**2)

    [xdot, thetadot, xddot, thetaddot]
  end

  # オイラー法で微分方程式を解く
  def euler_solve(s, sdot, dt)
    ret = Array.new(4)
    (0..3).each do |i|
      ret[i] = s[i] + sdot[i] * dt
    end
    ret
  end

  # ルンゲクッタで微分方程式を解く
  def runge_kutta_solve(s, u, dt)
    k1 = differential(s, u)
    s1 = euler_solve(s, k1, dt / 2)
    k2 = differential(s1, u)
    s2 = euler_solve(s, k2, dt / 2)
    k3 = differential(s2, u)
    s3 = euler_solve(s, k3, dt)
    k4 = differential(s3, u)

    snext = s.dup
    (0..3).each do |i|
      snext[i] += (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt / 6
    end

    snext[1] = (snext[1] + 3*Math::PI) % (2 * Math::PI) - Math::PI
    snext
  end
end