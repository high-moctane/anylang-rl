package main

import "math"

type Env struct {
	// NOTE: 本当だったら const で定義したいが gopath になくてめんどい
	// 先頭大文字か小文字かで意味が変わってくるが書き捨てプログラムなので無視
	g    float64 // 重力加速度
	M    float64 // カートの質量
	m    float64 // ポールの質量
	l    float64 // ポールの半分の長さ
	ml   float64 //あとの計算で使う
	mass float64 //あとの計算で使う
	fps  int     // frames per second
	tau  float64 // 制御周期

	s []float64 // 状態 [x, theta, xdot, thetadot]
}

func NewEnv() *Env {
	return &Env{
		g:    9.80665,
		M:    1.0,
		m:    0.1,
		l:    0.5,
		ml:   0.1 * 0.5,
		mass: 1.0 + 0.1,
		fps:  50,
		tau:  1.0 / 50,
		s:    []float64{0.0, -math.Pi, 0.0, 0.0},
	}
}

func (e *Env) ResetEnv() {
	e.s = []float64{0.0, -math.Pi, 0.0, 0.0}
}

func (e *Env) State() []float64 {
	return e.s
}

func (e *Env) Reward() float64 {
	x, theta, _, _ := sToParams(e.s)
	if math.Abs(x) > 2.0 {
		return -2.0
	}
	return -math.Abs(theta) + math.Pi/2.0
}

func (e *Env) Step(a float64) {
	e.s = e.rungeKuttaSolve(e.s, a, e.tau)
}

// differential は状態 s で力 u を加えたときの微分
func (e *Env) differential(s []float64, u float64) []float64 {
	_, theta, xdot, thetadot := sToParams(s)
	sintheta := math.Sin(theta)
	costheta := math.Cos(theta)

	xddot := (4.0*u/3.0 + 4.0*e.ml*math.Pow(thetadot, 2.0)*sintheta/3.0 - e.m*e.g*math.Sin(2.0*theta)/2.0) / (4.0*e.mass - e.m*math.Pow(costheta, 2.0))
	thetaddot := (e.mass*e.g*sintheta - e.ml*math.Pow(thetadot, 2.0)*sintheta*costheta - u*costheta) / (4.0*e.mass*e.l/3.0 - e.ml*math.Pow(costheta, 2.0))

	return []float64{xdot, thetadot, xddot, thetaddot}
}

// eulerSolve はオイラー法を用いて微分方程式を解く
func (*Env) eulerSolve(s, sdot []float64, dt float64) []float64 {
	ret := make([]float64, 4)
	for i := 0; i < 4; i++ {
		ret[i] = s[i] + sdot[i]*dt
	}
	return ret
}

// rungeKuttaSolve はルンゲクッタ法を用いて微分方程式を解く
func (e *Env) rungeKuttaSolve(s []float64, u, dt float64) []float64 {
	k1 := e.differential(s, u)
	s1 := e.eulerSolve(s, k1, dt/2.0)
	k2 := e.differential(s1, u)
	s2 := e.eulerSolve(s, k2, dt/2)
	k3 := e.differential(s2, u)
	s3 := e.eulerSolve(s, k3, dt)
	k4 := e.differential(s3, u)

	sNext := make([]float64, 4)
	for i := 0; i < 4; i++ {
		sNext[i] = s[i] + (k1[i]+2.0*k2[i]+2.0*k3[i]+k4[i])*dt/6.0
	}
	sNext[1] = math.Mod(sNext[1]+3.0*math.Pi, 2.0*math.Pi) - math.Pi
	return sNext
}

// こういう関数を作っておくとバグが減らせるかも
func sToParams(s []float64) (float64, float64, float64, float64) {
	// x, theta, xdot, thetadot
	return s[0], s[1], s[2], s[3]
}
