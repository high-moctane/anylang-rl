#include "env.h"

env_t *new_env()
{
    env_t *env;
    env = (env_t *)malloc(sizeof(env_t));
    if (env == NULL)
        exit(EXIT_FAILURE);

    env->g = 9.80665;
    env->M = 1.0;
    env->m = 0.1;
    env->l = 0.5;
    env->ml = env->m * env->l;
    env->mass = env->M + env->m;
    env->fps = 50;
    env->tau = 1.0 / (double)(env->fps);
    env->s = initial_state();
    return env;
}

state_t initial_state()
{
    state_t s;
    s = (state_t)malloc(sizeof(double) * 4);
    if (s == NULL)
        exit(EXIT_FAILURE);
    s[0] = 0.0;
    s[1] = -M_PI;
    s[2] = 0.0;
    s[3] = 0.0;
    return s;
}

void reset_env(env_t *env)
{
    state_t s = initial_state();
    env->s = s;
    return;
}

double get_reward(env_t *env)
{
    double x = env->s[0];
    double theta = env->s[1];
    if (fabs(x) > 2.0)
        return -2.0;

    return -fabs(theta) + M_PI_2;
}

void run_step(env_t *env, double a)
{
    state_t s_next;
    s_next = runge_kutta_solve(env, env->s, a, env->tau);
    env->s = s_next;
    return;
}

// 状態 s で力 u を加えたときの微分
state_t differential(env_t *env, state_t s, double u)
{
    double theta = s[1];
    double xdot = s[2];
    double thetadot = s[3];

    double sintheta = sin(theta);
    double costheta = cos(theta);

    double xddot =
        (4.0 * u / 3.0 + 4.0 * env->ml * pow(thetadot, 2.0) * sintheta / 3.0 - env->m * env->g * sin(2.0 * theta) / 2.0) /
        (4.0 * env->mass - env->m * pow(costheta, 2.0));
    double thetaddot =
        (env->mass * env->g * sintheta - env->ml * pow(thetadot, 2.0) * sintheta * costheta - u * costheta) /
        (4.0 * env->mass * env->l / 3.0 - env->ml * pow(costheta, 2.0));

    state_t sdot;
    sdot = (state_t)malloc(sizeof(double) * 4);
    if (sdot == NULL)
        exit(EXIT_FAILURE);
    sdot[0] = xdot;
    sdot[1] = thetadot;
    sdot[2] = xddot;
    sdot[3] = thetaddot;
    return sdot;
}

// オイラー法で微分方程式を解く
state_t euler_solve(state_t s, state_t sdot, double dt)
{
    int i;
    state_t ret;

    ret = (state_t)malloc(sizeof(double) * 4);
    for (i = 0; i < 4; i++)
        ret[i] = s[i] + sdot[i] * dt;
    return ret;
}

// ルンゲクッタ法で微分方程式を解く
state_t runge_kutta_solve(env_t *env, state_t s, double u, double dt)
{
    int i;
    double *k1, *k2, *k3, *k4, *s1, *s2, *s3;
    state_t s_next;

    k1 = differential(env, s, u);
    s1 = euler_solve(s, k1, dt / 2.0);
    k2 = differential(env, s1, u);
    s2 = euler_solve(s, k2, dt / 2.0);
    k3 = differential(env, s2, u);
    s3 = euler_solve(s, k3, dt);
    k4 = differential(env, s3, u);

    s_next = (state_t)malloc(sizeof(double) * 4);
    for (i = 0; i < 4; i++)
        s_next[i] = s[i] + (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) * dt / 6.0;
    s_next[1] = fmod(s_next[1] + 3.0 * M_PI, 2.0 * M_PI) - M_PI;

    free(k1);
    free(k2);
    free(k3);
    free(k4);
    free(s1);
    free(s2);
    free(s3);

    return s_next;
}