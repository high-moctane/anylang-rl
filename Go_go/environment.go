package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

type Environment interface {
	StateSize() int
	ActionSize() int
	State() State
	Reward() Reward
	Info() string
	RunStep(Action)
	Reset()
	IsFinish() bool
}

type Maze struct {
	maze          [][]rune
	height, width int

	defaultReward, goalReward, wallReward Reward

	initH, initW int
	goalH, goalW int
	h, w         int
}

func NewMaze(config *Config) (*Maze, error) {
	mazePath, err := config.Get("ENV_MAZE_PATH")
	if err != nil {
		return nil, fmt.Errorf("new maze error: %w", err)
	}
	maze, err := openMaze(mazePath)
	if err != nil {
		return nil, fmt.Errorf("new maze error: %w", err)
	}
	height := len(maze)
	width := len(maze[0])

	defaultReward, err := config.GetAsFloat64("ENV_DEFAULT_REWARD")
	if err != nil {
		return nil, fmt.Errorf("new maze error: %w", err)
	}

	goalReward, err := config.GetAsFloat64("ENV_GOAL_REWARD")
	if err != nil {
		return nil, fmt.Errorf("new maze error: %w", err)
	}

	wallReward, err := config.GetAsFloat64("ENV_WALL_REWARD")
	if err != nil {
		return nil, fmt.Errorf("new maze error: %w", err)
	}

	initH, initW := 1, 1
	goalH, goalW := height-2, width-2
	h, w := initH, initW

	return &Maze{
		maze,
		height,
		width,
		defaultReward,
		goalReward,
		wallReward,
		initH,
		initW,
		goalH,
		goalW,
		h,
		w,
	}, nil
}

func openMaze(path string) ([][]rune, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("open maze error: %w", err)
	}
	defer f.Close()

	sc := bufio.NewScanner(f)

	res := [][]rune{}

	for sc.Scan() {
		res = append(res, []rune(sc.Text()))
	}
	if sc.Err() != nil {
		return nil, fmt.Errorf("open maze error: %w", sc.Err())
	}

	return res, nil
}

func (m *Maze) posToS(h, w int) State { return h*m.width + w }

func (m *Maze) isGoal() bool { return m.h == m.goalH && m.w == m.goalW }

func (m *Maze) isWall() bool { return m.maze[m.h][m.w] == '#' }

func (m *Maze) StateSize() int { return m.height * m.width }

func (*Maze) ActionSize() int { return 4 }

func (m *Maze) State() State { return m.posToS(m.h, m.w) }

func (m *Maze) Reward() Reward {
	if m.isWall() {
		return m.wallReward
	} else if m.isGoal() {
		return m.goalReward
	}
	return m.defaultReward
}

func (m *Maze) Info() string { return fmt.Sprintf("%d,%d", m.h, m.w) }

func (m *Maze) RunStep(a Action) {
	if a == 0 {
		m.h--
	} else if a == 1 {
		m.h++
	} else if a == 2 {
		m.w--
	} else if a == 3 {
		m.w++
	} else {
		panic(fmt.Errorf("action index out of range: %d", a))
	}
}

func (m *Maze) Reset() {
	m.h = m.initH
	m.w = m.initW
}

func (m *Maze) IsFinish() bool { return m.isGoal() || m.isWall() }

type Cartpole struct {
	actions []float64

	xBounds, thetaBounds, xDotBounds, thetaDotBounds [2]float64

	xSize, thetaSize, xDotSize, thetaDotSize int

	g, m, l, ml, mass float64

	tau float64

	initState, s CartpoleState
}

