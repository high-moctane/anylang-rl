#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "experiment.h"
#include "SFMT.h"

sfmt_t *new_sfmt();
void save_returns(double *, int);
void save_states(state_t *, int);
void save_actions(double *, int);
void save_rewards(double *, int);