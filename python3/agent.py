from math import pi
import random


class Agent:
    def __init__(self):
        self.alpha = 0.1  # 学習率
        self.gamma = 0.999  # 割引率
        self.epsilon = 0.1  # ランダムに行動選択する割合

        self.init_qvalue = 10000.0  # q-value の初期値
        self.actions = [-10.0, 10.0]  # 行動の候補

        # 状態分割の下限と上限
        self.x_limits = [-2.0, 2.0]
        self.theta_limits = [-pi, pi]
        self.xdot_limits = [-2.0, 2.0]
        self.thetadot_limits = [-10.0, 10.0]

        # 状態の分割数
        self.x_num = 4
        self.theta_num = 90
        self.xdot_num = 10
        self.thetadot_num = 50

        # 状態分割の bins を生成
        self.x_bins = self.make_bins(self.x_limits, self.x_num)
        self.theta_bins = self.make_bins(self.theta_limits, self.theta_num)
        self.xdot_bins = self.make_bins(self.xdot_limits, self.xdot_num)
        self.thetadot_bins = self.make_bins(
            self.thetadot_limits, self.thetadot_num)

        self.qtable = self.make_qtable()

    def action(self, s):
        """eps-greedy"""
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        s_idx = self.get_s_idx(s)
        max_idx = self.argmax(self.qtable[s_idx])
        return self.actions[max_idx]

    def learn(self, s, a, r, snext):
        s_idx = self.get_s_idx(s)
        a_idx = self.actions.index(a)
        snext_idx = self.get_s_idx(s)

        self.qtable[s_idx][a_idx] = \
            (1.0 - self.alpha) * self.qtable[s_idx][a_idx] + \
            self.alpha * (r + self.gamma * max(self.qtable[snext_idx]))

    def set_test_params(self):
        """test 用のパラメータに変更する"""
        self.alpha = 0.0
        self.epsilon = 0.0

    def make_qtable(self):
        # NOTE: すごい多重配列にすると table 作るだけで心折れるので見送り

        total_states_num = self.x_num * self.theta_num * self.xdot_num * self.thetadot_num
        return [[self.init_qvalue] * len(self.actions) for _ in range(total_states_num)]

    def make_bins(self, limits, num):
        width = (limits[1] - limits[0]) / (num - 2)
        return [limits[0] + width * i for i in range(num - 1)]

    def digitize(self, bins, x):
        for i, v in enumerate(bins):
            if x < v:
                return i
        return len(bins)

    def digitize_all(self, s):
        x_idx = self.digitize(self.x_bins, s[0])
        theta_idx = self.digitize(self.theta_bins, s[1])
        xdot_idx = self.digitize(self.xdot_bins, s[2])
        thetadot_idx = self.digitize(self.thetadot_bins, s[3])
        return x_idx, theta_idx, xdot_idx, thetadot_idx

    def get_s_idx(self, s):
        indices = self.digitize_all(s)
        return indices[0] + self.x_num * (indices[1] + self.theta_num * (indices[2] + self.xdot_num * indices[3]))

    def argmax(self, lst):
        idx = 0
        max_val = lst[0]
        for i, v in enumerate(lst):
            if v > max_val:
                idx = i
        return idx
