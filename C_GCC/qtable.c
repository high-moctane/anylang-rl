#include <stdlib.h>
#include "qtable.h"

qtable_t *new_qtable(int state_size, int action_size, double init_qvalue)
{
    double **table;
    qtable_t *qtable;
    int i, j;

    if ((qtable = (qtable_t *)malloc(sizeof(qtable_t))) == NULL)
    {
        return NULL;
    }

    if ((table = (double **)malloc(sizeof(double *) * state_size)) == NULL)
    {
        return NULL;
    }

    for (i = 0; i < state_size; i++)
    {
        if ((table[i] = (double *)malloc(sizeof(double) * action_size)) == NULL)
        {
            return NULL;
        }

        for (j = 0; j < action_size; j++)
        {
            table[i][j] = init_qvalue;
        }
    }

    qtable->state_size = state_size;
    qtable->action_size = action_size;
    qtable->init_qvalue = init_qvalue;
    qtable->table = table;

    return qtable;
}