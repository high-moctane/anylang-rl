use crate::env;

use rand::prelude::random;
use std::f64;
use std::f64::consts::PI;

const ALPHA: f64 = 0.1; // 学習率
const GAMMA: f64 = 0.999; // 割引率
const EPSILON: f64 = 0.1; // ランダムに行動選択する割合

const INIT_QVALUE: f64 = 10000.0; // q-value の初期値
const ACTIONS: [f64; 2] = [-10.0, 10.0]; // 行動の候補

// 状態分割の下限と上限
const X_LIMITS: [f64; 2] = [-2.0, 2.0];
const THETA_LIMITS: [f64; 2] = [-PI, PI];
const XDOT_LIMITS: [f64; 2] = [-2.0, 2.0];
const THETADOT_LIMITS: [f64; 2] = [-10.0, 10.0];

// 状態の分割数
const X_NUM: usize = 4;
const THETA_NUM: usize = 40;
const XDOT_NUM: usize = 10;
const THETADOT_NUM: usize = 50;

pub struct Agent {
    alpha: f64,
    gamma: f64,
    epsilon: f64,
    q_table: Vec<Vec<f64>>,

    // 状態分割の bins
    x_bins: Vec<f64>,
    theta_bins: Vec<f64>,
    xdot_bins: Vec<f64>,
    thetadot_bins: Vec<f64>,
}

impl Agent {
    pub fn new() -> Agent {
        Agent {
            alpha: ALPHA,
            gamma: GAMMA,
            epsilon: EPSILON,
            q_table: new_qtable(),

            x_bins: make_bins(X_LIMITS, X_NUM),
            theta_bins: make_bins(THETA_LIMITS, THETA_NUM),
            xdot_bins: make_bins(XDOT_LIMITS, XDOT_NUM),
            thetadot_bins: make_bins(THETADOT_LIMITS, THETADOT_NUM),
        }
    }

    pub fn test_agent(agent: &mut Agent) {
        agent.alpha = 0.0;
        agent.epsilon = 0.0;
    }

    pub fn action(&self, s: &env::State) -> env::Action {
        if random::<f64>() < self.epsilon {
            let idx = (random::<f64>() * 2.0).floor() as usize;
            return ACTIONS[idx];
        }
        let s_idx = self.get_s_idx(s);
        let max_idx = argmax(&self.q_table[s_idx]);
        ACTIONS[max_idx]
    }

    pub fn learn(&mut self, s: &env::State, a: env::Action, r: env::Reward, snext: &env::State) {
        let s_idx = self.get_s_idx(s);
        let a_idx = ACTIONS.iter().position(|&x| x == a).unwrap();
        let snext_idx = self.get_s_idx(snext);

        self.q_table[s_idx][a_idx] = (1.0 - self.alpha) * self.q_table[s_idx][a_idx]
            + self.alpha
                * (r + self.gamma
                    * self.q_table[snext_idx]
                        .iter()
                        .fold(f64::NEG_INFINITY, |m, &v| m.max(v)))
    }

    fn dizitize_all(&self, s: &env::State) -> (usize, usize, usize, usize) {
        let x_idx = digitize(&self.x_bins, s[0]);
        let theta_idx = digitize(&self.theta_bins, s[1]);
        let xdot_idx = digitize(&self.xdot_bins, s[2]);
        let thetadot_idx = digitize(&self.thetadot_bins, s[3]);
        (x_idx, theta_idx, xdot_idx, thetadot_idx)
    }

    fn get_s_idx(&self, s: &env::State) -> usize {
        let indices = self.dizitize_all(s);
        indices.0 + X_NUM * (indices.1 + THETA_NUM * (indices.2 + XDOT_NUM * indices.3))
    }
}

fn make_bins(limits: [f64; 2], num: usize) -> Vec<f64> {
    let width = (limits[1] - limits[0]) / (num - 2) as f64;
    let mut ans = Vec::with_capacity(num - 1);
    for i in 0..num - 1 {
        ans.push(limits[0] + width * i as f64)
    }
    ans
}

fn digitize<T: PartialOrd>(bins: &[T], x: T) -> usize {
    for i in 0..bins.len() {
        if x < bins[i] {
            return i;
        }
    }
    bins.len()
}

fn new_qtable() -> Vec<Vec<f64>> {
    let max_num = X_NUM * THETA_NUM * XDOT_NUM * THETADOT_NUM;
    let mut ans = Vec::with_capacity(max_num);
    for _ in 0..max_num {
        ans.push(vec![INIT_QVALUE, INIT_QVALUE]);
    }
    ans
}

fn argmax<T: PartialOrd>(v: &[T]) -> usize {
    let mut idx = 0;

    for i in 0..v.len() {
        if v[idx] < v[i] {
            idx = i;
        }
    }
    idx
}
