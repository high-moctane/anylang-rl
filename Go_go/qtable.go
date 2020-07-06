package main

type QTable struct {
	StateSize, ActionSize int
	InitQValue            float64
	Table                 [][]float64
}

func NewQTable(stateSize, actionSize int, initQValue float64) *QTable {
	table := make([][]float64, stateSize)
	for i := 0; i < stateSize; i++ {
		table[i] = make([]float64, actionSize)
		for j := 0; j < actionSize; j++ {
			table[i][j] = initQValue
		}
	}

	return &QTable{stateSize, actionSize, initQValue, table}
}
