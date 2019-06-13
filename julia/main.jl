include("experiment.jl")

qtable, hist = Experiment.run()

open("returns.csv", "w") do io
    for returns in hist.returns
        println(io, returns)
    end
end

open("states.csv", "w") do io
    for s in hist.states
        println(io, join(s, ","))
    end
end