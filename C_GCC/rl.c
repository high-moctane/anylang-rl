#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "config.h"
#include "main.h"
#include "qtable.h"
#include "rl.h"

rl_t *new_rl(config_t *config)
{
    rl_t *rl;
    double init_qvalue;
    int i;

    if ((rl = (rl_t *)malloc(sizeof(rl_t))) == NULL)
    {
        return NULL;
    }

    if ((rl->returns_path = get_config(config, "RL_RETURNS_PATH")) == NULL)
    {
        return NULL;
    }
    if ((rl->test_history_path = get_config(config, "RL_TEST_HISTORY_PATH")) == NULL)
    {
        return NULL;
    }

    rl->max_episode = get_config_as_int(config, "RL_MAX_EPISODE");
    rl->max_step = get_config_as_int(config, "RL_MAX_STEP");

    if ((rl->agent = rl_choose_agent(config)) == NULL)
    {
        return NULL;
    }
    if ((rl->env = rl_choose_env(config)) == NULL)
    {
        return NULL;
    }

    init_qvalue = get_config_as_double(config, "QTABLE_INITIAL_QVALUE");
    rl->qtable = new_qtable(
        rl->env->state_size(rl->env->params),
        rl->env->action_size(rl->env->params),
        init_qvalue);

    if ((rl->returns = (double *)malloc(sizeof(double) * rl->max_episode)) == NULL)
    {
        return NULL;
    }

    rl->test_history = NULL;

    return rl;
}

agent_t *rl_choose_agent(const config_t *config)
{
    char *name;

    if ((name = get_config(config, "AGENT_NAME")) == NULL)
    {
        return NULL;
    }
    if (strcmp(name, "Q-learning") == 0)
    {
        return new_agent_qlearning(config);
    }
    else if (strcmp(name, "Sarsa") == 0)
    {
        return new_agent_sarsa(config);
    }

    return NULL;
}

env_t *rl_choose_env(const config_t *config)
{
    char *name;

    if ((name = get_config(config, "ENV_NAME")) == NULL)
    {
        return NULL;
    }

    if (strcmp(name, "Maze") == 0)
    {
        return new_env_maze(config);
    }
    else if (strcmp(name, "Cartpole") == 0)
    {
        return new_env_cartpole(config);
    }

    return NULL;
}

int rl_run(rl_t *rl)
{
    history_t *history;
    double returns;
    int i, j;

    for (i = 0; i < rl->max_episode; i++)
    {
        if ((history = rl_run_episode(rl)) == NULL)
        {
            return FALSE;
        }

        returns = 0.0;
        for (j = 0; j < history->length; j++)
        {
            returns += history->entries[j]->reward;
        }
        rl->returns[i] = returns;
        history_free(history);
    }

    for (i = 0; i < rl->max_episode; i++)
    {
        rl->returns[i] = returns;
    }

    return TRUE;
}

history_t *rl_run_episode(rl_t *rl)
{
    history_t *history;
    int s1, a1, s2, a2;
    double r;
    char *info;
    int i, j;

    if ((history = new_history()) == NULL)
    {
        return NULL;
    }

    rl->env->reset(rl->env->params);

    s1 = rl->env->state(rl->env->params);
    s2 = s1;
    info = rl->env->info(rl->env->params);
    r = rl->env->reward(rl->env->params);
    a1 = rl->agent->action(rl->agent->params, rl->qtable, s1);

    history_push(history, a1, r, s2, info);

    for (i = 0; i < rl->max_step; i++)
    {
        rl->env->run_step(rl->env->params, a1);
        s2 = rl->env->state(rl->env->params);
        r = rl->env->reward(rl->env->params);
        info = rl->env->info(rl->env->params);
        a2 = rl->agent->action(rl->agent->params, rl->qtable, s2);

        history_push(history, a1, r, s2, info);

        if (rl->env->is_finish(rl->env->params))
        {
            for (j = 0; j < rl->qtable->action_size; j++)
            {
                rl->qtable->table[s2][j] = 0.0;
            }
        }
        rl->agent->learn(rl->agent->params, rl->qtable,
                         s1, a1, r, s2, a2);

        if (rl->env->is_finish(rl->env->params))
        {
            break;
        }

        s1 = s2;
        a1 = a2;
    }

    return history;
}

int rl_run_test(rl_t *rl)
{
    rl->agent->fix(rl->agent->params);
    if ((rl->test_history = rl_run_episode(rl)) == NULL)
    {
        return FALSE;
    }
    return TRUE;
}

int rl_save_returns(rl_t *rl)
{
    FILE *fp;
    int i;

    if ((fp = fopen(rl->returns_path, "w")) == NULL)
    {
        return FALSE;
    }

    for (i = 0; i < rl->max_episode; i++)
    {
        if (!fprintf(fp, "%.15lf\n", rl->returns[i]))
        {
            fclose(fp);
            return FALSE;
        }
    }

    fclose(fp);
    return TRUE;
}

int rl_save_test_history(rl_t *rl)
{
    return history_save(rl->test_history, rl->test_history_path);
}