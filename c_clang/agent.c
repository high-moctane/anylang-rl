#include "agent.h"

agent_t *new_agent()
{
    agent_t *agent;

    agent = (agent_t *)malloc(sizeof(agent_t));
    if (agent == NULL)
        exit(EXIT_FAILURE);

    // なんかいい方法ないかね
    agent->init_qvalue = 10000.0;
    agent->actions[0] = -10.0;
    agent->actions[1] = 10.0;

    agent->x_limits[0] = -2.0;
    agent->x_limits[1] = 2.0;
    agent->theta_limits[0] = -M_PI;
    agent->theta_limits[1] = M_PI;
    agent->xdot_limits[0] = -2.0;
    agent->xdot_limits[1] = 2.0;
    agent->thetadot_limits[0] = -10.0;
    agent->thetadot_limits[1] = 10.0;

    agent->x_num = 4;
    agent->theta_num = 90;
    agent->xdot_num = 10;
    agent->thetadot_num = 50;

    agent->x_bins = make_bins(agent->x_limits, agent->x_num);
    agent->theta_bins = make_bins(agent->theta_limits, agent->theta_num);
    agent->xdot_bins = make_bins(agent->xdot_limits, agent->xdot_num);
    agent->thetadot_bins = make_bins(agent->thetadot_limits, agent->thetadot_num);

    agent->alpha = 0.1;
    agent->gamma = 0.999;
    agent->eps = 0.1;
    agent->qtable = make_qtable(
        agent->x_num * agent->theta_num * agent->xdot_num * agent->thetadot_num,
        2,
        agent->init_qvalue);
    return agent;
}

// eps-greedy
double decide_action(agent_t *agent, state_t s)
{
    int s_idx, max_idx;

    if (((double)rand() / (double)RAND_MAX) < agent->eps)
    {
        int idx = (int)(rand() * 2.0 / (1.0 + RAND_MAX));
        return agent->actions[idx];
    }

    s_idx = s_index(agent, s);
    max_idx = argmax(agent->qtable[s_idx], 2);
    return agent->actions[max_idx];
}

void agent_learn(agent_t *agent, state_t s, double a, double r, state_t s_next)
{
    int s_idx = s_index(agent, s);
    int a_idx = find_idx(agent->actions, 2, a);
    int s_next_idx = s_index(agent, s_next);

    agent->qtable[s_idx][a_idx] =
        (1.0 - agent->alpha) * agent->qtable[s_idx][a_idx] +
        agent->alpha * (r + agent->gamma * find_max(agent->qtable[s_next_idx], 2));
    return;
}

void agent_set_test_params(agent_t *agent)
{
    agent->alpha = 0.0;
    agent->eps = 0.0;
    return;
}

double *make_bins(double limits[], int num)
{
    int i;
    double width = (limits[1] - limits[0]) / (double)(num - 2);
    double *bins;

    bins = (double *)malloc(sizeof(double) * (num - 1));
    if (bins == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < num - 1; i++)
        bins[i] = limits[0] + width * i;

    return bins;
}

double **make_qtable(int s_num, int a_num, double init_qvalue)
{
    int i, j;
    double **qtable;
    qtable = (double **)malloc(sizeof(double *) * s_num);
    if (qtable == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < s_num; i++)
    {
        qtable[i] = (double *)malloc(sizeof(double) * a_num);
        if (qtable[i] == NULL)
            exit(EXIT_FAILURE);

        for (j = 0; j < a_num; j++)
        {
            qtable[i][j] = init_qvalue;
        }
    }
    return qtable;
}

int digitize(double *bins, int bins_len, double x)
{
    int i;
    for (i = 0; i < bins_len; i++)
    {
        if (x < bins[i])
            return i;
    }
    return bins_len;
}

int s_index(agent_t *agent, state_t s)
{
    int x_idx = digitize(agent->x_bins, agent->x_num - 1, s[0]);
    int theta_idx = digitize(agent->theta_bins, agent->theta_num - 1, s[1]);
    int xdot_idx = digitize(agent->xdot_bins, agent->xdot_num - 1, s[2]);
    int thetadot_idx = digitize(agent->thetadot_bins, agent->thetadot_num - 1, s[3]);
    return x_idx + agent->x_num * (theta_idx + agent->theta_num * (xdot_idx + agent->xdot_num * thetadot_idx));
}

int argmax(double doubles[], int len)
{
    int i;
    int idx = 0;
    double max_val = doubles[0];
    for (i = 0; i < len; i++)
    {
        if (doubles[i] > max_val)
        {
            idx = i;
            max_val = doubles[i];
        }
    }
    return idx;
}

int find_idx(double doubles[], int len, double x)
{
    int i;
    for (i = 0; i < len; i++)
    {
        if (x == doubles[i])
        {
            return i;
        }
    }
    // めんどくさいので強制終了
    exit(EXIT_FAILURE);
    return 0;
}

double find_max(double doubles[], int len)
{
    int i;
    double max = doubles[0];
    for (i = 0; i < len; i++)
    {
        if (doubles[i] > max)
        {
            max = doubles[i];
        }
    }
    return max;
}