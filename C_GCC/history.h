#ifndef HISTORY_H
#define HISTORY_H

typedef struct
{
    int action;
    double reward;
    int state;
    char *info;
} history_entry_t;

typedef struct
{
    int length;
    int capacity;
    history_entry_t **entries;
} history_t;

#endif

history_t *new_history(void);

int history_push(history_t *history, int a, double r, int s, char info[]);

void history_free(history_t *history);

int history_save(history_t *history, const char path[]);
