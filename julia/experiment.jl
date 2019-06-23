module Experiment

include("agent.jl")
include("cartpoleenv.jl")

const episodesnum = 10000
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
    agent = AgentNGnet.newagent()

    for episode = 1:episodesnum
        hist = oneepisode(agent)
        returns[episode] = sum(hist.rewards)
    end

    returns, agent
end

function test(agent)
    testagent = AgentNGnet.newtestagent(agent)
    hist = oneepisode(testagent)
    hist, testagent
end

function oneepisode(agent)
    hist = newhistory()

    s = Env.newstate()
    a = 0.0
    r = 0.0
    snext = Env.newstate()
    anext = 0.0

    for step = 1:stepsnum
        hist.states[step] = s
        hist.actions[step] = a
        hist.rewards[step] = r

        anext = AgentNGnet.action(agent, s)
        snext = Env.onestep(s, anext)
        r = Env.reward(snext, a)
        AgentNGnet.learn!(agent, s, anext, r, snext)

        s = snext
        a = anext
    end

    hist
end

end