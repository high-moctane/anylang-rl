pub type QValue = f64;

pub struct QTable {
    pub state_size: usize,
    pub action_size: usize,
    pub init_qvalue: QValue,
    pub table: Vec<Vec<QValue>>,
}

impl QTable {
    pub fn new(state_size: usize, action_size: usize, init_qvalue: QValue) -> QTable {
        let table = vec![vec![init_qvalue; action_size]; state_size];
        QTable {
            state_size,
            action_size,
            init_qvalue,
            table,
        }
    }
}
