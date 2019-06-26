module Experiment

include("agent.jl")
include("cartpoleenv.jl")

const episodesnum = 20000000
const stepsnum = Env.fps * 10

struct History
    states::Vector{Env.State}
    actions::Vector{Float64}
    rewards::Vector{Float64}
end

function newhistory()
    states = Vector{Env.State}(undef, stepsnum)
    actions = Vector{Float64}(undef, stepsnum)
    rewards = Vector{Float64}(undef, stepsnum)
    History(states, actions, rewards)
end

function run()
    returns = Vector{Float64}(undef, episodesnum)
    qtable = Agent.newqtable()
    agentparams = Agent.defaultparams

    for episode = 1:episodesnum
        hist = oneepisode(agentparams, qtable)
        returns[episode] = sum(hist.rewards)
    end

    returns, qtable
end

function test(qtable)
    hist = oneepisode(Agent.defaulttestparams, qtable)
    hist, qtable
end

function oneepisode(agentparams, qtable)
    hist = newhistory()

    s = Env.newstate()
    a = 0.0
    r = 0.0

    for step = 1:stepsnum
        hist.states[step] = s
        hist.actions[step] = a
        hist.rewards[step] = r

        a = Agent.action(agentparams, qtable, s)
        snext = Env.onestep(s, anext)
        r = Env.reward(snext, a)
        Agent.learn!(agentparams, qtable, s, a, r, snext)

        s = snext
    end

    hist
end

end