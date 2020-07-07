import config
import q_table
import history
import agent.sarsa as sarsa
import agent.q_learning as q_learning
import environment.cartpole as cartpole
import environment.maze as maze


class InvalidAgentNameException(Exception):
    pass


class InvalidEnvNameException(Exception):
    pass


class RL:
    def __init__(self, config: config.Config):
        self.returns_path = config.items["RL_RETURNS_PATH"]
        self.test_history_path = config.items["RL_TEST_HISTORY_PATH"]

        self.max_episode = int(config.items["RL_MAX_EPISODE"])
        self.max_step = int(config.items["RL_MAX_STEP"])

        self.agent = self.choose_agent(config)
        self.env = self.choose_environment(config)

        init_qvalue = float(config.items["QTABLE_INITIAL_QVALUE"])
        self.q_table = q_table.QTable(
            self.env.state_size(), self.env.action_size(), init_qvalue)

        self.returns = []
        self.test_history = history.History()

    def choose_agent(self, config: config.Config):
        agent_name = config.items["AGENT_NAME"]
        if agent_name == "Sarsa":
            return sarsa.Sarsa(config)
        elif agent_name == "Q-learning":
            return q_learning.QLearning(config)
        raise InvalidAgentNameException(agent_name)

    def choose_environment(self, config: config.Config):
        env_name = config.items["ENV_NAME"]
        if env_name == "Cartpole":
            return cartpole.Cartpole(config)
        elif env_name == "Maze":
            return maze.Maze(config)
        raise InvalidEnvNameException(env_name)

    def run(self):
        for _ in range(self.max_episode):
            history_ = self.run_episode()
            self.returns.append(sum(history_.rewards))

    def run_episode(self) -> history.History:
        history_ = history.History()

        self.env.reset()

        s1 = self.env.state()
        s2 = s1
        r = self.env.reward()
        info = self.env.info()
        a1 = self.agent.action(self.q_table, s1)
        a2 = a1

        history_.append(a1, r, s2, info)

        for _ in range(self.max_step):
            self.env.run_step(a1)
            s2 = self.env.state()
            r = self.env.reward()
            info = self.env.info()
            a2 = self.agent.action(self.q_table, s2)

            history_.append(a1, r, s2, info)

            if self.env.is_finish():
                for i in range(self.q_table.action_size):
                    self.q_table.table[s2][i] = 0.
            self.agent.learn(self.q_table, s1, a1, r, s2, a2)

            if self.env.is_finish():
                break

            s1 = s2
            a1 = a2

        return history_

    def run_test(self):
        self.agent.fix()
        self.test_history = self.run_episode()

    def save_returns(self):
        with open(self.returns_path, mode="w") as f:
            for ret in self.returns:
                f.write("{:.15f}\n".format(ret))

    def save_test_history(self):
        self.test_history.save(self.test_history_path)
