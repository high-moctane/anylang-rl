use crate::agent::q_learning::QLearning;
use crate::agent::Agent;
use crate::config::Config;
use crate::environment::maze::Maze;
use crate::environment::Environment;
use crate::experiment::Experiment;
use std::env;
use std::error;
use std::fmt;

mod agent;
mod config;
mod environment;
mod experiment;
mod history;
mod q_table;

pub struct Runner {
    config: Config,
}

impl Runner {
    pub fn new(args: env::Args) -> Result<Self, Box<dyn error::Error>> {
        let config_path = Runner::parse_args(args)?;
        let config = Config::new(&config_path)?;
        Ok(Runner { config })
    }

    fn parse_args(args: env::Args) -> Result<String, InvalidArgsError> {
        let argvec: Vec<String> = args.collect();
        if argvec.len() != 2 {
            return Err(InvalidArgsError::new(argvec));
        }
        let config_path = argvec[1].clone();
        Ok(config_path)
    }

    pub fn run(&self) -> Result<(), Box<dyn error::Error>> {
        let agent = self.choose_agent()?;
        let env = self.choose_environment()?;
        let mut exp = Experiment::new(&self.config, agent, env)?;

        exp.run();
        exp.save_returns()?;
        exp.test_and_save()?;

        Ok(())
    }

    fn choose_agent(&self) -> Result<Box<dyn Agent>, Box<dyn error::Error>> {
        let agent_name = self.config.get("AGENT_NAME")?;
        match &*agent_name {
            "Q-learning" => Ok(QLearning::new(&self.config)?),
            _ => Err(Box::new(InvalidAgentNameError::new(&agent_name))),
        }
    }

    fn choose_environment(&self) -> Result<Box<dyn Environment>, Box<dyn error::Error>> {
        let env_name = self.config.get("ENV_NAME")?;
        match &*env_name {
            "Maze" => Ok(Maze::new(&self.config)?),
            _ => Err(Box::new(InvalidEnvironmentNameError::new(&env_name))),
        }
    }
}

#[derive(Debug)]
pub struct InvalidArgsError {
    args: Vec<String>,
}

impl InvalidArgsError {
    fn new(args: Vec<String>) -> Self {
        InvalidArgsError { args }
    }
}

impl error::Error for InvalidArgsError {}

impl fmt::Display for InvalidArgsError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid args: {:?}", &self.args)
    }
}

#[derive(Debug)]
pub struct InvalidAgentNameError {
    name: String,
}

impl InvalidAgentNameError {
    fn new(name: &str) -> Self {
        InvalidAgentNameError {
            name: String::from(name),
        }
    }
}

impl error::Error for InvalidAgentNameError {}

impl fmt::Display for InvalidAgentNameError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid args: {}", &self.name)
    }
}

#[derive(Debug)]
pub struct InvalidEnvironmentNameError {
    name: String,
}

impl InvalidEnvironmentNameError {
    fn new(name: &str) -> Self {
        InvalidEnvironmentNameError {
            name: String::from(name),
        }
    }
}

impl error::Error for InvalidEnvironmentNameError {}

impl fmt::Display for InvalidEnvironmentNameError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid args: {}", &self.name)
    }
}

pub type State = usize;

pub type Action = usize;

pub type Reward = f64;
