import copy
from math import sin, cos, pi
import random


class CartPoleEnv:
    def __init__(self):
        self.g = 9.80665  # 重力加速度
        self.M = 1.0  # カートの質量
        self.m = 0.1  # ポールの質量
        self.l = 0.5  # pole の半分の長さ
        self.action_range = 10.  # -10. <= a <= 10.
        self.fps = 50  # frames per sec
        self.tau = 1 / self.fps  # 制御周期

        # あとの計算で使う
        self.ml = self.m * self.l
        self.mass = self.M + self.m

        # self.s が生成される
        # s = [x, theta, xdot, thetadot]
        self.reset_state()

    def reset_state(self):
        # s = (x, theta, xdot, thetadot)
        self.s = [.0, 0, .0, .0]

    def step(self, u):
        """入力 u を受け取る"""

        assert(abs(u) <= self.action_range)
        self._runge_kutta_solve(self.s, u, self.tau)

    def state(self):
        return self.s

    def reward(self):
        x, theta, xdot, thetadot = self.s
        if abs(thetadot) > 15:
            return -2
        elif abs(x) > 1:
            return -2
        if abs(theta) < 0.5:
            return 2
        return cos(theta)

    def _state_equation(self, s, u, dt):
        """状態 s で力 u を加えたときの dt 時間後の状態方程式を計算する"""

        x, theta, xdot, thetadot = s
        sintheta = sin(theta)
        costheta = cos(theta)

        xddot = (4*u/3 + 4*self.ml*(thetadot**2)*sintheta/3 -
                 self.m * self.g*sin(2*theta)/2) / (4*self.mass - self.m*(costheta**2))
        thetaddot = (self.mass*self.g*sintheta - self.ml*(thetadot**2)*sintheta *
                     costheta - u*costheta) / (4*self.mass*self.l/3 - self.ml*(costheta**2))

        return [xdot, thetadot, xddot, thetaddot]

    def _euler_solve(self, s, sdot, dt):
        """オイラー法を用いて，状態 s のとき状態の微分 sdot から dt 時間後の状態を計算する"""

        return [s[i] + sdot[i]*dt for i in range(len(sdot))]

    def _runge_kutta_solve(self, s, u, dt):
        """ルンゲクッタを用いて状態 s のとき力 u を加えて dt 時間後の状態を計算する。
        NOTE: self.s を破壊的に更新する。ベンチとってないけどそのほうが速いよね？
        """

        # FIXME: なんか引数が変だぞ
        k1 = self._state_equation(s, u, dt/2)
        s1 = self._euler_solve(s, k1, dt/2)
        k2 = self._state_equation(s1, u, dt/2)
        s2 = self._euler_solve(s, k2, dt/2)
        k3 = self._state_equation(s2, u, dt/2)
        s3 = self._euler_solve(s, k3, dt)
        k4 = self._state_equation(s3, u, dt)

        # FIXME: ここ self.tau じゃなくね？？
        for i in range(len(self.s)):
            self.s[i] = s[i] + \
                (k1[i] + 2*k2[i] + 2 * k3[i] + k4[i]) * self.tau / 6

        # theta の正規化はこのタイミングで行う
        self.s[1] = self._normalize_theta(self.s[1])

    def _normalize_theta(self, theta):
        if theta >= pi:
            return theta - 2*pi
        elif theta < -pi:
            return theta + 2*pi
        return theta


