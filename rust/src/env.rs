use std::f64::consts::PI;

const G: f64 = 9.80665; // 重力加速度
const MCART: f64 = 1.0; // カートの質量
const MPOLE: f64 = 0.1; // ポールの質量
const L: f64 = 0.5; // ポールの半分の長さ
pub const FPS: u32 = 50; // frames per second
const TAU: f64 = 1.0 / FPS as f64; // 制御周期

// あとの計算でつかう
const ML: f64 = MPOLE * L;
const MASS: f64 = MCART + MPOLE;

const STATE_LEN: usize = 4; // 状態ベクトルの長さ

pub type State = [f64; 4];
pub type Action = f64;
pub type Reward = f64;

pub fn new_state() -> State {
    // [x, theta, xdot, thetadot]
    [0.0, -PI, 0.0, 0.0]
}

pub fn step(s: &State, a: Action) -> State {
    runge_kutta_solve(s, a, TAU)
}

pub fn reward(s: &State) -> Reward {
    let [x, theta, _, _] = s;
    if x.abs() > 2.0 {
        return -2.0;
    }
    -theta.abs() + PI / 2.0
}

/// 状態 s で力 u を加えたときの微分
fn differential(s: &State, u: Action) -> State {
    let [_x, theta, xdot, thetadot] = s;
    let sintheta = theta.sin();
    let costheta = theta.cos();

    let xddot = (4.0 * u / 3.0 + 4.0 * ML * thetadot.powf(2.0) * sintheta / 3.0
        - MPOLE * G * (2.0 * theta).sin() / 2.0)
        / (4.0 * MASS - MPOLE * costheta.powf(2.0));
    let thetaddot =
        (MASS * G * sintheta - ML * thetadot.powf(2.0) * sintheta * costheta - u * costheta)
            / (4.0 * MASS * L / 3.0 - ML * costheta.powf(2.0));

    [*xdot, *thetadot, xddot, thetaddot]
}

/// オイラー法を用いて微分方程式を解く
fn euler_solve(s: &State, sdot: &State, dt: f64) -> State {
    let mut ans = [0.0; STATE_LEN];
    for i in 0..STATE_LEN {
        ans[i] = s[i] + sdot[i] * dt;
    }
    ans
}

fn runge_kutta_solve(s: &State, u: Action, dt: f64) -> State {
    let k1 = differential(s, u);
    let s1 = euler_solve(s, &k1, dt / 2.0);
    let k2 = differential(&s1, u);
    let s2 = euler_solve(s, &k2, dt / 2.0);
    let k3 = differential(&s2, u);
    let s3 = euler_solve(s, &k3, dt);
    let k4 = differential(&s3, u);

    let mut snext = [0.0; STATE_LEN];
    for i in 0..STATE_LEN {
        snext[i] = s[i] + (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) * dt / 6.0;
    }

    snext[1] = (snext[1] + 3.0 * PI) % (2.0 * PI) - PI;
    snext
}
