#include "main.h"

int main(void)
{
    experiment_t *exp;
    double *returns;
    history_t *history;

    srand((unsigned)time(NULL));

    exp = new_experiment();
    returns = experiment_run(exp);
    history = experiment_test(exp);

    save_returns(returns, exp->episodes_num);
    save_states(history->states, exp->steps_num);
    save_actions(history->actions, exp->steps_num);
    save_rewards(history->rewards, exp->steps_num);

    return EXIT_SUCCESS;
}

void save_returns(double *returns, int len)
{
    int i;
    char buf[1024];
    FILE *fp;

    fp = fopen("returns.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < len; i++)
    {
        snprintf(buf, sizeof(buf), "%f\n", returns[i]);
        fputs(buf, fp);
    }

    fclose(fp);
    return;
}

void save_states(state_t *states, int len)
{
    int i;
    char buf[1024];
    FILE *fp;

    fp = fopen("states.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < len; i++)
    {
        snprintf(buf, sizeof(buf), "%f,%f,%f,%f\n", states[i][0], states[i][1], states[i][2], states[i][3]);
        fputs(buf, fp);
    }

    fclose(fp);
    return;
}

void save_actions(double *actions, int len)
{
    int i;
    char buf[1024];
    FILE *fp;

    fp = fopen("actions.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < len; i++)
    {
        snprintf(buf, sizeof(buf), "%f\n", actions[i]);
        fputs(buf, fp);
    }

    fclose(fp);
    return;
}

void save_rewards(double *rewards, int len)
{
    int i;
    char buf[1024];
    FILE *fp;

    fp = fopen("rewards.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    for (i = 0; i < len; i++)
    {
        snprintf(buf, sizeof(buf), "%f\n", rewards[i]);
        fputs(buf, fp);
    }

    fclose(fp);
    return;
}
