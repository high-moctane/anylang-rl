#include <math.h>
#include <stdlib.h>
#include "utils.h"

#ifndef ENV_H
#define ENV_H
typedef struct
{
    double g;        // 重力加速度
    double M;        // カートの質量
    double m;        // ポールの質量
    double l;        // ポールの半分の長さ
    double ml, mass; //あとの計算で使う
    int fps;         //frames per second
    double tau;      // 制御周期
    state_t s;       // 状態
} env_t;
#endif

env_t *new_env();
state_t initial_state();
void reset_env(env_t *);
double get_reward(env_t *);
void run_step(env_t *, double);
state_t differential(env_t *, state_t, double);
state_t euler_solve(state_t, state_t, double);
state_t runge_kutta_solve(env_t *, state_t, double, double);
