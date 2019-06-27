package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	exp := NewExperiment()
	returns := exp.Run()
	hist := exp.Test()

	SaveReturns(returns)
	SaveStates(hist.states)
	SaveActions(hist.actions)
	SaveRewards(hist.rewards)
}

func SaveReturns(returns []float64) {
	f, err := os.Create("returns.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for _, r := range returns {
		w.WriteString(fmt.Sprint(r))
		w.WriteString("\n")
	}
}

func SaveStates(states [][]float64) {
	f, err := os.Create("states.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for _, s := range states {
		w.WriteString(fmt.Sprintf("%f,%f,%f,%f\n", s[0], s[1], s[2], s[3]))
	}
}

func SaveActions(actions []float64) {
	f, err := os.Create("actions.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for _, a := range actions {
		w.WriteString(fmt.Sprint(a))
		w.WriteString("\n")
	}
}

func SaveRewards(rewards []float64) {
	f, err := os.Create("rewards.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for _, r := range rewards {
		w.WriteString(fmt.Sprint(r))
		w.WriteString("\n")
	}
}
