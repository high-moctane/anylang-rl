import agent.abs_agent as abs_agent
import environment.abs_environment as abs_env
import config
import q_table
import history


class Experiment:
    """Runs reinforcement learning experiments."""

    def __init__(self, config: config.Config, agent: abs_agent.Agent, env: abs_env.Environment):
        self._max_episode = int(config.cfg["EXPERIMENT_MAX_EPISODE"])
        self._max_step = int(config.cfg["EXPERIMENT_MAX_STEP"])
        self._max_succeeded_episode = int(
            config.cfg["EXPERIMENT_MAX_SUCCEEDED_EPISODE"])

        self.agent = agent
        self.env = env
        self.q_table = q_table.QTable(
            float(config.cfg["QTABLE_INIT_QVALUE"]),
            self.env.s_space(),
            self.env.a_space(),
        )

        self._success_count = 0

        self._returns = []

        self._returns_path = config.cfg["RETURNS_PATH"]
        self._q_table_path = config.cfg["QTABLE_PATH"]
        self._history_path = config.cfg["HISTORY_PATH"]

    def run(self):
        """Run an experiment."""
        for episode in range(self._max_episode):
            hist, succeeded = self.run_episode()
            if succeeded:
                self._success_count += 1
            else:
                self._success_count = 0
            self._returns.append(sum(hist.r))

            if self._success_count >= self._max_succeeded_episode:
                break

    def test_and_save(self):
        """Fix the agent, run test, and save the results."""
        self.agent.fix()
        hist, _ = self.run_episode()
        hist.save(self._history_path)
        self.q_table.save(self._q_table_path)

    def save_returns(self):
        """Save returns into path."""
        with open(self._returns_path, mode="w") as f:
            for returns in self._returns:
                f.write("{:.15f}\n".format(returns))

    def run_episode(self) -> ("history.History", bool):
        """Runs one episode.
        Returns:
            (history, bool)
            history: the history of the episode.
            bool: whether the experiment was successful.
        """

        hist = history.History()

        self.env.reset()
        s1 = s2 = self.env.s()
        a1 = a2 = self.agent.a(self.q_table, s1)
        r = self.env.r()

        hist.append(a1, s2, r, self.env.info())

        for step in range(self._max_step):
            a1 = a2
            self.env.run_step(a1)
            s2 = self.env.s()
            a2 = self.agent.a(self.q_table, s2)
            r = self.env.r()
            self.agent.learn(self.q_table, s1, a1, r, s2, a2)

            hist.append(a1, s2, r, self.env.info())

            s1 = s2
            if self.env.is_done():
                break

        return hist, self.env.is_success()
