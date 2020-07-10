#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "config.h"
#include "environment.h"
#include "main.h"

env_t *new_env_maze(const config_t *config)
{
    env_maze_params_t *params;
    env_t *env;

    if ((params = new_env_maze_params(config)) == NULL)
    {
        return NULL;
    }

    if ((env = (env_t *)malloc(sizeof(env_t))) == NULL)
    {
        return NULL;
    }

    if ((env->params = (env_params_t *)malloc(sizeof(env_params_t))) == NULL)
    {
        return NULL;
    }

    env->type = ENV_TYPE_MAZE;
    env->params->env_params_maze = params;
    env->state_size = env_maze_state_size;
    env->action_size = env_maze_action_size;
    env->state = env_maze_state;
    env->reward = env_maze_reward;
    env->info = env_maze_info;
    env->run_step = env_maze_run_step;
    env->reset = env_maze_reset;
    env->is_finish = env_maze_is_finish;

    return env;
}

env_maze_params_t *new_env_maze_params(const config_t *config)
{
    env_maze_params_t *params;
    char **maze;
    char *maze_path;
    int height, width;
    double default_reward, goal_reward, wall_reward;

    if ((maze_path = get_config(config, "ENV_MAZE_PATH")) == NULL)
    {
        return NULL;
    }

    if ((maze = (char **)malloc(sizeof(char *) * MAX_MAZE_HEIGHT)) == NULL)
    {
        return NULL;
    }

    if (!env_maze_parse_maze(maze_path, maze, &height, &width))
    {
        return NULL;
    }

    default_reward = get_config_as_double(config, "ENV_DEFAULT_REWARD");
    goal_reward = get_config_as_double(config, "ENV_GOAL_REWARD");
    wall_reward = get_config_as_double(config, "ENV_WALL_REWARD");

    if ((params = (env_maze_params_t *)malloc(sizeof(env_maze_params_t))) == NULL)
    {
        return NULL;
    }

    params->maze = maze;
    params->height = height;
    params->width = width;
    params->default_reward = default_reward;
    params->goal_reward = goal_reward;
    params->wall_reward = wall_reward;
    params->init_pos = new_env_maze_pos(1, 1);
    params->goal_pos = new_env_maze_pos(height - 2, width - 2);
    params->pos = new_env_maze_pos(params->init_pos->h, params->init_pos->w);

    return params;
}

int env_maze_parse_maze(const char maze_path[], char **maze, int *height, int *width)
{
    FILE *fp;
    char line[MAX_MAZE_WIDTH];
    int i;

    *height = *width = 0;

    if ((fp = fopen(maze_path, "r")) == NULL)
    {
        return FALSE;
    }

    while (fgets(line, MAX_MAZE_WIDTH, fp) != NULL)
    {
        if ((maze[*height] = (char *)malloc(sizeof(char) * (MAX_MAZE_WIDTH))) == NULL)
        {
            fclose(fp);
            return FALSE;
        }

        for (i = 0; i < MAX_MAZE_WIDTH; i++)
        {
            if (line[i] == '\n')
            {
                line[i] = '\0';
                break;
            }
        }

        strcpy(maze[*height], line);

        (*height)++;
    }

    *width = strlen(maze[0]);

    fclose(fp);
    return TRUE;
}

int env_maze_state_size(env_params_t *env_params)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    return params->height * params->width;
}

int env_maze_action_size(env_params_t *env_params)
{
    return 4;
}

int env_maze_state(env_params_t *env_params)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    return env_maze_pos_to_s(params, params->pos);
}

int env_maze_pos_to_s(env_maze_params_t *params, env_maze_pos_t *pos)
{
    return pos->h * params->width + pos->w;
}

double env_maze_reward(env_params_t *env_params)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    if (env_maze_is_wall(params))
    {
        return params->wall_reward;
    }
    else if (env_maze_is_goal(params))
    {
        return params->goal_reward;
    }
    return params->default_reward;
}

int env_maze_is_wall(env_maze_params_t *params)
{
    env_maze_pos_t *pos;

    pos = params->pos;

    return params->maze[pos->h][pos->w] == '#';
}

