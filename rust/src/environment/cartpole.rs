use crate::config::Config;
use crate::environment::Environment;
use crate::{Action, Reward, State};
use std::error;
use std::f64::consts::PI;

pub struct Cartpole {
    actions: Vec<f64>,

    x_bounds: [f64; 2],
    theta_bounds: [f64; 2],
    xdot_bounds: [f64; 2],
    thetadot_bounds: [f64; 2],

    x_space: usize,
    theta_space: usize,
    xdot_space: usize,
    thetadot_space: usize,

    g: f64,
    m: f64,
    l: f64,
    ml: f64,
    mass: f64,

    tau: f64,

    init_state: SVar,
    s: SVar,
}

impl Cartpole {
    pub fn new(config: &Config) -> Result<Box<Self>, Box<dyn error::Error>> {
        let actions = vec![
            config.get("ENV_ACTION_LEFT")?.parse()?,
            config.get("ENV_ACTION_RIGHT")?.parse()?,
        ];

        let x_bounds = [
            config.get("ENV_X_LEFT")?.parse()?,
            config.get("ENV_X_RIGHT")?.parse()?,
        ];
        let theta_bounds = [
            config.get("ENV_THETA_LEFT")?.parse()?,
            config.get("ENV_THETA_RIGHT")?.parse()?,
        ];
        let xdot_bounds = [
            config.get("ENV_XDOT_LEFT")?.parse()?,
            config.get("ENV_XDOT_RIGHT")?.parse()?,
        ];
        let thetadot_bounds = [
            config.get("ENV_THETADOT_LEFT")?.parse()?,
            config.get("ENV_THETADOT_RIGHT")?.parse()?,
        ];

        let x_space = config.get("ENV_X_SPACE")?.parse()?;
        let theta_space = config.get("ENV_THETA_SPACE")?.parse()?;
        let xdot_space = config.get("ENV_XDOT_SPACE")?.parse()?;
        let thetadot_space = config.get("ENV_THETADOT_SPACE")?.parse()?;

        let g = config.get("ENV_G")?.parse()?;
        let cartmass: f64 = config.get("ENV_CART_MASS")?.parse()?;
        let m = config.get("ENV_POLE_MASS")?.parse()?;
        let l = config.get("ENV_POLE_LENGTH")?.parse()?;
        let ml = m * l;
        let mass = cartmass + m;

        let fps: u32 = config.get("ENV_FPS")?.parse()?;
        let tau = 1. / fps as f64;

        let init_state = [0., PI, 0., 0.];
        // let init_state = (PI, 0.);
        let s = init_state.clone();

        Ok(Box::new(Cartpole {
            actions,
            x_bounds,
            theta_bounds,
            xdot_bounds,
            thetadot_bounds,
            x_space,
            theta_space,
            xdot_space,
            thetadot_space,
            g,
            m,
            l,
            ml,
            mass,
            tau,
            init_state,
            s,
        }))
    }

    fn solve_runge_kutta(&self, s: &SVar, u: f64, dt: f64) -> SVar {
        let k1 = self.differential(s, u);
        let s1 = self.solve_euler(s, &k1, dt / 2.);
        let k2 = self.differential(&s1, u);
        let s2 = self.solve_euler(s, &k2, dt / 2.);
        let k3 = self.differential(&s2, u);
        let s3 = self.solve_euler(s, &k3, dt);
        let k4 = self.differential(&s3, u);

        let mut snext = s.clone();
        for i in 0..s.len() {
            snext[i] += (k1[i] + 2. * k2[i] + 2. * k3[i] + k4[i]) * dt / 6.;
        }
        snext[1] = normalize(snext[1]);

        snext
    }

    fn differential(&self, s: &SVar, u: f64) -> SVar {
        let [_, theta, xdot, thetadot] = *s;

        let sintheta = theta.sin();
        let costheta = theta.cos();

        let l = self.l;
        let g = self.g;
        let m = self.m;
        let ml = self.ml;
        let mass = self.mass;

        let xddot = (4. * u / 3. + 4. * ml * thetadot.powi(2) * sintheta / 3.
            - m * g * (2. * theta).sin() / 2.)
            / (4. * mass - m * costheta.powi(2));
        let thetaddot =
            (mass * g * sintheta - ml * thetadot.powi(2) * sintheta * costheta - u * costheta)
                / (4. * mass * l / 3. - ml * costheta.powi(2));

        [xdot, thetadot, xddot, thetaddot]
    }

    fn solve_euler(&self, s: &SVar, sdot: &SVar, dt: f64) -> SVar {
        let mut res = s.clone();
        for i in 0..s.len() {
            res[i] += sdot[i] * dt
        }
        res
    }
}

impl Environment for Cartpole {
    fn s_space(&self) -> usize {
        self.x_space * self.theta_space * self.xdot_space * self.thetadot_space
    }

    fn a_space(&self) -> usize {
        self.actions.len()
    }

    fn s(&self) -> State {
        let x_idx = digitize(&self.x_bounds, self.x_space, self.s[0]);
        let theta_idx = digitize(&self.theta_bounds, self.theta_space, self.s[1]);
        let xdot_idx = digitize(&self.xdot_bounds, self.xdot_space, self.s[2]);
        let thetadot_idx = digitize(&self.thetadot_bounds, self.thetadot_space, self.s[3]);

        ((x_idx * self.theta_space + theta_idx) * self.xdot_space + xdot_idx) * self.thetadot_space
            + thetadot_idx
    }

    fn info(&self) -> String {
        let [x, theta, xdot, thetadot] = self.s;
        format!("{:.15},{:.15},{:.15},{:.15}", x, theta, xdot, thetadot)
    }

    fn r(&self) -> Reward {
        let [x, theta, ..] = self.s;
        if x.abs() > 2. {
            -100.
        } else {
            -(theta.abs()) + PI / 2. - 0.01 * x.abs()
        }
    }

    fn reset(&mut self) {
        self.s = self.init_state.clone();
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

fn digitize(bounds: &[f64; 2], num: usize, val: f64) -> usize {
    if val < bounds[0] {
        0
    } else if val >= bounds[1] {
        num - 1
    } else {
        let width = (bounds[1] - bounds[0]) / (num - 2) as f64;
        ((val - bounds[0]) / width) as usize + 1
    }
}

type SVar = [f64; 4];

fn normalize(theta: f64) -> f64 {
    (theta + 3. * PI) % (2. * PI) - PI
}
