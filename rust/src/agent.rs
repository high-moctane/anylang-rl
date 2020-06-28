use crate::q_table::QTable;
use crate::{Action, Reward, State};

pub mod q_learning;

pub trait Agent {
    fn a(&mut self, q_table: &QTable, s: State) -> Action;

    fn learn(&self, q_table: &mut QTable, s1: State, a1: Action, r: Reward, s2: State, a2: Action);

    fn fix(&mut self);
}
