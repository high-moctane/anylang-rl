use crate::agent::Agent;
use crate::config::Config;
use crate::environment::Environment;
use crate::history::History;
use crate::q_table::QTable;
use crate::Reward;
use std::error;
use std::fs::File;
use std::io::BufWriter;
use std::io::Write;

pub struct Experiment {
    max_episode: usize,
    max_step: usize,
    max_succeeded_episode: usize,

    // agent: Box<dyn Agent>,
    // env: Box<dyn Environment>,
    agent: Box<dyn Agent>,
    env: Box<dyn Environment>,

    q_table: QTable,

    success_count: usize,

    returns: Vec<Reward>,

    q_table_path: String,
    history_path: String,
    returns_path: String,
}

impl Experiment {
    pub fn new(
        config: &Config,
        agent: Box<dyn Agent>,
        env: Box<dyn Environment>,
    ) -> Result<Box<Self>, Box<dyn error::Error>> {
        let max_episode: usize = config.get("EXPERIMENT_MAX_EPISODE")?.parse()?;
        let max_step: usize = config.get("EXPERIMENT_MAX_STEP")?.parse()?;
        let max_succeeded_episode: usize =
            config.get("EXPERIMENT_MAX_SUCCEEDED_EPISODE")?.parse()?;

        let q_table = QTable::new(
            config.get("QTABLE_INIT_QVALUE")?.parse::<f64>()?,
            env.s_space(),
            env.a_space(),
        );

        let success_count = 0;

        let returns = vec![];

        let q_table_path = config.get("QTABLE_PATH")?;
        let history_path = config.get("HISTORY_PATH")?;
        let returns_path = config.get("RETURNS_PATH")?;

        Ok(Box::new(Experiment {
            max_episode,
            max_step,
            max_succeeded_episode,
            agent,
            env,
            q_table,
            success_count,
            returns,
            q_table_path,
            history_path,
            returns_path,
        }))
    }

    pub fn run(&mut self) {
        for _ in 0..self.max_episode {
            let (history, succeeded) = self.run_episode();
            if succeeded {
                self.success_count += 1;
            } else {
                self.success_count = 0;
            }

            self.returns.push(history.r.iter().sum());

            if self.success_count >= self.max_succeeded_episode {
                break;
            }
        }
    }

    pub fn run_episode(&mut self) -> (Box<History>, bool) {
        let mut history = History::new();

        self.env.reset();

        let mut s1 = self.env.s();
        let mut s2 = s1;
        let mut a1 = self.agent.a(&self.q_table, s1);
        let mut a2 = a1;
        let mut r = self.env.r();

        history.push(a1, s2, r, &self.env.info());

        for _ in 0..self.max_step {
            a1 = a2;
            self.env.run_step(a1);
            s2 = self.env.s();
            a2 = self.agent.a(&mut self.q_table, s2);
            r = self.env.r();
            self.agent.learn(&mut self.q_table, s1, a1, r, s2, a2);

            history.push(a1, s2, r, &self.env.info());

            s1 = s2;

            if self.env.is_done() {
                break;
            }
        }

        (Box::new(history), self.env.is_success())
    }

    pub fn test_and_save(&mut self) -> Result<(), Box<dyn error::Error>> {
        self.agent.fix();
        let (history, _) = self.run_episode();
        history.save(&self.history_path)?;
        self.q_table.save(&self.q_table_path)?;

        Ok(())
    }

    pub fn save_returns(&self) -> std::io::Result<()> {
        let file = File::create(&self.returns_path)?;
        let mut writer = BufWriter::new(&file);
        for returns in &self.returns {
            writer.write(format!("{:.15}\n", returns).as_bytes())?;
        }

        writer.flush()?;

        Ok(())
    }
}
