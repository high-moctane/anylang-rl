package main

import (
	"math"
	"math/rand"
	"time"
)

func init() {
	// golang の rand は seed 与えないと毎回同じなので与える
	rand.Seed(time.Now().UnixNano())
}

type Agent struct {
	// NOTE: 定数を struct の内部に含めるのはあんまり気持ちよくないが，
	// グローバルに定数を置くのも気がひけるので仕方なくこういう仕様にする

	initQvalue float64   // Q-value の初期値
	actions    []float64 // 行動の候補

	// 状態分割の下限と上限
	xLimits, thetaLimits, xdotLimits, thetadotLimits []float64

	// 状態の分割数
	xNum, thetaNum, xdotNum, thetadotNum int

	// 状態分割の bins
	xBins, thetaBins, xdotBins, thetadotBins []float64

	// 学習に使うパラメータ
	alpha float64 // 学習率
	gamma float64 // 割引率
	eps   float64 // ランダムに行動選択する割合

	// 深いスライスは生成に泣いてしまう
	qTable [][]float64
}

func NewAgent() *Agent {
	initQvalue := 10000.0
	actions := []float64{-10.0, 10.0}

	xLimits := []float64{-2.0, 2.0}
	thetaLimits := []float64{-math.Pi, math.Pi}
	xdotLimits := []float64{-2.0, 2.0}
	thetadotLimits := []float64{-10.0, 10.0}

	xNum := 4
	thetaNum := 40
	xdotNum := 10
	thetadotNum := 50

	xBins := makeBins(xLimits, xNum)
	thetaBins := makeBins(thetaLimits, thetaNum)
	xdotBins := makeBins(xdotLimits, xdotNum)
	thetadotBins := makeBins(thetadotLimits, thetadotNum)

	alpha := 0.1
	gamma := 0.999
	eps := 0.1

	qTable := makeQtable(xNum*thetaNum*xdotNum*thetadotNum, len(actions), initQvalue)

	// こういうの書いてるとグローバルを汚染したくなる
	return &Agent{
		initQvalue:     initQvalue,
		actions:        actions,
		xLimits:        xLimits,
		thetaLimits:    thetaLimits,
		xdotLimits:     xdotLimits,
		thetadotLimits: thetadotLimits,
		xNum:           xNum,
		thetaNum:       thetaNum,
		xdotNum:        xdotNum,
		thetadotNum:    thetadotNum,
		xBins:          xBins,
		thetaBins:      thetaBins,
		xdotBins:       xdotBins,
		thetadotBins:   thetadotBins,
		alpha:          alpha,
		gamma:          gamma,
		eps:            eps,
		qTable:         qTable,
	}
}

// Action は eps-greedy 方策です
func (ag *Agent) Action(s []float64) float64 {
	if rand.Float64() < ag.eps {
		return ag.actions[rand.Intn(len(ag.actions))]
	}

	sIdx := ag.sIndex(s)
	maxIdx := argmax(ag.qTable[sIdx])
	return ag.actions[maxIdx]
}

func (ag *Agent) Learn(s []float64, a float64, r float64, sNext []float64) {
	sIdx := ag.sIndex(s)
	aIdx := findIdx(ag.actions, a)
	sNextIdx := ag.sIndex(sNext)

	ag.qTable[sIdx][aIdx] =
		(1.0-ag.alpha)*ag.qTable[sIdx][aIdx] +
			ag.alpha*(r+ag.gamma*findMax(ag.qTable[sNextIdx]))
}

// SetTestParams で test 用のパラメータに変更する
func (ag *Agent) SetTestParams() {
	ag.alpha = 0.0
	ag.eps = 0.0
}

func makeBins(limits []float64, num int) []float64 {
	width := (limits[1] - limits[0]) / float64(num-2)
	bins := make([]float64, num-1)
	for i := 0; i < num-1; i++ {
		bins[i] = limits[0] + width*float64(i)
	}
	return bins
}

func makeQtable(sLen, aLen int, initQvalue float64) [][]float64 {
	qTable := make([][]float64, sLen)
	for i := 0; i < sLen; i++ {
		qTable[i] = make([]float64, aLen)
		for j := 0; j < aLen; j++ {
			qTable[i][j] = initQvalue
		}
	}
	return qTable
}

func (*Agent) digitize(bins []float64, x float64) int {
	for i, v := range bins {
		if x < v {
			return i
		}
	}
	return len(bins)
}

func (ag *Agent) digitizeAll(s []float64) (int, int, int, int) {
	xIdx := ag.digitize(ag.xBins, s[0])
	thetaIdx := ag.digitize(ag.thetaBins, s[1])
	xdotIdx := ag.digitize(ag.xdotBins, s[2])
	thetadotIdx := ag.digitize(ag.thetadotBins, s[3])
	return xIdx, thetaIdx, xdotIdx, thetadotIdx
}

func (ag *Agent) sIndex(s []float64) int {
	xIdx, thetaIdx, xdotIdx, thetadotIdx := ag.digitizeAll(s)
	return xIdx + ag.xNum*(thetaIdx+ag.thetaNum*(xdotIdx+ag.xdotNum*thetadotIdx))
}

// argmax は []floats しか受け取れないが仕方がないのである
func argmax(floats []float64) int {
	idx := 0
	maxVal := floats[0]
	for i, v := range floats {
		if v > maxVal {
			idx = i
			maxVal = v
		}
	}
	return idx
}

func findIdx(floats []float64, x float64) int {
	for i, v := range floats {
		if x == v {
			return i
		}
	}
	// めんどくさいので panic でいいや
	panic("not found x")
}

func findMax(floats []float64) float64 {
	max := floats[0]
	for _, v := range floats {
		if v > max {
			max = v
		}
	}
	return max
}
