class Sarsa
  def initialize(config)
    @alpha = config.config["AGENT_ALPHA"].to_f
    @gamma = config.config["AGENT_GAMMA"].to_f
    @eps = config.config["AGENT_EPSILON"].to_f
  end

  def action(q_table, s)
    if rand < @eps
      return rand(0...q_table.action_size)
    end
    argmax(q_table.table[s])
  end

  def learn(q_table, s1, a1, r, s2, a2)
    q_table.table[s1][a1] = \
      (1.0 - @alpha) * q_table.table[s1][a1] + @alpha * (r + @gamma * q_table.table[s2][a2])
  end

  def fix
    @alpha = 0.0
    @eps = 0.0
  end

  def argmax(arr)
    res = 0
    (1...arr.length).each do |i|
      if arr[res] < arr[i]
        res = i
      end
    end
    res
  end
end
