#include <stdio.h>
#include "config.h"
#include "main.h"
#include "rl.h"

int run(char argc, char *argv[])
{
    config_t *config;
    rl_t *rl;

    if (argc != 2)
    {
        return FALSE;
    }

    if ((config = new_config(argv[1])) == NULL)
    {
        return FALSE;
    }

    if ((rl = new_rl(config)) == NULL)
    {
        return FALSE;
    }

    if (!rl_run(rl))
    {
        return FALSE;
    }

    if (!rl_save_returns(rl))
    {
        return FALSE;
    }

    if (!rl_run_test(rl))
    {
        return FALSE;
    }

    if (!rl_save_test_history(rl))
    {
        return FALSE;
    }

    return TRUE;
}
