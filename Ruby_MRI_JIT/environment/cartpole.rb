class Cartpole
  def initialize(config)
    @actions = [
      config.config["ENV_ACTION_LEFT"].to_f,
      config.config["ENV_ACTION_RIGHT"].to_f
    ]

    @x_bounds = [
      config.config["ENV_X_LEFT"].to_f,
      config.config["ENV_X_RIGHT"].to_f
    ]
    @theta_bounds = [
      config.config["ENV_THETA_LEFT"].to_f,
      config.config["ENV_THETA_RIGHT"].to_f
    ]
    @xdot_bounds = [
      config.config["ENV_XDOT_LEFT"].to_f,
      config.config["ENV_XDOT_RIGHT"].to_f
    ]
    @thetadot_bounds = [
      config.config["ENV_THETADOT_LEFT"].to_f,
      config.config["ENV_THETADOT_RIGHT"].to_f
    ]

    @x_size = config.config["ENV_X_SIZE"].to_i
    @theta_size = config.config["ENV_THETA_SIZE"].to_i
    @xdot_size = config.config["ENV_XDOT_SIZE"].to_i
    @thetadot_size = config.config["ENV_THETADOT_SIZE"].to_i

    @g = config.config["ENV_GRAVITY"].to_f
    cartmass = config.config["ENV_CART_MASS"].to_f
    @m = config.config["ENV_POLE_MASS"].to_f
    @l = config.config["ENV_POLE_LENGTH"].to_f
    @ml = @m * @l
    @mass = cartmass + @m

    fps = config.config["ENV_FRAME_PER_SECOND"].to_i
    @tau = 1.0 / fps

    @init_state = [0.0, Math::PI, 0.0, 0.0].freeze
    @s = @init_state.clone
  end

  def solve_runge_kutta(s, u, dt)
    k1 = differential(s, u)
    s1 = solve_euler(s, k1, dt / 2.0)
    k2 = differential(s1, u)
    s2 = solve_euler(s, k2, dt / 2.0)
    k3 = differential(s2, u)
    s3 = solve_euler(s, k3, dt)
    k4 = differential(s3, u)

    snext = s.map.with_index { |val, i|
      val + (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) * dt / 6.0
    }

    snext[1] = normalize_theta(snext[1])

    snext
  end

  def differential(s, u)
    _, theta, xdot, thetadot = s

    sintheta = Math.sin(theta)
    costheta = Math.cos(theta)

    xddot = (4.0 * u / 3.0 + 4.0 * @ml * thetadot**2 * sintheta / 3.0 \
      - @m * @g * Math.sin(2.0 * theta) / 2.0) \
      / (4.0 * @mass - @m * costheta**2)
    thetaddot = (@mass * @g * sintheta - @ml * thetadot**2 * sintheta * costheta - u * costheta) \
      / (4.0 * @mass * @l / 3.0 - @ml * costheta**2)

    [xdot, thetadot, xddot, thetaddot]
  end

  def solve_euler(s, sdot, dt)
    (0...s.length).map { |i| s[i] + sdot[i] * dt }
  end

  def state_size
    @x_size * @theta_size * @xdot_size * @thetadot_size
  end

  def action_size
    @actions.length
  end

  def state
    x_idx = digitize(@x_bounds, @x_size, @s[0])
    theta_idx = digitize(@theta_bounds, @theta_size, @s[1])
    xdot_idx = digitize(@xdot_bounds, @xdot_size, @s[2])
    thetadot_idx = digitize(@thetadot_bounds, @thetadot_size, @s[3])

    ((x_idx * @theta_size + theta_idx) * @xdot_size + xdot_idx) * @thetadot_size + thetadot_idx
  end

  def info
    x, theta, xdot, thetadot = @s
    sprintf("%.15f,%.15f,%.15f,%.15f", x, theta, xdot, thetadot)
  end

  def reward
    x, theta, _, _ = @s
    if x.abs > 2.0
      -2.0
    else
      -theta.abs + Math::PI / 2.0 - 0.01 * x.abs
    end
  end

  def reset
    @s = @init_state.clone
  end

  def run_step(a)
    u = @actions[a]
    @s = solve_runge_kutta(@s, u, @tau)
  end

  def is_finish
    false
  end

  def digitize(bounds, num, val)
    if val < bounds[0]
      0
    elsif val >= bounds[1]
      num - 1
    else
      width = (bounds[1] - bounds[0]) / (num - 2)
      ((val - bounds[0]) / width).to_i + 1
    end
  end

  def normalize_theta(theta)
    (theta + 3*Math::PI) % (2 * Math::PI) - Math::PI
  end
end