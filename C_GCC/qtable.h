#ifndef QTABLE_H
#define QTABLE_H

typedef struct
{
    int state_size;
    int action_size;
    double init_qvalue;
    double **table;
} qtable_t;

#endif

qtable_t *new_qtable(int state_size, int action_size, double init_qvalue);
