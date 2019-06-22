module NGnet

using LinearAlgebra

struct RBF
    μ::Vector{Float64}
    invΣ::Array{Float64, 2}
end

function avalue(rbf, x)
    exp((x - rbf.μ)' * rbf.invΣ * (x - rbf.μ) / -2)
end

const RBFs = Vector{RBF}

function newrbfs(bins...)
    # Note: あまり効率的ではなさそうだがどうせ1回しか実行されないので
    # これでよいということにする
    rbfs = []
    for μ in newμs(bins)
        push!(rbfs, RBF(μ, newinvΣ(bins)))
    end
    rbfs
end

function newμs(bins)
    mus = []
    for elems in Iterators.product(bins...)
        push!(mus, collect(elems))
    end
    mus
end

function newinvΣ(bins)
    # NOTE: これは bins が等間隔で並んでいることを前提としているなあ
    subs = [bin[2] - bin[1] for bin in bins]
    Σ = LinearAlgebra.Diagonal(subs)
    inv(Σ)
end

function bvalue(rbfs, x)
    a = [avalue(rbf, x) for rbf in rbfs]
    a / sum(a)
end

function value(rbfs, x, weight)
    sum(weight .* bvalue(rbfs, x))
end

function value(weight, bval)
    sum(weight .* bval)
end

end