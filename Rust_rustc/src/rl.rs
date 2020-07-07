use crate::agent::q_learning::QLearning;
use crate::agent::sarsa::Sarsa;
use crate::agent::Agent;
use crate::config::Config;
use crate::environment::cartpole::Cartpole;
use crate::environment::maze::Maze;
use crate::environment::Environment;
use crate::history::History;
use crate::q_table::{QTable, QValue};
use std::error::Error;
use std::fmt;
use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::io::BufWriter;

pub struct RL {
    returns_path: String,
    test_history_path: String,

    max_episode: usize,
    max_step: usize,

    agent: Box<dyn Agent>,
    env: Box<dyn Environment>,
    q_table: QTable,

    returns: Vec<f64>,
    test_history: History,
}

impl RL {
    pub fn new(config: &Config) -> Result<RL, Box<dyn Error>> {
        let returns_path = config.get("RL_RETURNS_PATH")?;
        let test_history_path = config.get("RL_TEST_HISTORY_PATH")?;

        let max_episode = config.get("RL_MAX_EPISODE")?.parse()?;
        let max_step = config.get("RL_MAX_STEP")?.parse()?;

        let agent = RL::choose_agent(&config)?;
        let env = RL::choose_environment(&config)?;

        let init_qvalue = config.get("QTABLE_INITIAL_QVALUE")?.parse::<QValue>()?;
        let q_table = QTable::new(env.state_size(), env.action_size(), init_qvalue);

        let returns = vec![];
        let test_history = History::new();

        Ok(RL {
            returns_path,
            test_history_path,
            max_episode,
            max_step,
            agent,
            env,
            q_table,
            returns,
            test_history,
        })
    }

    fn choose_agent(config: &Config) -> Result<Box<dyn Agent>, Box<dyn Error>> {
        let agent_name = config.get("AGENT_NAME")?;
        match agent_name.as_str() {
            "Sarsa" => Ok(Box::new(Sarsa::new(&config)?)),
            "Q-learning" => Ok(Box::new(QLearning::new(&config)?)),
            _ => Err(Box::new(AgentNameError::new(&agent_name))),
        }
    }

    fn choose_environment(config: &Config) -> Result<Box<dyn Environment>, Box<dyn Error>> {
        let env_name = config.get("ENV_NAME")?;
        match env_name.as_str() {
            "Cartpole" => Ok(Box::new(Cartpole::new(&config)?)),
            "Maze" => Ok(Box::new(Maze::new(&config)?)),
            _ => Err(Box::new(EnvironmentNameError::new(&env_name))),
        }
    }

    pub fn run(&mut self) {
        for _episode in 0..self.max_episode {
            let history = self.run_episode();
            self.returns.push(history.rewards.iter().sum())
        }
    }

    fn run_episode(&mut self) -> History {
        let mut history = History::new();

        self.env.reset();

        let mut s1 = self.env.state();
        let mut s2 = s1;
        let mut r = self.env.reward();
        let mut info = self.env.info();
        let mut a1 = self.agent.action(&self.q_table, s1);
        let mut a2;

        history.push(a1, r, s2, &info);

        for _step in 0..self.max_step {
            self.env.run_step(a1);
            s2 = self.env.state();
            r = self.env.reward();
            info = self.env.info();
            a2 = self.agent.action(&self.q_table, s2);

            history.push(a1, r, s2, &info);

            if self.env.is_finish() {
                for i in 0..self.q_table.action_size {
                    self.q_table.table[s2][i] = 0.;
                }
            }
            self.agent.learn(&mut self.q_table, s1, a1, r, s2, a2);

            if self.env.is_finish() {
                break;
            }

            s1 = s2;
            a1 = a2;
        }

        history
    }

    pub fn run_test(&mut self) {
        self.agent.fix();
        self.test_history = self.run_episode();
    }

    pub fn save_returns(&self) -> io::Result<()> {
        let file = File::create(&self.returns_path)?;
        let mut writer = BufWriter::new(file);

        for ret in &self.returns {
            writer.write(&format!("{:.15}\n", ret).as_bytes())?;
        }

        writer.flush()?;

        Ok(())
    }

    pub fn save_test_history(&self) -> io::Result<()> {
        self.test_history.save(&self.test_history_path)?;
        Ok(())
    }
}

#[derive(Debug)]
struct AgentNameError {
    name: String,
}

impl AgentNameError {
    fn new(name: &str) -> AgentNameError {
        AgentNameError {
            name: String::from(name),
        }
    }
}

impl Error for AgentNameError {}

impl fmt::Display for AgentNameError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid agent name: {}", &self.name)
    }
}

#[derive(Debug)]
struct EnvironmentNameError {
    name: String,
}

impl EnvironmentNameError {
    fn new(name: &str) -> EnvironmentNameError {
        EnvironmentNameError {
            name: String::from(name),
        }
    }
}

impl Error for EnvironmentNameError {}

impl fmt::Display for EnvironmentNameError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid environment name: {}", &self.name)
    }
}
