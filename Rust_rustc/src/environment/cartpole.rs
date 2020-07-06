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

    x_size: usize,
    theta_size: usize,
    xdot_size: usize,
    thetadot_size: usize,

    g: f64,
    m: f64,
    l: f64,
    ml: f64,
    mass: f64,

    tau: f64,

    init_state: CartpoleState,
    s: CartpoleState,
}

impl Cartpole {
    pub fn new(config: &Config) -> Result<Cartpole, Box<dyn error::Error>> {
        let actions = vec![
            config.get("ENVIRONMENT_ACTION_LEFT")?.parse()?,
            config.get("ENVIRONMENT_ACTION_RIGHT")?.parse()?,
        ];

        let x_bounds = [
            config.get("ENVIRONMENT_X_LEFT")?.parse()?,
            config.get("ENVIRONMENT_X_RIGHT")?.parse()?,
        ];
        let theta_bounds = [
            config.get("ENVIRONMENT_THETA_LEFT")?.parse()?,
            config.get("ENVIRONMENT_THETA_RIGHT")?.parse()?,
        ];
        let xdot_bounds = [
            config.get("ENVIRONMENT_XDOT_LEFT")?.parse()?,
            config.get("ENVIRONMENT_XDOT_RIGHT")?.parse()?,
        ];
        let thetadot_bounds = [
            config.get("ENVIRONMENT_THETADOT_LEFT")?.parse()?,
            config.get("ENVIRONMENT_THETADOT_RIGHT")?.parse()?,
        ];

        let x_size = config.get("ENVIRONMENT_X_SIZE")?.parse()?;
        let theta_size = config.get("ENVIRONMENT_THETA_SIZE")?.parse()?;
        let xdot_size = config.get("ENVIRONMENT_XDOT_SIZE")?.parse()?;
        let thetadot_size = config.get("ENVIRONMENT_THETADOT_SIZE")?.parse()?;

        let g = config.get("ENVIRONMENT_GRAVITY")?.parse()?;
        let cartmass: f64 = config.get("ENVIRONMENT_CART_MASS")?.parse()?;
        let m = config.get("ENVIRONMENT_POLE_MASS")?.parse()?;
        let l = config.get("ENVIRONMENT_POLE_LENGTH")?.parse()?;
        let ml = m * l;
        let mass = cartmass + m;

        let fps: u32 = config.get("ENVIRONMENT_FRAME_PER_SECOND")?.parse()?;
        let tau = 1. / fps as f64;

        let init_state = [0., PI, 0., 0.];
        // let init_state = (PI, 0.);
        let s = init_state.clone();

        Ok(Cartpole {
            actions,
            x_bounds,
            theta_bounds,
            xdot_bounds,
            thetadot_bounds,
            x_size,
            theta_size,
            xdot_size,
            thetadot_size,
            g,
            m,
            l,
            ml,
            mass,
            tau,
            init_state,
            s,
        })
    }

    fn solve_runge_kutta(&self, s: &CartpoleState, u: f64, dt: f64) -> CartpoleState {
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

    fn differential(&self, s: &CartpoleState, u: f64) -> CartpoleState {
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

    fn solve_euler(&self, s: &CartpoleState, sdot: &CartpoleState, dt: f64) -> CartpoleState {
        let mut res = s.clone();
        for i in 0..s.len() {
            res[i] += sdot[i] * dt
        }
        res
    }
}

impl Environment for Cartpole {
    fn state_size(&self) -> usize {
        self.x_size * self.theta_size * self.xdot_size * self.thetadot_size
    }

    fn action_size(&self) -> usize {
        self.actions.len()
    }

    fn state(&self) -> State {
        let x_idx = digitize(&self.x_bounds, self.x_size, self.s[0]);
        let theta_idx = digitize(&self.theta_bounds, self.theta_size, self.s[1]);
        let xdot_idx = digitize(&self.xdot_bounds, self.xdot_size, self.s[2]);
        let thetadot_idx = digitize(&self.thetadot_bounds, self.thetadot_size, self.s[3]);

        ((x_idx * self.theta_size + theta_idx) * self.xdot_size + xdot_idx) * self.thetadot_size
            + thetadot_idx
    }

    fn info(&self) -> String {
        let [x, theta, xdot, thetadot] = self.s;
        format!("{:.15},{:.15},{:.15},{:.15}", x, theta, xdot, thetadot)
    }

    fn reward(&self) -> Reward {
        let [x, theta, ..] = self.s;
        if x.abs() > 2. {
            -2.
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

    fn is_finish(&self) -> bool {
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

type CartpoleState = [f64; 4];

fn normalize(theta: f64) -> f64 {
    (theta + 3. * PI) % (2. * PI) - PI
}
