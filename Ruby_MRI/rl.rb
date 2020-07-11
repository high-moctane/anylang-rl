require_relative "environment/cartpole"
require_relative "environment/maze"
require_relative "history"
require_relative "agent/q_learning"
require_relative "agent/sarsa"
require_relative "q_table"


class RL
  def initialize(config)
    @returns_path = config.config["RL_RETURNS_PATH"]
    @test_history_path = config.config["RL_TEST_HISTORY_PATH"]

    @max_episode = config.config["RL_MAX_EPISODE"].to_i
    @max_step = config.config["RL_MAX_STEP"].to_i

    @agent = choose_agent(config)
    @env = choose_env(config)

    init_qvalue = config.config["QTABLE_INITIAL_QVALUE"].to_f
    @q_table = QTable.new(@env.state_size, @env.action_size, init_qvalue)

    @returns = []
    @test_history = History.new
  end

  def choose_agent(config)
    agent_name = config.config["AGENT_NAME"]
    case agent_name
    when "Q-learning" then
      QLearning.new(config)
    when "Sarsa" then
      Sarsa.new(config)
    else
      raise "invalid agent name: #{agent_name}"
    end
  end

  def choose_env(config)
    env_name =config.config["ENV_NAME"]
    case env_name
    when "Cartpole" then
      Cartpole.new(config)
    when "Maze" then
      Maze.new(config)
    else
      raise "invalid env name: #{env_name}"
    end
  end

  def run
    (0...@max_episode).each do |_|
      history = run_episode
      @returns.push(history.rewards.sum)
    end
  end

  def run_episode
    history = History.new

    @env.reset

    s1 = s2 = @env.state
    r = @env.reward
    info = @env.info
    a1 = a2 = @agent.action(@q_table, s1)

    history.push(a1, r, s2, info)

    (0...@max_step).each do |_|
      @env.run_step(a1)
      s2 = @env.state
      r = @env.reward
      info = @env.info
      a2 = @agent.action(@q_table, s2)

      history.push(a1, r, s2, info)

      if @env.is_finish
        @q_table.table[s2].fill(0.0)
      end

      @agent.learn(@q_table, s1, a1, r, s2, a2)

      if @env.is_finish
        break
      end

      s1 = s2
      a1 = a2
    end

    history
  end

  def run_test
    @agent.fix
    @test_history = run_episode
  end

  def save_returns
    open(@returns_path, "w") do |f|
      @returns.each do |ret|
        f.puts(sprintf("%.15f", ret))
      end
    end
  end

  def save_test_history
    @test_history.save(@test_history_path)
  end
end
