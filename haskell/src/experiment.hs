module Experiment
    ( Experiments
    , run
    , test
    )
where

import qualified Env                           as E
import qualified Agent                         as A

episodesNum = 10000
stepsNum = E.fps * 10

data Experiments = Experiments {params :: A.Params
    , qtable :: A.Qtable
    , states :: [E.State]
    , actions :: [E.Action]
    , rewards :: [E.Reward]
    }


initExperiments :: IO Experiments
initExperiments = return Experiments { params  = A.defaultParams
                                     , qtable  = A.newQtable
                                     , states  = [E.initState]
                                     , actions = [0.0]
                                     , rewards = [0.0]
                                     }

resetExperiments :: Experiments -> IO Experiments
resetExperiments ex = return Experiments { params  = A.defaultParams
                                         , qtable  = qtable ex
                                         , states  = [E.initState]
                                         , actions = [0.0]
                                         , rewards = [0.0]
                                         }

makeTestExperiments :: Experiments -> IO Experiments
makeTestExperiments ex = return Experiments { params  = A.defaultTestParams
                                            , qtable  = qtable ex
                                            , states  = [E.initState]
                                            , actions = [0.0]
                                            , rewards = [0.0]
                                            }


run :: IO ([IO E.Reward], Experiments)
run = do
    let initEx  = initExperiments
    let loop    = iterate (>>= oneEpisode) initEx
    let returns = map (\ioEx -> sum . rewards <$> ioEx) (take episodesNum loop)
    ex <- loop !! (episodesNum - 1)
    return (returns, ex)



test :: Experiments -> IO Experiments
test ex = do
    testEx <- makeTestExperiments ex
    oneEpisode testEx


oneEpisode :: Experiments -> IO Experiments
oneEpisode ex = do
    let loop = iterate (>>= oneStep) $ resetExperiments ex
    loop !! (stepsNum - 1)


oneStep :: Experiments -> IO Experiments
oneStep ex = do
    let s       = head $ states ex
    let qtable' = qtable ex
    let params' = params ex
    a <- A.action params' qtable' s
    let sNext = E.oneStep s a
    let r     = E.reward sNext
    A.learn params' qtable' s a r sNext
    return Experiments { params  = params'
                       , qtable  = qtable'
                       , states  = sNext : states ex
                       , actions = a : actions ex
                       , rewards = r : rewards ex
                       }
