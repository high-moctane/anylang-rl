use std::error::Error;

mod agent;
mod config;
mod environment;
mod history;
mod q_table;
mod rl;

pub fn run(args: &mut std::env::Args) -> Result<(), Box<dyn Error>> {
    let config = config::Config::new(args)?;
    let mut rl = rl::RL::new(&config)?;
    rl.run();
    rl.save_returns()?;
    rl.run_test();
    rl.save_test_history()?;
    Ok(())
}

type Action = usize;
type Reward = f64;
type State = usize;
