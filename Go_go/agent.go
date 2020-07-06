package main

import (
	"fmt"
	"math/rand"
)

type Agent interface {
	Action(*QTable, State) Action
	Learn(*QTable, State, Action, Reward, State, Action)
	Fix()
}

type QLearning struct {
	alpha, gamma, eps float64
}

func NewQLearning(config *Config) (*QLearning, error) {
	alpha, err := config.GetAsFloat64("AGENT_ALPHA")
	if err != nil {
		return nil, fmt.Errorf("new qlearning error: %w", err)
	}

	gamma, err := config.GetAsFloat64("AGENT_GAMMA")
	if err != nil {
		return nil, fmt.Errorf("new qlearning error: %w", err)
	}

	eps, err := config.GetAsFloat64("AGENT_EPSILON")
	if err != nil {
		return nil, fmt.Errorf("new qlearning error: %w", err)
	}

	return &QLearning{alpha, gamma, eps}, nil
}

func (ql *QLearning) Action(qTable *QTable, s State) Action {
	if rand.Float64() < ql.eps {
		return rand.Intn(qTable.ActionSize)
	}
	return argmax(qTable.Table[s])
}

func (ql *QLearning) Learn(qTable *QTable, s1 State, a1 Action, r Reward, s2 State, a2 Action) {
	val := max(qTable.Table[s2])

	alpha := ql.alpha
	gamma := ql.gamma

	qTable.Table[s1][a1] = (1.-alpha)*qTable.Table[s1][a1] + alpha*(r+gamma*val)
}

func (ql *QLearning) Fix() {
	ql.alpha = 0.
	ql.eps = 0.
}

type Sarsa struct {
	alpha, gamma, eps float64
}

func NewSarsa(config *Config) (*Sarsa, error) {
	alpha, err := config.GetAsFloat64("AGENT_ALPHA")
	if err != nil {
		return nil, fmt.Errorf("new qlearning error: %w", err)
	}

	gamma, err := config.GetAsFloat64("AGENT_GAMMA")
	if err != nil {
		return nil, fmt.Errorf("new qlearning, error: %w", err)
	}

	eps, err := config.GetAsFloat64("AGENT_EPSILON")
	if err != nil {
		return nil, fmt.Errorf("new qlearning error: %w", err)
	}

	return &Sarsa{alpha, gamma, eps}, nil
}

func (sa *Sarsa) Action(qTable *QTable, s State) Action {
	if rand.Float64() < sa.eps {
		return rand.Intn(qTable.ActionSize)
	}
	return argmax(qTable.Table[s])
}

func (sa *Sarsa) Learn(qTable *QTable, s1 State, a1 Action, r Reward, s2 State, a2 Action) {
	alpha := sa.alpha
	gamma := sa.gamma

	qTable.Table[s1][a1] = (1.-alpha)*qTable.Table[s1][a1] + alpha*(r+gamma*qTable.Table[s2][a2])
}

func (sa *Sarsa) Fix() {
	sa.alpha = 0.
	sa.eps = 0.
}

func max(floats []float64) float64 {
	if len(floats) == 0 {
		panic("max error: floats len is 0")
	}
	res := floats[0]
	for i := 1; i < len(floats); i++ {
		if res < floats[i] {
			res = floats[i]
		}
	}
	return res
}

func argmax(floats []float64) int {
	res := 0
	for i := 1; i < len(floats); i++ {
		if floats[res] < floats[i] {
			res = i
		}
	}
	return res
}