int env_maze_is_goal(env_maze_params_t *params)
{
    return env_maze_is_equall_pos(params->pos, params->goal_pos);
}

int env_maze_is_equall_pos(env_maze_pos_t *pos1, env_maze_pos_t *pos2)
{
    return pos1->h == pos2->h && pos1->w == pos2->w;
}

char *env_maze_info(env_params_t *env_params)
{
    env_maze_params_t *params;
    char *info;

    params = env_params->env_params_maze;

    if ((info = (char *)malloc(sizeof(char) * 6)) == NULL)
    {
        return NULL;
    }

    sprintf(info, "%d,%d", params->pos->h, params->pos->w);
    return info;
}

void env_maze_run_step(env_params_t *env_params, int a)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    if (a == 0)
    {
        params->pos->h--;
    }
    else if (a == 1)
    {
        params->pos->h++;
    }
    else if (a == 2)
    {
        params->pos->w--;
    }
    else if (a == 3)
    {
        params->pos->w++;
    }
    else
    {
        fprintf(stderr, "action index out of range: %d\n", a);
        exit(EXIT_FAILURE);
    }
    return;
}

void env_maze_reset(env_params_t *env_params)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    memcpy(params->pos, params->init_pos, sizeof(env_maze_pos_t));
}

int env_maze_is_finish(env_params_t *env_params)
{
    env_maze_params_t *params;

    params = env_params->env_params_maze;

    return env_maze_is_goal(params) || env_maze_is_wall(params);
}

env_maze_pos_t *new_env_maze_pos(int h, int w)
{
    env_maze_pos_t *pos;

    if ((pos = (env_maze_pos_t *)malloc(sizeof(env_maze_pos_t))) == NULL)
    {
        return NULL;
    }

    pos->h = h;
    pos->w = w;

    return pos;
}

env_t *new_env_cartpole(const config_t *config)
{
    env_cartpole_params_t *params;
    env_t *env;

    if ((params = new_env_cartpole_params(config)) == NULL)
    {
        return NULL;
    }

    if ((env = (env_t *)malloc(sizeof(env_t))) == NULL)
    {
        return NULL;
    }

    if ((env->params = (env_params_t *)malloc(sizeof(env_params_t))) == NULL)
    {
        return NULL;
    }

    env->type = ENV_TYPE_CARTPOLE;
    env->params->env_params_cartpole = params;
    env->state_size = env_cartpole_state_size;
    env->action_size = env_cartpole_action_size;
    env->state = env_cartpole_state;
    env->reward = env_cartpole_reward;
    env->info = env_cartpole_info;
    env->run_step = env_cartpole_run_step;
    env->reset = env_cartpole_reset;
    env->is_finish = env_cartpole_is_finish;

    return env;
}

