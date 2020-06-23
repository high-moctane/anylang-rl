import agent.abs_agent as abs_agent
import environment.abs_environment as abs_env
import config
import q_table


class Experiment:
    """実験をするクラスです。"""

    def __init__(self, config: config.Config, agent: abs_agent.Agent, env: abs_env.Environment):
        self._config = config

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

        self._episode = 0
        self._step = 0
        self._success_count = 0

        self._returns = []

    def run(self):
        """実験をします。"""
        for episode in range(self._max_episode):
            returns, succeeded = self.run_episode()
            if succeeded:
                self._success_count += 1
            else:
                self._success_count = 0
            self._returns.append(returns)

            if self._success_count >= self._max_succeeded_episode:
                break

    def test_and_save(self, path: str):
        """学習率を止めた状態で動かして履歴を保存します。"""
        self.agent.fix()
        self.run_episode()
        self.env.save_history(path)
        self.q_table.save(self._config.cfg["QTABLE_PATH"])

    def save_returns(self, path: str):
        """報酬和を保存します。"""
        with open(path, mode="w") as f:
            for returns in self._returns:
                f.write("{:.12f}\n".format(returns))

    def run_episode(self) -> bool:
        """1 エピソード実行します。
        Returns:
            (float, bool)
            float: 報酬和
            bool: 成功したかどうか
        """

        self.env.reset()
        s1 = s2 = self.env.s()
        a1 = a2 = self.agent.a(self.q_table, s1)
        r1 = r2 = self.env.r()
        returns = 0.

        for step in range(self._max_step):
            a1 = a2
            self.env.run_step(a1)
            s2 = self.env.s()
            a2 = self.agent.a(self.q_table, s2)
            r = self.env.r()
            returns += r
            self.agent.learn(self.q_table, s1, a1, r, s2, a2)
            s1 = s2
            if self.env.is_done(s1):
                break

        return returns, self.env.is_success(s1)
