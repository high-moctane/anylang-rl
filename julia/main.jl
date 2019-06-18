include("experiment.jl")

returns, qtable = Experiment.run()
testhistory, qtable = Experiment.test(qtable)

open("states.csv", "w") do io
    for s in testhistory.states
        println(io, join(s, ","))
    end
end

open("actions.csv", "w") do io
    for a in testhistory.actions
        println(io, join(a, ","))
    end
end

open("rewards.csv", "w") do io
    for r in testhistory.rewards
        println(io, r)
    end
end

open("returns.csv", "w") do io
    for r in returns
        println(io, r)
    end
end
