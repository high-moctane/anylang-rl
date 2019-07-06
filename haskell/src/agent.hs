module Agent
    ( Params
    , defaultParams
    , defaultTestParams
    , Qtable
    , newQtable
    , action
    , learn
    )
where

import qualified Data.List                     as L
import qualified Data.Vector                   as V
import qualified Data.Vector.Generic           as G
import qualified Data.Vector.Generic.Mutable   as GM
import qualified Data.Vector.Unboxed           as VU
import qualified Data.Vector.Mutable           as VM
import qualified Data.Vector.Unboxed.Mutable   as VUM
import qualified System.Random                 as R
import qualified Env                           as E


-- Q-value の初期値
initQvalue = 10000.0

-- 行動の候補
actions = [-10.0, 10.0]

-- 状態分割の下限と上限
xLimits = [-2.0, 2.0]
thetaLimits = [-pi, pi]
xdotLimits = [-2.0, 2.0]
thetadotLimits = [-10.0, 10.0]

-- 状態の分割数
xNum = 4
thetaNum = 40
xdotNum = 10
thetadotNum = 50
maxStateLen = xNum * thetaNum * xdotNum * thetadotNum

makeBins :: [Double] -> Int -> [Double]
makeBins lims num =
    [lims !! 0, lims !! 0 + (lims !! 1 - lims !! 0) / fromIntegral (num - 2) .. lims
        !! 1]

-- 状態分割の bins を生成
xBins = makeBins xLimits xNum
thetaBins = makeBins thetaLimits thetaNum
xdotBins = makeBins xdotLimits xdotNum
thetadotBins = makeBins thetadotLimits thetadotNum

-- 学習に使うパラメータ
data Params = Params { alpha :: Double, gamma :: Double, epsilon :: Double }

defaultParams = Params 0.1 0.999 0.1
defaultTestParams = Params 0.0 0.999 0.0


-- 思い切って1次元配列でいいことにした
type Qtable = IO (VUM.IOVector Double)

newQtable :: IO (VUM.IOVector Double)
newQtable = VUM.replicate (maxStateLen * length actions) initQvalue


action :: Params -> Qtable -> E.State -> IO Double
action params qtable s = do
    r <- R.randomIO :: IO Double
    if r < epsilon params
        then do
            aIdx <- R.randomRIO (0, length actions) :: IO Int
            return $ actions !! aIdx
        else do
            let sIdx = getSIdx s
            actions' <- sliceQtable qtable sIdx
            aIdx     <- argmax actions'
            return $ actions !! aIdx

learn :: Params -> Qtable -> E.State -> E.Action -> E.Reward -> E.State -> IO ()
learn params qtable s a r sNext = do
    let sIdx     = getSIdx s
    let aIdx     = getAIdx a
    let sNextIdx = getSIdx sNext
    table  <- qtable
    qValue <- VUM.unsafeRead table $ getIdx sIdx aIdx
    sli    <- sliceQtable qtable sNextIdx
    maxQ   <- max' sli
    VUM.unsafeWrite table (getIdx sIdx aIdx)
        $ (1.0 - alpha params)
        * qValue
        + alpha params
        * (r + gamma params * maxQ)

digitize :: Double -> [Double] -> Int
digitize x bins = length $ takeWhile (< x) bins

getSIdx :: E.State -> Int
getSIdx s =
    xIdx + xNum * (thetaIdx + thetaNum * (xdotIdx + xdotNum * thetadotIdx))
  where
    (x, theta, xdot, thetadot) = E.tupleState s
    xIdx                       = digitize x xBins
    thetaIdx                   = digitize theta thetaBins
    xdotIdx                    = digitize xdot xdotBins
    thetadotIdx                = digitize thetadot thetadotBins

getAIdx :: E.Action -> Int
getAIdx a = let Just x = L.elemIndex a actions in x

-- TODO length actions == 2 を利用しているがちゃんとしたアルゴリズムにしたい
argmax :: VUM.IOVector Double -> IO Int
argmax vec = do
    a <- GM.unsafeRead vec 0
    b <- GM.unsafeRead vec 1
    if a > b then return 0 else return 1


sliceQtable :: Qtable -> Int -> IO (VUM.IOVector Double)
sliceQtable qtable sIdx = VUM.slice sIdx (length actions) <$> qtable

getIdx :: Int -> Int -> Int
getIdx sIdx aIdx = sIdx * length actions + aIdx

-- TODO length actions == 2 を利用しているがちゃんとしたアルゴリズムにしたい
max' :: VUM.IOVector Double -> IO Double
max' vec = do
    a <- GM.unsafeRead vec 0
    b <- GM.unsafeRead vec 1
    if a > b then return a else return b