env_cartpole_params_t *new_env_cartpole_params(const config_t *config)
{
    env_cartpole_params_t *params;
    double *actions;
    double x_left, x_right;
    double theta_left, theta_right;
    double xdot_left, xdot_right;
    double thetadot_left, thetadot_right;
    int x_size, theta_size, xdot_size, thetadot_size;
    double g, cartmass, m, l, ml, mass;
    int fps;
    double tau;
    double *init_state, *s;

    if ((actions = (double *)malloc(sizeof(double) * MAX_CARTPOLE_ACTIONS_LEN)) == NULL)
    {
        return NULL;
    }
    actions[0] = get_config_as_double(config, "ENV_ACTION_LEFT");
    actions[1] = get_config_as_double(config, "ENV_ACTION_RIGHT");

    x_left = get_config_as_double(config, "ENV_X_LEFT");
    x_right = get_config_as_double(config, "ENV_X_RIGHT");
    theta_left = get_config_as_double(config, "ENV_THETA_LEFT");
    theta_right = get_config_as_double(config, "ENV_THETA_RIGHT");
    xdot_left = get_config_as_double(config, "ENV_XDOT_LEFT");
    xdot_right = get_config_as_double(config, "ENV_XDOT_RIGHT");
    thetadot_left = get_config_as_double(config, "ENV_THETADOT_LEFT");
    thetadot_right = get_config_as_double(config, "ENV_THETADOT_RIGHT");

    x_size = get_config_as_int(config, "ENV_X_SIZE");
    theta_size = get_config_as_int(config, "ENV_THETA_SIZE");
    xdot_size = get_config_as_int(config, "ENV_XDOT_SIZE");
    thetadot_size = get_config_as_int(config, "ENV_THETADOT_SIZE");

    g = get_config_as_double(config, "ENV_GRAVITY");
    cartmass = get_config_as_double(config, "ENV_CART_MASS");
    m = get_config_as_double(config, "ENV_POLE_MASS");
    l = get_config_as_double(config, "ENV_POLE_LENGTH");
    ml = m * l;
    mass = cartmass + m;

    fps = get_config_as_double(config, "ENV_FRAME_PER_SECOND");
    tau = 1.0 / (double)fps;

    init_state = new_env_cartpole_state(0.0, M_PI, 0.0, 0.0);
    s = new_env_cartpole_state(init_state[0], init_state[1], init_state[2], init_state[3]);

    if ((params = (env_cartpole_params_t *)malloc(sizeof(env_cartpole_params_t))) == NULL)
    {
        return NULL;
    }

    params->actions = actions;
    params->x_left = x_left;
    params->x_right = x_right;
    params->theta_left = theta_left;
    params->theta_right = theta_right;
    params->xdot_left = xdot_left;
    params->xdot_right = xdot_right;
    params->thetadot_left = thetadot_left;
    params->thetadot_right = thetadot_right;
    params->x_size = x_size;
    params->theta_size = theta_size;
    params->xdot_size = xdot_size;
    params->thetadot_size = thetadot_size;
    params->g = g;
    params->m = m;
    params->l = l;
    params->ml = ml;
    params->mass = mass;
    params->tau = tau;
    params->init_state = init_state;
    params->s = s;

    return params;
}

double *env_cartpole_solve_runge_kutta(
    env_cartpole_params_t *env,
    double *s,
    double u,
    double dt)
{
    double *k1, *k2, *k3, *k4, *s1, *s2, *s3, *snext;
    int i;

    k1 = env_cartpole_differential(env, s, u);
    s1 = env_cartpole_solve_euler(env, s, k1, dt / 2.0);
    k2 = env_cartpole_differential(env, s1, u);
    s2 = env_cartpole_solve_euler(env, s, k2, dt / 2.0);
    k3 = env_cartpole_differential(env, s2, u);
    s3 = env_cartpole_solve_euler(env, s, k3, dt);
    k4 = env_cartpole_differential(env, s3, u);

    if ((snext = new_env_cartpole_state(s[0], s[1], s[2], s[3])) == NULL)
    {
        return NULL;
    }

    for (i = 0; i < 4; i++)
    {
        snext[i] += (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) * dt / 6.0;
    }

    snext[1] = env_cartpole_theta_normalize(snext[1]);

    free(k1);
    free(k2);
    free(k3);
    free(k4);
    free(s1);
    free(s2);
    free(s3);
    return snext;
}

double *env_cartpole_differential(env_cartpole_params_t *env, double *s, double u)
{
    double theta, xdot, thetadot;
    double sintheta, costheta;
    double l, g, m, ml, mass;
    double xddot, thetaddot;

    theta = s[1];
    xdot = s[2];
    thetadot = s[3];

    sintheta = sin(theta);
    costheta = cos(theta);

    l = env->l;
    g = env->g;
    m = env->m;
    ml = env->ml;
    mass = env->mass;

    xddot = (4.0 * u / 3.0 + 4.0 * ml * pow(thetadot, 2.0) * sintheta / 3.0 - m * g * sin(2.0 * theta) / 2.0) / (4.0 * mass - m * pow(costheta, 2.0));
    thetaddot = (mass * g * sintheta - ml * pow(thetadot, 2.0) * sintheta * costheta - u * costheta) / (4.0 * mass * l / 3.0 - ml * pow(costheta, 2.0));

    return new_env_cartpole_state(xdot, thetadot, xddot, thetaddot);
}

