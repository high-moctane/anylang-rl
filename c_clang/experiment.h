#include <stdlib.h>
#include "agent.h"
#include "env.h"
#include "utils.h"

#ifndef EXPERIMENT_H
#define EXPERIMENT_H
typedef struct
{
    state_t *states;
    double *actions;
    double *rewards;
} history_t;

typedef struct
{
    agent_t *agent;
    env_t *env;
    int episodes_num, steps_num;
} experiment_t;
#endif

history_t *new_history(int);
void free_history(history_t *, int);
experiment_t *new_experiment();
double *experiment_run(experiment_t *);
history_t *experiment_test(experiment_t *);
history_t *one_episode(experiment_t *);
