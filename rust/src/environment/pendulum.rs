use crate::config::Config;
use crate::environment::Environment;
use crate::{Action, Reward, State};
use std::error;
use std::f64::consts::PI;

pub struct Pendulum {
    actions: Vec<f64>,

    theta_bounds: (f64, f64),
    thetadot_bounds: (f64, f64),
    theta_space: usize,
    thetadot_space: usize,

    g: f64,
    l: f64,
    m: f64,

    tau: f64,

    init_state: St,
    s: St,

    last_thetaddot: f64,
}

impl Pendulum {
    pub fn new(config: &Config) -> Result<Box<Self>, Box<dyn error::Error>> {
        let actions = vec![
            config.get("ENV_ACTION_LEFT")?.parse()?,
            config.get("ENV_ACTION_RIGHT")?.parse()?,
        ];

        let theta_bounds = (
            config.get("ENV_THETA_LEFT")?.parse()?,
            config.get("ENV_THETA_RIGHT")?.parse()?,
        );
        let thetadot_bounds = (
            config.get("ENV_THETADOT_LEFT")?.parse()?,
            config.get("ENV_THETADOT_RIGHT")?.parse()?,
        );
        let theta_space = config.get("ENV_THETA_SPACE")?.parse()?;
        let thetadot_space = config.get("ENV_THETADOT_SPACE")?.parse()?;

        let g = config.get("ENV_G")?.parse()?;
        let l = config.get("ENV_LENGTH")?.parse()?;
        let m = config.get("ENV_MASS")?.parse()?;

        let fps: u32 = config.get("ENV_FPS")?.parse()?;
        let tau = 1. / fps as f64;

        let init_state = (PI / 3., 0.);
        // let init_state = (PI, 0.);
        let s = init_state;

        let last_thetaddot = 0.;

        Ok(Box::new(Pendulum {
            actions,
            theta_bounds,
            thetadot_bounds,
            theta_space,
            thetadot_space,
            g,
            l,
            m,
            tau,
            init_state,
            s,
            last_thetaddot,
        }))
    }

    fn solve_runge_kutta(&self, s: &St, u: f64, dt: f64) -> St {
        let k1 = self.differential(s, u, dt);
        let s1 = self.solve_euler(s, &k1, dt / 2.);
        let k2 = self.differential(&s1, u, dt / 2.);
        let s2 = self.solve_euler(s, &k2, dt / 2.);
        let k3 = self.differential(&s2, u, dt / 2.);
        let s3 = self.solve_euler(s, &k3, dt);
        let k4 = self.differential(&s3, u, dt);

        let next_val = |s, k1, k2, k3, k4| s + (k1 + 2. * k2 + 2. * k3 + k4) * dt / 6.;
        let theta = next_val(s.0, k1.0, k2.0, k3.0, k4.0);
        let theta = normalize(theta);
        let thetadot = next_val(s.1, k1.1, k2.1, k3.1, k4.1);

        (theta, thetadot)
    }

    fn differential(&self, s: &St, u: f64, dt: f64) -> St {
        let (theta, thetadot) = s;

        let l = self.l;
        let g = self.g;
        let m = self.m;

        let thetadot = -g / l * theta.cos() + u * theta / (m * l * l);
        let thetaddot = g / l * theta.sin() + u / (m * l * l);

        (thetadot, thetaddot)
    }

    fn solve_euler(&self, s: &St, sdot: &St, dt: f64) -> St {
        (s.0 + sdot.0 * dt, s.1 + sdot.1 * dt)
    }
}

impl Environment for Pendulum {
    fn s_space(&self) -> usize {
        self.theta_space * self.thetadot_space
    }

    fn a_space(&self) -> usize {
        self.actions.len()
    }

    fn s(&self) -> State {
        let theta_idx = digitize(&self.theta_bounds, self.theta_space, self.s.0);
        let thetadot_idx = digitize(&self.thetadot_bounds, self.thetadot_space, self.s.1);

        theta_idx * self.thetadot_space + thetadot_idx
    }

    fn info(&self) -> String {
        let theta = self.s.0;
        let thetadot = self.s.1;
        format!("{:.15},{:.15}", theta, thetadot)
    }

    fn r(&self) -> Reward {
        let theta = self.s.0;
        -(theta.abs()) + PI / 2.
    }

    fn reset(&mut self) {
        self.s = self.init_state;
        self.last_thetaddot = 0.
    }

    fn run_step(&mut self, a: Action) {
        let u = self.actions[a];
        self.s = self.solve_runge_kutta(&self.s, u, self.tau);
    }

    fn is_done(&self) -> bool {
        false
    }

    fn is_success(&self) -> bool {
        false
    }
}

fn digitize(bounds: &(f64, f64), num: usize, val: f64) -> usize {
    if val < bounds.0 {
        0
    } else if val >= bounds.1 {
        num - 1
    } else {
        let width = (bounds.1 - bounds.0) / (num - 2) as f64;
        ((val - bounds.0) / width) as usize + 1
    }
}

type St = (f64, f64);

fn normalize(theta: f64) -> f64 {
    (theta + 3. * PI) % (2. * PI) - PI
}
