require_relative "config"
require_relative "rl"

def run(argv)
  if argv.length != 1
    raise "invalid argv length: #{argv}"
  end

  config = Config.new(argv[0])
  rl = RL.new(config)
  rl.run
  rl.save_returns
  rl.run_test
  rl.save_test_history
end