func NewCartpole(config *Config) (*Cartpole, error) {
	aLeft, err := config.GetAsFloat64("ENV_ACTION_LEFT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	aRight, err := config.GetAsFloat64("ENV_ACTION_RIGHT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	actions := []float64{aLeft, aRight}

	xLeft, err := config.GetAsFloat64("ENV_X_LEFT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	xRight, err := config.GetAsFloat64("ENV_X_RIGHT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	xBounds := [2]float64{xLeft, xRight}

	thetaLeft, err := config.GetAsFloat64("ENV_THETA_LEFT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaRight, err := config.GetAsFloat64("ENV_THETA_RIGHT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaBounds := [2]float64{thetaLeft, thetaRight}

	xDotLeft, err := config.GetAsFloat64("ENV_XDOT_LEFT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	xDotRight, err := config.GetAsFloat64("ENV_XDOT_RIGHT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	xDotBounds := [2]float64{xDotLeft, xDotRight}

	thetaDotLeft, err := config.GetAsFloat64("ENV_THETADOT_LEFT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaDotRight, err := config.GetAsFloat64("ENV_THETADOT_RIGHT")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaDotBounds := [2]float64{thetaDotLeft, thetaDotRight}

	xSize, err := config.GetAsInt("ENV_X_SIZE")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaSize, err := config.GetAsInt("ENV_THETA_SIZE")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	xDotSize, err := config.GetAsInt("ENV_XDOT_SIZE")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	thetaDotSize, err := config.GetAsInt("ENV_THETADOT_SIZE")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}

	g, err := config.GetAsFloat64("ENV_GRAVITY")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	cartMass, err := config.GetAsFloat64("ENV_CART_MASS")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	m, err := config.GetAsFloat64("ENV_POLE_MASS")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	l, err := config.GetAsFloat64("ENV_POLE_LENGTH")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	ml := m * l
	mass := cartMass + m

	fps, err := config.GetAsInt("ENV_FRAME_PER_SECOND")
	if err != nil {
		return nil, fmt.Errorf("new cartpole error: %w", err)
	}
	tau := 1. / float64(fps)

	initState := CartpoleState{0., math.Pi, 0., 0.}
	s := initState

	return &Cartpole{
		actions,
		xBounds,
		thetaBounds,
		xDotBounds,
		thetaDotBounds,
		xSize,
		thetaSize,
		xDotSize,
		thetaDotSize,
		g,
		m,
		l,
		ml,
		mass,
		tau,
		initState,
		s,
	}, nil
}

func (cp *Cartpole) solveRungeKutta(s CartpoleState, u, dt float64) CartpoleState {
	k1 := cp.differential(s, u)
	s1 := cp.solveEuler(s, k1, dt/2.)
	k2 := cp.differential(s1, u)
	s2 := cp.solveEuler(s, k2, dt/2.)
	k3 := cp.differential(s2, u)
	s3 := cp.solveEuler(s, k3, dt)
	k4 := cp.differential(s3, u)

	sNext := s
	for i := 0; i < len(s); i++ {
		sNext[i] += (k1[i] + 2.*k2[i] + 2.*k3[i] + k4[i]) * dt / 6.
	}
	sNext[1] = cp.normalize(sNext[1])

	return sNext
}

func (cp *Cartpole) differential(s CartpoleState, u float64) CartpoleState {
	theta := s[1]
	xDot := s[2]
	thetaDot := s[3]

	sin := math.Sin
	cos := math.Cos

	sinTheta := sin(theta)
	cosTheta := cos(theta)

	l := cp.l
	g := cp.g
	m := cp.m
	ml := cp.ml
	mass := cp.mass

	thetaDot2 := math.Pow(thetaDot, 2.)
	cosTheta2 := math.Pow(cosTheta, 2.)

	xDDot := (4.*u/3. + 4.*ml*thetaDot2*sinTheta/3. - m*g*sin(2.*theta)/2.) /
		(4.*mass - m*cosTheta2)
	thetaDDot := (mass*g*sinTheta - ml*thetaDot2*sinTheta*cosTheta - u*cosTheta) /
		(4.*mass*l/3. - ml*cosTheta2)

	return CartpoleState{xDot, thetaDot, xDDot, thetaDDot}
}

func (cp *Cartpole) solveEuler(s, sDot CartpoleState, dt float64) CartpoleState {
	res := s
	for i := 0; i < len(s); i++ {
		res[i] += sDot[i] * dt
	}
	return res
}

func (cp *Cartpole) StateSize() int {
	return cp.xSize * cp.thetaSize * cp.xDotSize * cp.thetaDotSize
}

func (cp *Cartpole) ActionSize() int { return len(cp.actions) }

func (cp *Cartpole) State() State {
	xIdx := cp.digitize(cp.xBounds, cp.xSize, cp.s[0])
	thetaIdx := cp.digitize(cp.thetaBounds, cp.thetaSize, cp.s[1])
	xDotIdx := cp.digitize(cp.xDotBounds, cp.xDotSize, cp.s[2])
	thetaDotIdx := cp.digitize(cp.thetaDotBounds, cp.thetaDotSize, cp.s[3])

	return ((xIdx*cp.thetaSize+thetaIdx)*cp.xDotSize+xDotIdx)*cp.thetaDotSize + thetaDotIdx
}

func (cp *Cartpole) Info() string {
	return fmt.Sprintf("%.15f,%.15f,%.15f,%.15f", cp.s[0], cp.s[1], cp.s[2], cp.s[3])
}

func (cp *Cartpole) Reward() Reward {
	x := cp.s[0]
	if math.Abs(x) > 2. {
		return -2.
	}
	theta := cp.s[1]
	return -math.Abs(theta) + math.Pi/2. - 0.01*math.Abs(x)
}

func (cp *Cartpole) Reset() {
	cp.s = cp.initState
}

func (cp *Cartpole) RunStep(a Action) {
	u := cp.actions[a]
	cp.s = cp.solveRungeKutta(cp.s, u, cp.tau)
}

func (cp *Cartpole) IsFinish() bool {
	return false
}

func (*Cartpole) digitize(bounds [2]float64, num int, val float64) int {
	if val < bounds[0] {
		return 0
	} else if val >= bounds[1] {
		return num - 1
	}
	width := (bounds[1] - bounds[0]) / float64(num-2)
	return int((val-bounds[0])/width) + 1
}

func (*Cartpole) normalize(theta float64) float64 {
	return math.Mod(theta+3.*math.Pi, 2.*math.Pi) - math.Pi
}

type CartpoleState [4]float64
