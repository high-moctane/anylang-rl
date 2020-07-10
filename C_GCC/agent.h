#include "config.h"
#include "qtable.h"
#include "SFMT/SFMT.h"

#define AGENT_TYPE_QLEARNING 0
#define AGENT_TYPE_SARSA 1

#ifndef AGENT_H
#define AGENT_H

typedef struct
{
    double alpha;
    double gamma;
    double eps;
    sfmt_t *sfmt;
} agent_params_qlearning_t;

typedef struct
{
    double alpha;
    double gamma;
    double eps;
    sfmt_t *sfmt;
} agent_params_sarsa_t;

typedef union {
    agent_params_qlearning_t *agent_params_qlearning;
    agent_params_sarsa_t *agent_params_sarsa;
} agent_params_t;

typedef struct
{
    int type;
    agent_params_t *params;
    int (*action)(agent_params_t *agent_params, qtable_t *qtable, int s);
    void (*learn)(agent_params_t *agent_params, qtable_t *qtable, int s1, int a1, double r, int s2, int a2);
    void (*fix)(agent_params_t *agent_params);
} agent_t;

#endif

agent_t *new_agent_qlearning(const config_t *config);

agent_params_qlearning_t *new_agent_qlearning_params(const config_t *config);

int agent_qlearning_action(agent_params_t *agent_params, qtable_t *qtable, int s);

void agent_qlearning_learn(agent_params_t *agent_params,
                           qtable_t *qtable,
                           int s1, int a1, double r, int s2, int a2);

void agent_qlearning_fix(agent_params_t *agent_params);

agent_t *new_agent_sarsa(const config_t *config);

agent_params_sarsa_t *new_agent_sarsa_params(const config_t *config);

int agent_sarsa_action(agent_params_t *agent_params, qtable_t *qtable, int s);

void agent_sarsa_learn(
    agent_params_t *agent_params,
    qtable_t *qtable,
    int s1, int a1, double r, int s2, int a2);

void agent_sarsa_fix(agent_params_t *agent_params);

double max(const double seq[], int length);

int argmax(const double seq[], int length);
