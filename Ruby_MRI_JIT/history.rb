class History
  attr_reader :actions, :rewards, :states, :info

  def initialize
    @actions = []
    @rewards = []
    @states = []
    @info = []
  end

  def push(a, r, s, info)
    @actions.push(a)
    @rewards.push(r)
    @states.push(s)
    @info.push(info)
  end

  def save(path)
    open(path, "w") do |f|
      (0...@actions.length).each do |i|
        f.puts(sprintf("%d\t%.15f\t%d\t%s", @actions[i], @rewards[i], @states[i], @info[i]))
      end
    end
  end
end