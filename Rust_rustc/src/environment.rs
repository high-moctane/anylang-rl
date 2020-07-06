use crate::{Action, Reward, State};

pub mod cartpole;
pub mod maze;

pub trait Environment {
    fn state_size(&self) -> usize;

    fn action_size(&self) -> usize;

    fn state(&self) -> State;

    fn reward(&self) -> Reward;

    fn info(&self) -> String;

    fn run_step(&mut self, a: Action);

    fn reset(&mut self);

    fn is_finish(&self) -> bool;
}
