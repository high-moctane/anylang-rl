#include <stdio.h>

#define MAX_CONFIG_LEN 128
#define MAX_CONFIG_LINE_LEN 128

#ifndef CONFIG_H
#define CONFIG_H

typedef struct
{
    int length;
    char **keys;
    char **values;
} config_t;

#endif

config_t *new_config(const char path[]);

int read_config(FILE *fp, char keys[], char values[]);

char *get_config(const config_t *config, const char key[]);

int get_config_as_int(const config_t *config, const char key[]);

double get_config_as_double(const config_t *config, const char key[]);
