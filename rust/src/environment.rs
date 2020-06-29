use crate::{Action, Reward, State};

pub mod cartpole;
pub mod maze;

pub trait Environment {
    fn s_space(&self) -> usize;

    fn a_space(&self) -> usize;

    fn s(&self) -> State;

    fn info(&self) -> String;

    fn r(&self) -> Reward;

    fn reset(&mut self);

    fn run_step(&mut self, a: Action);

    fn is_done(&self) -> bool;

    fn is_success(&self) -> bool;
}
