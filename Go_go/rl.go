package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type RL struct {
	returnsPath, testHistoryPath string

	maxEpisode, maxStep int

	agent  Agent
	env    Environment
	qTable *QTable

	returns     []float64
	testHistory *History
}

func NewRL(config *Config) (*RL, error) {
	returnsPath, err := config.Get("RL_RETURNS_PATH")
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}
	testHistoryPath, err := config.Get("RL_TEST_HISTORY_PATH")
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}

	maxEpisodeStr, err := config.Get("RL_MAX_EPISODE")
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}
	maxEpisode, err := strconv.Atoi(maxEpisodeStr)
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}

	maxStepStr, err := config.Get("RL_MAX_STEP")
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}
	maxStep, err := strconv.Atoi(maxStepStr)
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}

	agent, err := chooseAgent(config)
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}
	env, err := chooseEnvironment(config)
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}

	initQValueStr, err := config.Get("QTABLE_INITIAL_QVALUE")
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}
	initQValue, err := strconv.ParseFloat(initQValueStr, 64)
	if err != nil {
		return nil, fmt.Errorf("new rl error: %w", err)
	}

	qTable := NewQTable(env.StateSize(), env.ActionSize(), initQValue)

	returns := []float64{}
	testHistory := NewHistory()

	return &RL{
		returnsPath,
		testHistoryPath,
		maxEpisode,
		maxStep,
		agent,
		env,
		qTable,
		returns,
		testHistory,
	}, nil
}

func chooseAgent(config *Config) (Agent, error) {
	agentName, err := config.Get("AGENT_NAME")
	if err != nil {
		return nil, fmt.Errorf("choose agent error: %w", err)
	}

	var agent Agent
	switch agentName {
	case "Sarsa":
		agent, err = NewSarsa(config)
	case "Q-learning":
		agent, err = NewQLearning(config)
	}
	if err != nil {
		return nil, fmt.Errorf("choose agent error: %w", err)
	}

	return agent, nil
}

func chooseEnvironment(config *Config) (Environment, error) {
	envName, err := config.Get("ENV_NAME")
	if err != nil {
		return nil, fmt.Errorf("choose environment error: %w", err)
	}

	var env Environment
	switch envName {
	case "Cartpole":
		env, err = NewCartpole(config)
	case "Maze":
		env, err = NewMaze(config)
	}
	if err != nil {
		return nil, fmt.Errorf("choose environment error: %w", err)
	}

	return env, nil
}

func (rl *RL) Run() {
	for episode := 0; episode < rl.maxEpisode; episode++ {
		history := rl.RunEpisode()

		returns := 0.0
		for _, reward := range history.Rewards {
			returns += reward
		}
		rl.returns = append(rl.returns, returns)
	}
}

func (rl *RL) RunEpisode() *History {
	history := NewHistory()

	rl.env.Reset()

	s1 := rl.env.State()
	s2 := s1
	r := rl.env.Reward()
	info := rl.env.Info()
	a1 := rl.agent.Action(rl.qTable, s1)
	var a2 Action

	history.Append(a1, r, s2, info)

	for step := 0; step < rl.maxStep; step++ {
		rl.env.RunStep(a1)
		s2 = rl.env.State()
		r = rl.env.Reward()
		info = rl.env.Info()
		a2 = rl.agent.Action(rl.qTable, s2)

		history.Append(a1, r, s2, info)

		if rl.env.IsFinish() {
			for i := 0; i < rl.qTable.ActionSize; i++ {
				rl.qTable.Table[s2][i] = 0.
			}
		}
		rl.agent.Learn(rl.qTable, s1, a1, r, s2, a2)

		if rl.env.IsFinish() {
			break
		}

		s1 = s2
		a1 = a2
	}

	return history
}

func (rl *RL) RunTest() {
	rl.agent.Fix()
	rl.testHistory = rl.RunEpisode()
}

func (rl *RL) SaveReturns() error {
	f, err := os.Create(rl.returnsPath)
	if err != nil {
		return fmt.Errorf("save returns error: %w", err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for _, ret := range rl.returns {
		w.WriteString(fmt.Sprintf("%.15f\n", ret))
	}

	return nil
}

func (rl *RL) SaveTestHistory() error {
	return rl.testHistory.Save(rl.testHistoryPath)
}
