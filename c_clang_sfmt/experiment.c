#include "experiment.h"

history_t *new_history(int steps_num)
{
    state_t *states;
    double *actions, *rewards;
    history_t *history;

    states = (state_t *)malloc(sizeof(state_t) * steps_num);
    if (states == NULL)
        exit(EXIT_FAILURE);

    actions = (double *)malloc(sizeof(double) * steps_num);
    if (actions == NULL)
        exit(EXIT_FAILURE);

    rewards = (double *)malloc(sizeof(double) * steps_num);
    if (rewards == NULL)
        exit(EXIT_FAILURE);

    history = (history_t *)malloc(sizeof(history_t));
    if (history == NULL)
        exit(EXIT_FAILURE);

    history->states = states;
    history->actions = actions;
    history->rewards = rewards;
    return history;
}

void free_history(history_t *history, int steps_num)
{
    int i;
    for (i = 0; i < steps_num; i++)
    {
        free(history->states[i]);
    }
    free(history->states);
    free(history->actions);
    free(history->rewards);
    free(history);
}

experiment_t *new_experiment(sfmt_t *sfmt)
{
    experiment_t *exp = (experiment_t *)malloc(sizeof(experiment_t));
    if (exp == NULL)
        exit(EXIT_FAILURE);

    exp->agent = new_agent(sfmt);
    exp->env = new_env();
    exp->episodes_num = 20000000;
    exp->steps_num = exp->env->fps * 10;
    return exp;
}

double *experiment_run(experiment_t *exp)
{
    double *returns;
    int i;
    int episode;
    history_t *hist;

    returns = (double *)malloc(sizeof(double) * exp->episodes_num);
    if (returns == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < exp->episodes_num; i++)
        returns[i] = 0.0;

    for (episode = 0; episode < exp->episodes_num; episode++)
    {
        hist = one_episode(exp);
        for (i = 0; i < exp->steps_num; i++)
        {
            returns[episode] += hist->rewards[i];
        }
        free_history(hist, exp->steps_num);
    }

    return returns;
}

history_t *experiment_test(experiment_t *exp)
{
    agent_set_test_params(exp->agent);
    return one_episode(exp);
}

history_t *one_episode(experiment_t *exp)
{
    int step;
    state_t s_next;

    history_t *hist = new_history(exp->steps_num);

    state_t s;
    double a = 0.0;
    double r = 0.0;

    reset_env(exp->env);
    s = exp->env->s;

    for (step = 0; step < exp->steps_num; step++)
    {
        hist->states[step] = s;
        hist->actions[step] = a;
        hist->rewards[step] = r;

        a = decide_action(exp->agent, s);
        run_step(exp->env, a);
        s_next = exp->env->s;
        r = get_reward(exp->env);
        agent_learn(exp->agent, s, a, r, s_next);

        s = s_next;
    }

    // これで十分だよね？？？
    free(s_next);

    return hist;
}