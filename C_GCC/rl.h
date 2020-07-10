#include "agent.h"
#include "environment.h"
#include "history.h"
#include "qtable.h"

#ifndef RL_H
#define RL_H

typedef struct
{
    char *returns_path;
    char *test_history_path;

    int max_episode;
    int max_step;

    agent_t *agent;
    env_t *env;
    qtable_t *qtable;

    double *returns;
    history_t *test_history;
} rl_t;

#endif

rl_t *new_rl(config_t *config);

agent_t *rl_choose_agent(const config_t *config);

env_t *rl_choose_env(const config_t *config);

int rl_run(rl_t *rl);

history_t *rl_run_episode(rl_t *rl);

int rl_run_test(rl_t *rl);

int rl_save_returns(rl_t *rl);

int rl_save_test_history(rl_t *rl);
