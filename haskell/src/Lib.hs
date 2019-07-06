module Lib
    ( run
    )
where

import           System.IO
import qualified Env                           as E
import qualified Experiment                    as Ex

run :: IO ()
run = do
    (returns, ex) <- Ex.run
    ex            <- Ex.test ex
    return ()
