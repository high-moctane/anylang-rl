use crate::agent;
use crate::env;

const EPISODES_NUM: usize = 10000000;
const STEPS_NUM: usize = env::FPS as usize * 10;

pub struct History {
    pub states: Vec<env::State>,
    pub actions: Vec<env::Action>,
    pub rewards: Vec<env::Reward>,
}

impl History {
    pub fn new() -> History {
        History {
            states: Vec::with_capacity(EPISODES_NUM),
            actions: Vec::with_capacity(EPISODES_NUM),
            rewards: Vec::with_capacity(EPISODES_NUM),
        }
    }
}

pub fn run(agent: &mut agent::Agent) -> Vec<f64> {
    let mut returns: Vec<f64> = Vec::with_capacity(EPISODES_NUM);

    for _ in 0..EPISODES_NUM {
        let hist = one_episode(agent);
        returns.push(hist.rewards.iter().sum())
    }

    returns
}

pub fn test(agent: &mut agent::Agent) -> History {
    agent::Agent::test_agent(agent);
    one_episode(agent)
}

pub fn one_episode(agent: &mut agent::Agent) -> History {
    let mut hist = History::new();

    let mut s = env::new_state();
    let mut a = 0.0;
    let mut r = 0.0;

    for _ in 0..STEPS_NUM {
        hist.states.push(s);
        hist.actions.push(a);
        hist.rewards.push(r);

        a = agent.action(&s);
        let snext = env::step(&s, a);
        r = env::reward(&snext);
        agent.learn(&s, a, r, &snext);

        s = snext;
    }

    hist
}
