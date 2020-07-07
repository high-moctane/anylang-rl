from typing import List
import config
import rl


def run(argv: List[str]):
    cfg = config.Config(argv)
    rl_ = rl.RL(cfg)
    rl_.run()
    rl_.save_returns()
    rl_.run_test()
    rl_.save_test_history()
