#include "config.h"

#define ENV_TYPE_MAZE 0
#define ENV_TYPE_CARTPOLE 1

#define MAX_MAZE_HEIGHT 50
#define MAX_MAZE_WIDTH 50

#define MAX_CARTPOLE_ACTIONS_LEN 2

#define M_PI 3.14159265358979324

#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

typedef struct
{
    int h;
    int w;
} env_maze_pos_t;

typedef struct
{
    char **maze;
    int height;
    int width;

    double default_reward;
    double goal_reward;
    double wall_reward;

    env_maze_pos_t *init_pos;
    env_maze_pos_t *goal_pos;
    env_maze_pos_t *pos;
} env_maze_params_t;

typedef struct
{
    double *actions;

    double x_left;
    double x_right;
    double theta_left;
    double theta_right;
    double xdot_left;
    double xdot_right;
    double thetadot_left;
    double thetadot_right;

    int x_size;
    int theta_size;
    int xdot_size;
    int thetadot_size;

    double g;
    double m;
    double l;
    double ml;
    double mass;

    double tau;

    double *init_state;
    double *s;
} env_cartpole_params_t;

typedef union {
    env_maze_params_t *env_params_maze;
    env_cartpole_params_t *env_params_cartpole;
} env_params_t;

typedef struct
{
    int type;
    env_params_t *params;

    int (*state_size)(env_params_t *env_params);
    int (*action_size)(env_params_t *env_params);

    int (*state)(env_params_t *env_params);
    double (*reward)(env_params_t *env_params);
    char *(*info)(env_params_t *env_params);

    void (*run_step)(env_params_t *env_params, int a);
    void (*reset)(env_params_t *env_params);
    int (*is_finish)(env_params_t *env_params);
} env_t;

#endif

env_t *new_env_maze(const config_t *config);

env_maze_params_t *new_env_maze_params(const config_t *config);

int env_maze_parse_maze(const char maze_path[], char **maze, int *height, int *width);

int env_maze_state_size(env_params_t *env_params);

int env_maze_action_size(env_params_t *env_params);

int env_maze_state(env_params_t *env_params);

int env_maze_pos_to_s(env_maze_params_t *params, env_maze_pos_t *pos);

double env_maze_reward(env_params_t *env_params);

int env_maze_is_wall(env_maze_params_t *params);

int env_maze_is_goal(env_maze_params_t *params);

int env_maze_is_equall_pos(env_maze_pos_t *pos1, env_maze_pos_t *pos2);

char *env_maze_info(env_params_t *env_params);

void env_maze_run_step(env_params_t *env_params, int a);

void env_maze_reset(env_params_t *env_params);

int env_maze_is_finish(env_params_t *env_params);

env_maze_pos_t *new_env_maze_pos(int h, int w);

env_t *new_env_cartpole(const config_t *config);

env_cartpole_params_t *new_env_cartpole_params(const config_t *config);

double *env_cartpole_solve_runge_kutta(
    env_cartpole_params_t *env,
    double *s,
    double u,
    double dt);

double *env_cartpole_differential(env_cartpole_params_t *env, double *s, double u);

double *env_cartpole_solve_euler(
    env_cartpole_params_t *env,
    double *s, double *sdot, double dt);

int env_cartpole_state_size(env_params_t *env_params);

int env_cartpole_action_size(env_params_t *env_params);

int env_cartpole_state(env_params_t *env_params);

char *env_cartpole_info(env_params_t *env_params);

double env_cartpole_reward(env_params_t *env_params);

void env_cartpole_reset(env_params_t *env_params);

void env_cartpole_run_step(env_params_t *env_params, int a);

int env_cartpole_is_finish(env_params_t *env_params);

int env_cartpole_digitize(double left, double right, int size, double val);

double env_cartpole_theta_normalize(double theta);

double *new_env_cartpole_state(double x, double theta, double xdot, double thetadot);
