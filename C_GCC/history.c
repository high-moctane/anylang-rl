#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "history.h"
#include "main.h"

history_t *new_history(void)
{
    history_t *history;

    if ((history = (history_t *)malloc(sizeof(history))) == NULL)
    {
        return NULL;
    }

    history->length = 0;
    history->capacity = 1;

    if ((history->entries = (history_entry_t **)malloc(sizeof(history_entry_t *))) == NULL)
    {
        return NULL;
    }

    return history;
}

int history_push(history_t *history, int a, double r, int s, char info[])
{
    void *ptr;

    if (history->length == history->capacity)
    {
        history->capacity *= 2;

        if ((ptr = realloc(history->entries, sizeof(history_entry_t *) * history->capacity)) == NULL)
        {
            return FALSE;
        }
        history->entries = (history_entry_t **)ptr;
    }

    if ((history->entries[history->length] = (history_entry_t *)malloc(sizeof(history_entry_t))) == NULL)
    {
        return FALSE;
    }

    history->entries[history->length]->action = a;
    history->entries[history->length]->reward = r;
    history->entries[history->length]->state = s;
    history->entries[history->length]->info = info;
    history->length++;

    return TRUE;
}

void history_free(history_t *history)
{
    int i;

    for (i = 0; i < history->length; i++)
    {
        free(history->entries[i]->info);
        free(history->entries[i]);
    }

    free(history->entries);
    free(history);

    return;
}

int history_save(history_t *history, const char path[])
{
    FILE *fp;
    int i, res;

    if ((fp = fopen(path, "w")) == NULL)
    {
        return FALSE;
    }

    for (i = 0; i < history->length; i++)
    {
        res = fprintf(fp, "%d\t%.15f\t%d\t%s\n",
                      history->entries[i]->action,
                      history->entries[i]->reward,
                      history->entries[i]->state,
                      history->entries[i]->info);
        if (!res)
        {
            fclose(fp);
            return FALSE;
        }
    }

    fclose(fp);
    return TRUE;
}