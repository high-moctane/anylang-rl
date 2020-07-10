#include <stdio.h>
#include <stdlib.h>
#include "runner.h"

int main(int argc, char *argv[])
{
    if (!run(argc, argv))
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}