double *env_cartpole_solve_euler(
    env_cartpole_params_t *env,
    double *s, double *sdot, double dt)
{
    double *res;
    int i;

    if ((res = new_env_cartpole_state(s[0], s[1], s[2], s[3])) == NULL)
    {
        return NULL;
    }

    for (i = 0; i < 4; i++)
    {
        res[i] += sdot[i] * dt;
    }

    return res;
}

int env_cartpole_state_size(env_params_t *env_params)
{
    env_cartpole_params_t *params;

    params = env_params->env_params_cartpole;

    return params->x_size * params->theta_size * params->xdot_size * params->thetadot_size;
}

int env_cartpole_action_size(env_params_t *env_params)
{
    return MAX_CARTPOLE_ACTIONS_LEN;
}

int env_cartpole_state(env_params_t *env_params)
{
    env_cartpole_params_t *params;
    int x_idx, theta_idx, xdot_idx, thetadot_idx;

    params = env_params->env_params_cartpole;

    x_idx = env_cartpole_digitize(
        params->x_left, params->x_right, params->x_size, params->s[0]);
    theta_idx = env_cartpole_digitize(
        params->theta_left, params->theta_right, params->theta_size, params->s[1]);
    xdot_idx = env_cartpole_digitize(
        params->xdot_left, params->xdot_right, params->xdot_size, params->s[2]);
    thetadot_idx = env_cartpole_digitize(
        params->thetadot_left, params->thetadot_right, params->thetadot_size, params->s[3]);

    return ((x_idx * params->theta_size + theta_idx) * params->xdot_size + xdot_idx) * params->thetadot_size + thetadot_idx;
}

char *env_cartpole_info(env_params_t *env_params)
{
    env_cartpole_params_t *params;
    double x, theta, xdot, thetadot;
    char *res;

    params = env_params->env_params_cartpole;
    x = params->s[0];
    theta = params->s[1];
    xdot = params->s[2];
    thetadot = params->s[3];

    if ((res = (char *)malloc(sizeof(char) * 128)) == NULL)
    {
        return NULL;
    }

    sprintf(res, "%.15lf,%.15lf,%.15lf,%.15lf", x, theta, xdot, thetadot);

    return res;
}

double env_cartpole_reward(env_params_t *env_params)
{
    env_cartpole_params_t *params;
    double x, theta;

    params = env_params->env_params_cartpole;

    x = params->s[0];
    theta = params->s[1];

    if (fabs(x) > 2.0)
    {
        return -2.0;
    }
    return -fabs(theta) + M_PI / 2.0 - 0.01 * fabs(x);
}

void env_cartpole_reset(env_params_t *env_params)
{
    env_cartpole_params_t *params;

    params = env_params->env_params_cartpole;

    memcpy(params->s, params->init_state, sizeof(double) * 4);

    return;
}

void env_cartpole_run_step(env_params_t *env_params, int a)
{
    env_cartpole_params_t *params;
    double u;
    double *snext;

    params = env_params->env_params_cartpole;

    u = params->actions[a];
    snext = env_cartpole_solve_runge_kutta(params, params->s, u, params->tau);
    free(params->s);
    params->s = snext;

    return;
}

int env_cartpole_is_finish(env_params_t *env_params)
{
    return FALSE;
}

int env_cartpole_digitize(double left, double right, int size, double val)
{
    double width;

    if (val < left)
    {
        return 0;
    }
    else if (val >= right)
    {
        return size - 1;
    }
    width = (right - left) / (double)(size - 2);
    return (int)((val - left) / width) + 1;
}

double env_cartpole_theta_normalize(double theta)
{
    return fmod(theta + 3.0 * M_PI, 2.0 * M_PI) - M_PI;
}

double *new_env_cartpole_state(double x, double theta, double xdot, double thetadot)
{
    double *res;

    if ((res = (double *)malloc(sizeof(double) * 4)) == NULL)
    {
        return NULL;
    }

    res[0] = x;
    res[1] = theta;
    res[2] = xdot;
    res[3] = thetadot;

    return res;
}
