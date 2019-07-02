module Agent where

import           Data.Array.IO
import           Env

-- Q-value の初期値
initQvalue :: Double
initQvalue = 10000.0

-- 行動の候補
actions = [-10.0, 10.0]

-- 状態分割の下限と上限
xLimits = [-2.0, 2.0]
thetaLimits = [-pi, pi]
xdotLimits = [-2.0, 2.0]
thetadotLimits = [-10.0, 10.0]

--状態の分割数
xNum = 4
thetaNum = 40
xdotNum = 10
thetadotNum = 50
maxStateIdx = xNum * thetaNum * xdotNum * thetadotNum

-- 状態分割の bins を生成
xBins =
    [xLimits !! 0, xLimits !! 0 + (xLimits !! 1 - xLimits !! 0) / (xNum - 2) .. xLimits
        !! 1]
thetaBins =
    [thetaLimits !! 0, thetaLimits
    !! 0
    +  (thetaLimits !! 1 - thetaLimits !! 0)
    /  (thetaNum - 2) .. thetaLimits !! 1]
xdotBins =
    [xdotLimits !! 0, xdotLimits
    !! 0
    +  (xdotLimits !! 1 - xdotLimits !! 0)
    /  (xdotNum - 2) .. xdotLimits !! 1]
thetadotBins =
    [thetadotLimits !! 0, thetadotLimits
    !! 0
    +  (thetadotLimits !! 1 - thetadotLimits !! 0)
    /  (thetadotNum - 2) .. thetadotLimits !! 1]

-- 学習に使うパラメータ
data Params = Params { alpha :: Double, gamma :: Double, epsilon :: Double }

defaultParams = Params 0.1 0.999 0.1
defaultTestParams = Params 0.0 0.999 0.0