class Agent:
    def __init__(self):
        self.alpha = 0.1  # 学習率
        self.gamma = 0.99  # 割引率
        self.eps = 0.1  # ランダムに探索する割合
        self.init_q = 10  # Q 値の初期値
        self.actions = [-10., .0, 10.]  # 行動の候補

        # 状態分割の下限と上限
        self.x_limits = [-1, 1]
        self.theta_limits = [-pi, pi]
        self.xdot_limits = [-2, 2]
        self.thetadot_limits = [-8, 8]

        # 状態の分割数
        self.x_num = 10
        self.theta_num = 36
        self.xdot_num = 10
        self.thetadot_num = 10

        # 状態分割の仕切りの値を生成
        self.x_bins = self._make_bins(self.x_limits, self.x_num)
        self.theta_bins = self._make_bins(self.theta_limits, self.theta_num)
        self.xdot_bins = self._make_bins(self.xdot_limits, self.xdot_num)
        self.thetadot_bins = self._make_bins(
            self.thetadot_limits, self.thetadot_num)

        self._init_qtable(self.init_q)

    def action(self, s):
        if random.random() < self.eps:
            return random.choice(self.actions)
        s_idx = self._s_to_idx(s)
        max_idx = self._argmax(self.qtable[s_idx])
        return self.actions[max_idx]

    def learn(self, s0, a0, r, s1, a1):
        # とりあえず Q-learning にした
        s0_idx = self._s_to_idx(s0)
        a0_idx = self.actions.index(a0)
        s1_idx = self._s_to_idx(s1)
        # a1_idx = self.actions.index(a1)

        self.qtable[s0_idx][a0_idx] = \
            (1-self.alpha) * self.qtable[s0_idx][a0_idx] + \
            self.alpha * (r + self.gamma * max(self.qtable[s1_idx]))

    def _init_qtable(self, init_q):
        total_s_idx = self.x_num * self.theta_num * self.xdot_num * self.thetadot_num
        self.qtable = [[init_q] * len(self.actions)
                       for _ in range(total_s_idx)]

    def _make_bins(self, limits, num):
        """状態分割の区切りとなる値のリストを作成する"""

        width = (limits[1] - limits[0]) / num
        return [limits[0] + width*(i+1) for i in range(num-1)]

    def _digitize(self, val, bins):
        for i, thresh in enumerate(bins):
            if val < thresh:
                return i
        return i + 1

    def _digitize_all(self, s):
        x_idx = self._digitize(s[0], self.x_bins)
        theta_idx = self._digitize(s[1], self.theta_bins)
        xdot_idx = self._digitize(s[2], self.xdot_bins)
        thetadot_idx = self._digitize(s[3], self.thetadot_bins)
        return x_idx, theta_idx, xdot_idx, thetadot_idx

    def _s_to_idx(self, s):
        xidx, thetaidx, xdotidx, thetadotidx = self._digitize_all(s)
        return xidx * self.theta_num * self.xdot_num * self.thetadot_num + \
            thetaidx * self.xdot_num * self.thetadot_num + \
            xdotidx * self.thetadot_num + \
            thetadotidx

    def _argmax(self, lst):
        return lst.index(max(lst))


class Experiment:
    def __init__(self):
        self.env = CartPoleEnv()
        self.agent = Agent()

        self.episodes_num = 10000
        self.steps_num = self.env.fps * 10

        self.returns_hist = [.0 for _ in range(self.episodes_num)]
        self.states_hist = [None for _ in range(self.steps_num)]

    def run(self):
        for episode in range(self.episodes_num):
            returns = self.episode()
            self.returns_hist[episode] = returns

    def test(self):
        return self.episode(states_hist=True)

    def episode(self, states_hist=False):
        returns = .0

        self.env.reset_state()
        s = self.env.state()
        a = None

        for step in range(self.steps_num):
            if states_hist:
                self.states_hist[step] = copy.copy(s)

            a_next = self.agent.action(s)
            self.env.step(a_next)
            s_next = self.env.state()
            r = self.env.reward()
            returns += r
            if step > 0:
                self.agent.learn(s, a, r, s_next, a_next)
            s = s_next
            a = a_next

        return returns


if __name__ == "__main__":
    exp = Experiment()
    exp.run()
    exp.test()

    with open("returns.csv", "w") as f:
        for ret in exp.returns_hist:
            print(ret, file=f)

    with open("states.csv", "w") as f:
        for s in exp.states_hist:
            print(",".join(map(str, s)), file=f)
