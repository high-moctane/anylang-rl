use crate::agent::Agent;
use crate::config::Config;
use crate::q_table::QTable;
use crate::{Action, Reward, State};
use rand;
use rand::Rng;
use std::error;

pub struct QLearning {
    alpha: f64,
    gamma: f64,
    eps: f64,
    // rng: Box<dyn rand::RngCore>,
    rng: rand::rngs::ThreadRng,
}

impl QLearning {
    pub fn new(config: &Config) -> Result<Box<Self>, Box<dyn error::Error>> {
        let alpha: f64 = config.get("AGENT_ALPHA")?.parse()?;
        let gamma: f64 = config.get("AGENT_GAMMA")?.parse()?;
        let eps: f64 = config.get("AGENT_EPSILON")?.parse()?;

        Ok(Box::new(QLearning {
            alpha,
            gamma,
            eps,
            rng: rand::thread_rng(),
            // TODO: Random seed
        }))
    }
}

impl Agent for QLearning {
    fn a(&mut self, q_table: &QTable, s: State) -> Action {
        let random_probability: f64 = self.rng.gen();
        if random_probability < self.eps {
            self.rng.gen_range(0, q_table.a_space)
        } else {
            argmax(&q_table.table[s])
        }
    }

    fn learn(
        &self,
        q_table: &mut QTable,
        s1: State,
        a1: Action,
        r: Reward,
        s2: State,
        _a2: Action,
    ) {
        let max = max(&q_table.table[s2]);
        q_table.table[s1][a1] =
            (1. - self.alpha) * q_table.table[s1][a1] + self.alpha * (r + self.gamma * max);
    }

    fn fix(&mut self) {
        self.alpha = 0.;
        self.eps = 0.;
    }
}

fn argmax<T: PartialOrd>(slice: &[T]) -> usize {
    let mut res = 0;
    for i in 1..slice.len() {
        if slice[i] > slice[res] {
            res = i;
        }
    }
    res
}

fn max(slice: &[f64]) -> f64 {
    slice.iter().fold(0. / 0., |m, v| v.max(m))
}
