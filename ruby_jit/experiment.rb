require_relative "agent"
require_relative "env"


class History
  attr_accessor :states, :actions, :rewards

  def initialize(steps_num)
    @states = Array.new(steps_num)
    @actions = Array.new(steps_num)
    @rewards = Array.new(steps_num)
  end
end


class Experiment
  def initialize
    @agent = Agent.new()
    @env = Env.new()

    @episodes_num = 10000000
    @steps_num = @env.fps * 10
  end

  def run
    returns = Array.new(@episodes_num)

    (0...@episodes_num).each do |episode|
      hist = one_episode
      returns[episode] = hist.rewards.sum
    end

    returns
  end

  def test
    @agent.set_test_params
    one_episode
  end

  def one_episode
    hist = History.new(@steps_num)

    @env.reset_state
    s = @env.state
    a = 0.0
    r = 0.0

    (0...@steps_num).each do |step|
      hist.states[step] = s
      hist.actions[step] = a
      hist.rewards[step] = r

      a = @agent.action(s)
      @env.step(a)
      s_next = @env.state
      r = @env.reward
      @agent.learn(s, a, r, s_next)

      s = s_next
    end

    hist
  end
end