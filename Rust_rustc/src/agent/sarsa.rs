use crate::agent;
use crate::config::Config;
use crate::q_table::QTable;
use crate::{Action, Reward, State};
use rand;
use rand::prelude::*;
use std::error::Error;
use std::f64;

pub struct Sarsa {
    alpha: f64,
    gamma: f64,
    eps: f64,

    rng: ThreadRng,
}

impl Sarsa {
    pub fn new(config: &Config) -> Result<Sarsa, Box<dyn Error>> {
        let alpha = config.get("AGENT_ALPHA")?.parse()?;
        let gamma = config.get("AGENT_GAMMA")?.parse()?;
        let eps: f64 = config.get("AGENT_EPSILON")?.parse()?;
        let rng = rand::thread_rng();
        Ok(Sarsa {
            alpha,
            gamma,
            eps,
            rng,
        })
    }
}

impl agent::Agent for Sarsa {
    fn action(&mut self, q_table: &QTable, s: State) -> Action {
        if self.rng.gen::<f64>() < self.eps {
            self.rng.gen_range(0, q_table.action_size)
        } else {
            argmax(&q_table.table[s])
        }
    }

    fn learn(&self, q_table: &mut QTable, s1: State, a1: Action, r: Reward, s2: State, a2: Action) {
        let alpha = self.alpha;
        let gamma = self.gamma;

        q_table.table[s1][a1] = (1.0 - self.alpha) * q_table.table[s1][a1]
            + alpha * (r + gamma * q_table.table[s2][a2]);
    }

    fn fix(&mut self) {
        self.alpha = 0.;
        self.eps = 0.;
    }
}

fn argmax<T: PartialOrd>(slice: &[T]) -> usize {
    let mut res = 0;
    for i in 1..slice.len() {
        if slice[res] < slice[i] {
            res = i
        }
    }
    return res;
}
