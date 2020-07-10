#include <stdlib.h>
#include <time.h>
#include "agent.h"
#include "config.h"
#include "SFMT/SFMT.h"

agent_t *new_agent_qlearning(const config_t *config)
{
    agent_params_qlearning_t *params;
    agent_t *agent;

    if ((params = new_agent_qlearning_params(config)) == NULL)
    {
        return NULL;
    }

    if ((agent = (agent_t *)malloc(sizeof(agent_t))) == NULL)
    {
        return NULL;
    }

    if ((agent->params = (agent_params_t *)malloc(sizeof(agent_params_t))) == NULL)
    {
        return NULL;
    }

    agent->type = AGENT_TYPE_QLEARNING;
    agent->params->agent_params_qlearning = params;
    agent->action = agent_qlearning_action;
    agent->learn = agent_qlearning_learn;
    agent->fix = agent_qlearning_fix;

    return agent;
}

agent_params_qlearning_t *new_agent_qlearning_params(const config_t *config)
{
    agent_params_qlearning_t *params;
    double alpha, gamma, eps;
    sfmt_t *sfmt;

    if ((params = (agent_params_qlearning_t *)malloc(sizeof(agent_params_qlearning_t))) == NULL)
    {
        return NULL;
    }

    alpha = get_config_as_double(config, "AGENT_ALPHA");
    gamma = get_config_as_double(config, "AGENT_GAMMA");
    eps = get_config_as_double(config, "AGENT_EPSILON");

    if ((sfmt = (sfmt_t *)malloc(sizeof(sfmt_t))) == NULL)
    {
        return NULL;
    }

    sfmt_init_gen_rand(sfmt, (uint32_t)time(NULL));

    params->alpha = alpha;
    params->gamma = gamma;
    params->eps = eps;
    params->sfmt = sfmt;

    return params;
}

int agent_qlearning_action(agent_params_t *agent_params, qtable_t *qtable, int s)
{
    agent_params_qlearning_t *params;

    params = agent_params->agent_params_qlearning;

    if (sfmt_genrand_real2(params->sfmt) < params->eps)
    {
        return (int)(sfmt_genrand_uint32(params->sfmt) % qtable->action_size);
    }
    return argmax(qtable->table[s], qtable->action_size);
}

void agent_qlearning_learn(
    agent_params_t *agent_params,
    qtable_t *qtable,
    int s1, int a1, double r, int s2, int a2)
{
    double max_;
    double alpha, gamma;

    alpha = agent_params->agent_params_qlearning->alpha;
    gamma = agent_params->agent_params_qlearning->gamma;

    max_ = max(qtable->table[s2], qtable->action_size);

    qtable->table[s1][a1] =
        (1.0 - alpha) * qtable->table[s1][a1] + alpha * (r + gamma * max_);
}

void agent_qlearning_fix(agent_params_t *agent_params)
{
    agent_params->agent_params_qlearning->alpha = 0.0;
    agent_params->agent_params_qlearning->eps = 0.0;
}

agent_t *new_agent_sarsa(const config_t *config)
{
    agent_params_sarsa_t *params;
    agent_t *agent;

    if ((params = new_agent_sarsa_params(config)) == NULL)
    {
        return NULL;
    }

    if ((agent = (agent_t *)malloc(sizeof(agent_t))) == NULL)
    {
        return NULL;
    }

    if ((agent->params = (agent_params_t *)malloc(sizeof(agent_params_t))) == NULL)
    {
        return NULL;
    }

    agent->type = AGENT_TYPE_SARSA;
    agent->params->agent_params_sarsa = params;
    agent->action = agent_sarsa_action;
    agent->learn = agent_sarsa_learn;
    agent->fix = agent_sarsa_fix;

    return agent;
}

agent_params_sarsa_t *new_agent_sarsa_params(const config_t *config)
{
    agent_params_sarsa_t *params;
    double alpha, gamma, eps;
    sfmt_t *sfmt;

    if ((params = (agent_params_sarsa_t *)malloc(sizeof(agent_params_sarsa_t))) == NULL)
    {
        return NULL;
    }

    alpha = get_config_as_double(config, "AGENT_ALPHA");
    gamma = get_config_as_double(config, "AGENT_GAMMA");
    eps = get_config_as_double(config, "AGENT_EPSILON");

    if ((sfmt = (sfmt_t *)malloc(sizeof(sfmt_t))) == NULL)
    {
        return NULL;
    }

    sfmt_init_gen_rand(sfmt, (uint32_t)time(NULL));

    params->alpha = alpha;
    params->gamma = gamma;
    params->eps = eps;
    params->sfmt = sfmt;

    return params;
}

int agent_sarsa_action(agent_params_t *agent_params, qtable_t *qtable, int s)
{
    agent_params_sarsa_t *params;

    params = agent_params->agent_params_sarsa;

    if (sfmt_genrand_real2(params->sfmt) < params->eps)
    {
        return (int)(sfmt_genrand_uint32(params->sfmt) % qtable->action_size);
    }
    return argmax(qtable->table[s], qtable->action_size);
}

void agent_sarsa_learn(
    agent_params_t *agent_params,
    qtable_t *qtable,
    int s1, int a1, double r, int s2, int a2)
{
    double alpha, gamma;

    alpha = agent_params->agent_params_sarsa->alpha;
    gamma = agent_params->agent_params_sarsa->gamma;

    qtable->table[s1][a1] =
        (1.0 - alpha) * qtable->table[s1][a1] + alpha * (r + gamma * qtable->table[s2][a2]);
}

void agent_sarsa_fix(agent_params_t *agent_params)
{
    agent_params->agent_params_sarsa->alpha = 0.0;
    agent_params->agent_params_sarsa->eps = 0.0;
}

double max(const double seq[], int length)
{
    double ret = seq[0];
    int i;
    for (i = 1; i < length; i++)
    {
        if (ret < seq[i])
        {
            ret = seq[i];
        }
    }
    return ret;
}

int argmax(const double seq[], int length)
{
    int ret = 0;
    int i;
    for (i = 1; i < length; i++)
    {
        if (seq[ret] < seq[i])
        {
            ret = i;
        }
    }
    return ret;
}