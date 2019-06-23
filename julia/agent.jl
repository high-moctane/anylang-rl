module AgentNGnet

include("ngnet.jl")

const μrange = [-10.0, 10.0]
const σrange = [0.01, 3.0]

# NGnet の bins を生成
const xbins = range(-3.0, 3.0, length = 5)
const thetabins = range(-pi, pi, length = 7)
const xdotbins = range(-3.0, 3.0, length = 5)
const thetadotbins = range(-10.0, 10.0, length = 7)

const ngnet = NGnet.newrbfs(xbins, thetabins, xdotbins, thetadotbins)

mutable struct Agent
    α::Float64  # 学習率
    γ::Float64  # 割引率
    η_μ::Float64  # \mu の更新率
    η_σ::Float64  # \sigma の更新率
    ngnet::NGnet.RBFs
    vweight::Vector{Float64}
    μweight::Vector{Float64}
    σweight::Vector{Float64}
end

function newagent()
    α = 0.01
    γ = 0.99
    η_μ = 0.01
    η_σ = 0.01
    ngnet = NGnet.newrbfs(xbins, thetabins, xdotbins, thetadotbins)
    vweight = zeros(length(ngnet))
    μweight = zeros(length(ngnet))
    σweight = ones(length(ngnet)) * σrange[2]
    Agent(α,
        γ,
        η_μ,
        η_σ,
        ngnet,
        vweight,
        μweight,
        σweight)
end

function newtestagent(agent)
    Agent(0.0,
        0.99,
        0.0,
        0.0,
        agent.ngnet,
        agent.vweight,
        agent.μweight,
        agent.σweight)
end

function action(agent, s)
    μ = NGnet.value(agent.ngnet, s, agent.μweight)
    μ = max(μrange[1], min(μrange[2], μ))
    σ = NGnet.value(agent.ngnet, s, agent.σweight)
    σ = max(σrange[1], min(σrange[2], σ))

    a = μ + randn() * σ
    max(μrange[1], min(μrange[2], a))
end

function learn!(agent, s0, a0, r, s1)
    s0bval = NGnet.bvalue(agent.ngnet, s0)
    s1bval = NGnet.bvalue(agent.ngnet, s1)

    td = r + agent.γ * NGnet.value(agent.vweight, s1bval) - NGnet.value(agent.vweight, s0bval)

    # critic
    agent.vweight += agent.α * td * s0bval

    # actor
    μ = NGnet.value(agent.μweight, s0bval)
    σ = NGnet.value(agent.σweight, s0bval)

    if td > 0.0
        agent.μweight += agent.η_μ * (a0 - μ) * s0bval
        if σ > σrange[1]
            agent.σweight -= agent.η_σ * NGnet.value(agent.σweight, s0bval) * s0bval
        end
    elseif td == 0.0
        # NOP
    else
        # if σ < σrange[2]
        #     agent.σweight += agent.η_σ * NGnet.value(agent.σweight, s0bval) * s0bval
        # end
    end
end

end