package main

type History struct {
	states  [][]float64
	actions []float64
	rewards []float64
}

func NewHistory(stepsNum int) *History {
	return &History{
		states:  make([][]float64, stepsNum),
		actions: make([]float64, stepsNum),
		rewards: make([]float64, stepsNum),
	}
}

type Experiment struct {
	agent                 *Agent
	env                   *Env
	episodesNum, stepsNum int
}

func NewExperiment() *Experiment {
	agent := NewAgent()
	env := NewEnv()
	return &Experiment{
		agent:       agent,
		env:         env,
		episodesNum: 20000000,
		stepsNum:    env.fps * 10,
	}
}

// Run は実験して returns を返す
func (e *Experiment) Run() []float64 {
	returns := make([]float64, e.episodesNum)

	for episode := 0; episode < e.episodesNum; episode++ {
		e.env.ResetEnv()
		hist := e.oneEpisode()
		for _, r := range hist.rewards {
			returns[episode] += r
		}
	}

	return returns
}

func (e *Experiment) Test() *History {
	e.env.ResetEnv()
	e.agent.SetTestParams()
	return e.oneEpisode()
}

func (e *Experiment) oneEpisode() *History {
	hist := NewHistory(e.stepsNum)

	s := e.env.State()
	a := 0.0
	r := 0.0

	for step := 0; step < e.stepsNum; step++ {
		hist.states[step] = s
		hist.actions[step] = a
		hist.rewards[step] = r

		a = e.agent.Action(s)
		e.env.Step(a)
		sNext := e.env.State()
		r = e.env.Reward()
		e.agent.Learn(s, a, r, sNext)

		s = sNext
	}

	return hist
}
