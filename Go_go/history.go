package main

import (
	"bufio"
	"fmt"
	"os"
)

type History struct {
	Actions []Action
	Rewards []Reward
	States  []State
	Info    []string
}

func NewHistory() *History {
	return &History{
		[]Action{},
		[]Reward{},
		[]State{},
		[]string{},
	}
}

func (h *History) Append(a Action, r Reward, s State, info string) {
	h.Actions = append(h.Actions, a)
	h.Rewards = append(h.Rewards, r)
	h.States = append(h.States, s)
	h.Info = append(h.Info, info)
}

func (h *History) Save(path string) error {
	f, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("history save error: %w", err)
	}
	defer f.Close()

	w := bufio.NewWriter(f)
	defer w.Flush()

	for i := 0; i < len(h.Actions); i++ {
		line := fmt.Sprintf("%d\t%.15f\t%d\t%s\n",
			h.Actions[i], h.Rewards[i], h.States[i], h.Info[i])
		w.WriteString(line)
	}

	return nil
}
