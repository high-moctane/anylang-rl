import agent
import cartpole


class History:
    def __init__(self, step_num):
        self.states = [None for _ in range(step_num)]
        self.actions = [None for _ in range(step_num)]
        self.rewards = [None for _ in range(step_num)]


class Experiment:
    def __init__(self):
        self.agent = agent.Agent()
        self.env = cartpole.CartPole()

        self.episodes_num = 10000000
        self.steps_num = self.env.fps * 10

    def run(self):
        returns = [None for _ in range(self.episodes_num)]

        for episode in range(self.episodes_num):
            hist = self.one_episode()
            returns[episode] = sum(hist.rewards)

        return returns

    def test(self):
        self.agent.set_test_params()
        return self.one_episode()

    def one_episode(self):
        hist = History(self.steps_num)

        self.env.reset_state()
        s = self.env.state()
        a = 0.0
        r = 0.0

        for step in range(self.steps_num):
            hist.states[step] = s
            hist.actions[step] = a
            hist.rewards[step] = r

            a = self.agent.action(s)
            self.env.step(a)
            s_next = self.env.state()
            r = self.env.reward()
            self.agent.learn(s, a, r, s_next)

            s = s_next

        return hist
