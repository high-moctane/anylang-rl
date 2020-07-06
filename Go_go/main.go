package main

import (
	"log"
	"os"
)

func main() {
	if err := run(os.Args[1:]); err != nil {
		log.Fatal(err)
	}
}

func run(args []string) error {
	config, err := NewConfig(args)
	if err != nil {
		return err
	}

	rl, err := NewRL(config)
	if err != nil {
		return err
	}

	rl.Run()
	if err := rl.SaveReturns(); err != nil {
		return err
	}
	rl.RunTest()
	if err := rl.SaveTestHistory(); err != nil {
		return err
	}

	return nil
}

type Action = int
type Reward = float64
type State = int
