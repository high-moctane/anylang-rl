class Agent
  def initialize
    @alpha = 0.1  # 学習率
    @gamma = 0.999  # 割引率
    @epsilon = 0.1  # ランダムに行動選択する割合

    @init_qvalue = 10000.0  # q-value の初期値
    @actions = [-10.0, 10.0]  # 行動の候補

    # 状態分割の下限と上限
    @x_limits = [-2.0, 2.0]
    @theta_limits = [-Math::PI, Math::PI]
    @xdot_limits = [-2.0, 2.0]
    @thetadot_limits = [-10.0, 10.0]

    # 状態の分割数
    @x_num = 4
    @theta_num = 90
    @xdot_num = 10
    @thetadot_num = 50

    # 状態分割の bins を生成
    @x_bins = make_bins(@x_limits, @x_num)
    @theta_bins = make_bins(@theta_limits, @theta_num)
    @xdot_bins = make_bins(@xdot_limits, @xdot_num)
    @thetadot_bins = make_bins(@thetadot_limits, @thetadot_num)

    @qtable = make_qtable
  end

  # eps-greedy
  def action(s)
    if Random.rand < @epsilon
      return @actions.sample
    end

    s_idx = s_index(s)
    max_idx = argmax(@qtable[s_idx])
    @actions[max_idx]
  end

  def learn(s, a, r, snext)
    s_idx = s_index(s)
    a_idx = @actions.index(a)
    snext_idx = s_index(snext)

    @qtable[s_idx][a_idx] = \
      (1.0 - @alpha) * @qtable[s_idx][a_idx] + \
      @alpha * (r + @gamma * @qtable[snext_idx].max)
  end

  def set_test_params
    @alpha = 0.0
    @epsilon = 0.0
  end

  def make_bins(limits, num)
    width = (limits[1] - limits[0]) / (num - 2)
    (0..(num-2)).map { |i| limits[0] + width * i }
  end

  def make_qtable
    s_size = @x_num * @theta_num * @xdot_num * @thetadot_num
    Array.new(s_size) {
      Array.new(@actions.size, @init_qvalue)
    }
  end

  def digitize(bins, x)
    bins.each_with_index do |v, i|
      if x < v
        return i
      end
    end
    bins.size
  end

  def digitize_all(s)
    x_idx = digitize(@x_bins, s[0])
    theta_idx = digitize(@theta_bins, s[1])
    xdot_idx = digitize(@xdot_bins, s[2])
    thetadot_idx = digitize(@thetadot_bins, s[3])
    [x_idx, theta_idx, xdot_idx, thetadot_idx]
  end

  def s_index(s)
    indices = digitize_all(s)
    indices[0] + @x_num * (indices[1] + @theta_num * (indices[2] + @xdot_num * indices[3]))
  end

  def argmax(arr)
    idx = 0
    max_val = arr[0]
    arr.each_with_index do |v, i|
      if v > max_val
        idx = i
      end
    end
    idx
  end
end