import experiment

exp = experiment.Experiment()
returns = exp.run()
history = exp.test()

with open("returns.csv", "w") as f:
    for r in returns:
        f.write(str(r))
        f.write("\n")

with open("states.csv", "w") as f:
    for s in history.states:
        f.write(",".join(map(str, s)))
        f.write("\n")

with open("actions.csv", "w") as f:
    for a in history.actions:
        f.write(str(a))
        f.write("\n")

with open("rewards.csv", "w") as f:
    for r in history.rewards:
        f.write(str(r))
        f.write("\n")
