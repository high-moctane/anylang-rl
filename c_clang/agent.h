#include <math.h>
#include <stdlib.h>
#include "utils.h"

#ifndef AGENT_H
#define AGENT_H
typedef struct
{
    double init_qvalue;
    double actions[2]; // 行動の候補

    // 状態分割の下限と上限
    double x_limits[2];
    double theta_limits[2];
    double xdot_limits[2];
    double thetadot_limits[2];

    // 状態の分割数
    int x_num, theta_num, xdot_num, thetadot_num;

    // 状態分割の bins
    double *x_bins, *theta_bins, *xdot_bins, *thetadot_bins;

    // 学習に使うパラメータ
    double alpha; //学習率
    double gamma; // 割引率
    double eps;   // ランダムに行動選択する割合

    // 多次元の配列を確保するのはたいへんつらい...
    double **qtable;
} agent_t;
#endif

agent_t *new_agent();
double decide_action(agent_t *, state_t);
void agent_learn(agent_t *, state_t, double, double, state_t);
void agent_set_test_params(agent_t *);
double *make_bins(double[], int);
double **make_qtable(int, int, double);
int digitize(double *, int, double);
int s_index(agent_t *, state_t);
int argmax(double[], int);
int find_idx(double[], int, double);
double find_max(double[], int);