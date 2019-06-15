module Experiment

include("cartpoleenv.jl")
include("agent.jl")

const episodesnum = 100000
const stepsnum = Env.fps * 10

struct History
    returns::Vector{Float64}
    states::Vector{Env.State}
end

function newhistory()
    returns = Vector{Float64}(undef, episodesnum)
    states = Vector{Env.State}(undef, stepsnum)
    History(returns, states)
end

function run()
    qtable = Agent.newqtable()
    hist = newhistory()

    for episode = 1:episodesnum
        returns = oneepisode(qtable, hist)
        hist.returns[episode] = returns
    end
    test(qtable, hist)

    qtable, hist
end

function test(qtable, hist)
    oneepisode(qtable, hist, savestates = true)
end

function oneepisode(qtable, hist; savestates = false)
    returns = 0.0

    s = Env.newstate()
    a = 0.0

    for step = 1:stepsnum
        if savestates
            hist.states[step] = s
        end

        anext = Agent.action(qtable, s)
        snext = Env.step(s, anext)
        r = Env.reward(s)
        returns += r
        if step > 1
            Agent.learn!(qtable, s, a, r, snext, anext)
        end
        s = snext
        a = anext
    end

    returns
end

end