from math import sin, cos, pi


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
        self.s = [.0, pi/3, .0, .0]

    def step(self, u):
        """入力 u を受け取る"""

        assert(abs(u) <= self.action_range)
        self._runge_kutta_solve(self.s, u, self.tau)

    def state(self):
        return self.s

    def reward(self):
        # TODO: そのうちいい感じの関数にする
        return cos(self.s[2])

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
        pass

    def learn(self):
        pass


if __name__ == "__main__":
    cartpole = CartPoleEnv()
    for i in range(50 * 10):
        s = cartpole.state()
        print(",".join(map(str, s)))
        cartpole.step(0.0)
