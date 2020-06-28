use crate::{Action, Reward, State};
use std::fs::File;
use std::io::BufWriter;
use std::io::Write;

pub struct History {
    pub a: Vec<Action>,
    pub s: Vec<State>,
    pub r: Vec<Reward>,
    pub info: Vec<String>,
}

impl History {
    pub fn new() -> Self {
        History {
            a: vec![],
            s: vec![],
            r: vec![],
            info: vec![],
        }
    }

    pub fn push(&mut self, a: Action, s: State, r: Reward, info: &str) {
        self.a.push(a);
        self.s.push(s);
        self.r.push(r);
        self.info.push(String::from(info));
    }

    pub fn save(&self, path: &str) -> std::io::Result<()> {
        let file = File::create(path)?;
        let mut writer = BufWriter::new(&file);

        for i in 0..self.a.len() {
            writer.write(
                format!(
                    "{}\t{}\t{:.15}\t{}\n",
                    self.a[i], self.s[i], self.r[i], &self.info[i]
                )
                .as_bytes(),
            )?;
        }

        writer.flush()?;

        Ok(())
    }
}
