class Maze
  def initialize(config)
    @maze = open_maze(config.config["ENV_MAZE_PATH"])
    @height = @maze.length
    @width = @maze[0].length

    @default_reward = config.config["ENV_DEFAULT_REWARD"].to_f
    @goal_reward = config.config["ENV_GOAL_REWARD"].to_f
    @wall_reward = config.config["ENV_WALL_REWARD"].to_f

    @init_pos = [1, 1].freeze
    @goal_pos = [@height - 2, @width - 2].freeze
    @pos = @init_pos.clone
  end

  def open_maze(path)
    maze = []
    open(path) do |f|
      f.each_line do |line|
        maze.push(line.chomp.split(""))
      end
    end
    maze
  end

  def pos_to_s(pos)
    pos[0] * @width + pos[1]
  end

  def is_goal
    @pos == @goal_pos
  end

  def is_wall
    @maze[@pos[0]][@pos[1]] == "#"
  end

  def state_size
    @height * @width
  end

  def action_size
    4
  end

  def state
    pos_to_s(@pos)
  end

  def reward
    if is_wall
      @wall_reward
    elsif is_goal
      @goal_reward
    else
      @default_reward
    end
  end

  def info
    "#{@pos[0]},#{@pos[1]}"
  end

  def run_step(a)
    @pos = \
      case a
      when 0 then
        [@pos[0]-1, @pos[1]]
      when 1 then
        [@pos[0]+1, @pos[1]]
      when 2 then
        [@pos[0], @pos[1]-1]
      when 3 then
        [@pos[0], @pos[1]+1]
      else
        raise "action index out of range: #{a}"
      end
  end

  def reset
    @pos = @init_pos.clone
  end

  def is_finish
    is_goal || is_wall
  end
end
