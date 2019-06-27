require_relative "experiment"

exp = Experiment.new()
returns = exp.run
history = exp.test

File.open("returns.csv", "w") do |f|
  returns.each do |r|
    f.puts(r)
  end
end

File.open("states.csv", "w") do |f|
  history.states.each do |s|
    f.puts(s.join(","))
  end
end

File.open("actions.csv", "w") do |f|
  history.actions.each do |a|
    f.puts(a)
  end
end

File.open("rewards.csv", "w") do |f|
  history.rewards.each do |r|
    f.puts(r)
  end
end