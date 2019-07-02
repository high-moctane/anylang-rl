module Env
  ( State
  , Action
  , Reward
  , initState
  , oneStep
  , reward
  )
where

import           Data.Fixed

g = 9.80665 -- 重力加速度
mCart = 1.0 -- カートの質量
mPole = 0.1 -- ポールの質量
l = 0.5 -- ポールの半分の長さ
fps = 50 -- frames per second
tau = 1 / fps -- 制御周期

-- あとでつかう
ml = mPole * l
mass = mCart + mPole


-- 状態ベクトル
-- 最初 tuple で実装しようと思ったけど気が遠くなるので List にした
type State = [Double]

-- 状態ベクトルの初期値
initState :: State
initState = [0.0, -pi, 0.0, 0.0]


-- 行動の値
type Action = Double


-- 報酬の型
type Reward = Double


reward :: State -> Double
reward s | abs x > 2.0 = -2.0
         | otherwise   = -abs theta + pi / 2
 where
  x     = s !! 0
  theta = s !! 1

oneStep :: State -> Action -> State
oneStep s a = rungeKuttaSolve s a tau

-- 状態 s で力 u を加えたときの微分
differential :: State -> Action -> State
differential s u = [xdot, thetadot, xddot, thetaddot]
 where
  theta    = s !! 1
  xdot     = s !! 2
  thetadot = s !! 3
  sintheta = sin theta
  costheta = cos theta
  -- なんじゃこりゃー（hie が整形した）
  xddot =
    (  4
      *  u
      /  3
      +  4
      *  ml
      *  thetadot
      ** 2
      *  sintheta
      /  3
      -  mPole
      *  g
      *  sin (2 * theta)
      /  2
      )
      / (4 * mass - mPole * costheta ** 2)
  thetaddot =
    (  mass
      *  g
      *  sintheta
      -  ml
      *  thetadot
      ** 2
      *  sintheta
      *  costheta
      -  u
      *  costheta
      )
      / (4 * mass * l / 3 - ml * costheta ** 2)


-- オイラー法で微分方程式を解く
eulerSolve :: State -> State -> Double -> State
eulerSolve s sdot dt = map (\ssdot -> fst ssdot + snd ssdot * dt) $ zip s sdot


-- ルンゲクッタ法で微分方程式を解く
rungeKuttaSolve :: State -> Double -> Double -> State
rungeKuttaSolve s u dt =
  [ snext !! 0
  , mod' ((snext !! 1) + 3.0 * pi) 2 * pi - pi
  , snext !! 2
  , snext !! 3
  ]
 where
  k1 = differential s u
  s1 = eulerSolve s k1 (dt / 2)
  k2 = differential s1 u
  s2 = eulerSolve s k2 (dt / 2)
  k3 = differential s2 u
  s3 = eulerSolve s k3 dt
  k4 = differential s3 u
  -- つらい
  snext =
    [ s !! 0 + (k1 !! 0 + 2 * k2 !! 0 + 2 * k3 !! 0 + k4 !! 0) * dt / 6
    , s !! 1 + (k1 !! 1 + 2 * k2 !! 1 + 2 * k3 !! 1 + k4 !! 1) * dt / 6
    , s !! 2 + (k1 !! 2 + 2 * k2 !! 2 + 2 * k3 !! 2 + k4 !! 2) * dt / 6
    , s !! 3 + (k1 !! 3 + 2 * k2 !! 3 + 2 * k3 !! 3 + k4 !! 3) * dt / 6
    ]
