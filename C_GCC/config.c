#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "config.h"
#include "main.h"

config_t *new_config(const char path[])
{
    FILE *fp;
    char **keys, **values;
    char *key, *value;
    int length = 0;
    config_t *config = NULL;

    if ((keys = (char **)malloc(sizeof(char *) * MAX_CONFIG_LEN)) == NULL)
    {
        return NULL;
    }
    if ((values = (char **)malloc(sizeof(char *) * MAX_CONFIG_LEN)) == NULL)
    {
        return NULL;
    }

    if ((fp = fopen(path, "r")) == NULL)
    {
        return NULL;
    }

    for (;;)
    {
        if ((key = (char *)malloc(sizeof(char) * MAX_CONFIG_LINE_LEN)) == NULL)
        {
            goto END;
        }

        if ((value = (char *)malloc(sizeof(char) * MAX_CONFIG_LINE_LEN)) == NULL)
        {
            goto END;
        }

        if (read_config(fp, key, value))
        {
            keys[length] = key;
            values[length] = value;
            length++;
        }
        else
        {
            break;
        }
    }

    if ((config = (config_t *)malloc(sizeof(config_t))) == NULL)
    {
        goto END;
    }

    config->length = length;
    config->keys = keys;
    config->values = values;

END:
    fclose(fp);
    return config;
}

int read_config(FILE *fp, char key[], char value[])
{
    char line[MAX_CONFIG_LINE_LEN + 1];
    char *assign_pos;
    int i, j;

    if (fgets(line, MAX_CONFIG_LINE_LEN, fp) == NULL)
    {
        return FALSE;
    }

    if ((assign_pos = strchr(line, '=')) != strrchr(line, '='))
    {
        return FALSE;
    }

    for (i = 0, j = 0; line[i] != '='; i++, j++)
    {
        key[j] = line[i];
    }
    key[j] = '\0';
    for (i++, j = 0; line[i] != '\n'; i++, j++)
    {
        value[j] = line[i];
    }
    value[j] = '\0';

    return TRUE;
}

char *get_config(const config_t *config, const char key[])
{
    int i;
    for (i = 0; i < config->length; i++)
    {
        if (strcmp(config->keys[i], key) == 0)
        {
            return config->values[i];
        }
    }
    return NULL;
}

int get_config_as_int(const config_t *config, const char key[])
{
    char *value;

    if ((value = get_config(config, key)) == NULL)
    {
        return 0;
    }
    return atoi(value);
}

double get_config_as_double(const config_t *config, const char key[])
{
    char *value;

    if ((value = get_config(config, key)) == NULL)
    {
        return 0.0;
    }
    return atof(value);
}
