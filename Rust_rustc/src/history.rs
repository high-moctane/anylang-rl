use crate::{Action, Reward, State};
use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::io::BufWriter;

pub struct History {
    pub actions: Vec<Action>,
    pub rewards: Vec<Reward>,
    pub states: Vec<State>,
    pub info: Vec<String>,
}

impl History {
    pub fn new() -> History {
        History {
            actions: vec![],
            rewards: vec![],
            states: vec![],
            info: vec![],
        }
    }

    pub fn push(&mut self, a: Action, r: Reward, s: State, s_info: &str) {
        self.actions.push(a);
        self.rewards.push(r);
        self.states.push(s);
        self.info.push(String::from(s_info));
    }

    pub fn save(&self, path: &str) -> io::Result<()> {
        let file = File::create(path)?;
        let mut writer = BufWriter::new(file);

        for i in 0..self.actions.len() {
            let line = format!(
                "{}\t{:.15}\t{}\t{}\n",
                self.actions[i], self.rewards[i], self.states[i], self.info[i]
            );
            writer.write(&line.as_bytes())?;
        }

        writer.flush()?;

        Ok(())
    }
}
