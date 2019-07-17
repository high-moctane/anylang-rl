mod agent;
mod env;
mod experiment;

use std::fs::File;
use std::io::{self, BufWriter, Write};

pub fn run() -> io::Result<()> {
    let mut agent = agent::Agent::new();
    let returns = experiment::run(&mut agent);
    let history = experiment::test(&mut agent);

    save_returns(returns)?;
    save_states(history.states)?;
    save_actions(history.actions)?;
    save_rewards(history.rewards)?;

    Ok(())
}

fn save_returns(returns: Vec<f64>) -> io::Result<()> {
    let mut w = BufWriter::new(File::create("./returns.csv")?);
    for r in returns {
        writeln!(&mut w, "{}", r)?;
    }
    w.flush()?;
    Ok(())
}

fn save_states(states: Vec<env::State>) -> io::Result<()> {
    let mut w = BufWriter::new(File::create("./states.csv")?);
    for s in states {
        writeln!(&mut w, "{},{},{},{}", s[0], s[1], s[2], s[3])?;
    }
    w.flush()?;
    Ok(())
}

fn save_actions(actions: Vec<env::Action>) -> io::Result<()> {
    let mut w = BufWriter::new(File::create("./actions.csv")?);
    for a in actions {
        writeln!(&mut w, "{}", a)?;
    }
    w.flush()?;
    Ok(())
}

fn save_rewards(rewards: Vec<env::Action>) -> io::Result<()> {
    let mut w = BufWriter::new(File::create("./rewards.csv")?);
    for r in rewards {
        writeln!(&mut w, "{}", r)?;
    }
    w.flush()?;
    Ok(())
}
