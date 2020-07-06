use crate::config::Config;
use crate::environment::Environment;
use crate::{Action, Reward, State};
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

pub struct Maze {
    maze: Vec<Vec<char>>,
    height: usize,
    width: usize,

    default_reward: Reward,
    goal_reward: Reward,
    wall_reward: Reward,

    init_pos: Pos,
    goal_pos: Pos,
    pos: Pos,
}

impl Maze {
    pub fn new(config: &Config) -> Result<Maze, Box<dyn Error>> {
        let maze = Maze::open_maze(&config.get("ENVIRONMENT_MAZE_PATH")?)?;
        let height = maze.len();
        let width = maze[0].len();

        let default_reward = config
            .get("ENVIRONMENT_DEFAULT_REWARD")?
            .parse::<Reward>()?;
        let goal_reward = config.get("ENVIRONMENT_GOAL_REWARD")?.parse::<Reward>()?;
        let wall_reward = config.get("ENVIRONMENT_WALL_REWARD")?.parse::<Reward>()?;

        let init_pos = (1, 1);
        let goal_pos = (height - 2, width - 2);
        let pos = init_pos;

        Ok(Maze {
            maze,
            height,
            width,
            default_reward,
            goal_reward,
            wall_reward,
            init_pos,
            goal_pos,
            pos,
        })
    }

    fn open_maze(path: &str) -> Result<Vec<Vec<char>>, Box<dyn Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);

        let mut res: Vec<Vec<char>> = vec![];

        for line in reader.lines() {
            res.push(line?.chars().collect())
        }

        Ok(res)
    }

    fn pos_to_s(&self, pos: &Pos) -> State {
        pos.0 * self.width + pos.1
    }

    fn is_goal(&self) -> bool {
        self.pos == self.goal_pos
    }

    fn is_wall(&self) -> bool {
        self.maze[self.pos.0][self.pos.1] == '#'
    }
}

impl Environment for Maze {
    fn state_size(&self) -> usize {
        self.height * self.width
    }

    fn action_size(&self) -> usize {
        4
    }

    fn state(&self) -> State {
        self.pos_to_s(&self.pos)
    }

    fn reward(&self) -> Reward {
        if self.is_wall() {
            self.wall_reward
        } else if self.is_goal() {
            self.goal_reward
        } else {
            self.default_reward
        }
    }

    fn info(&self) -> String {
        format!("{},{}", self.pos.0, self.pos.1)
    }

    fn run_step(&mut self, a: Action) {
        self.pos = match a {
            0 => (self.pos.0 - 1, self.pos.1),
            1 => (self.pos.0 + 1, self.pos.1),
            2 => (self.pos.0, self.pos.1 - 1),
            3 => (self.pos.0, self.pos.1 + 1),
            _ => panic!(format!("action index out of range: {}", a)),
        }
    }

    fn reset(&mut self) {
        self.pos = self.init_pos
    }

    fn is_finish(&self) -> bool {
        self.is_goal() || self.is_wall()
    }
}

type Pos = (usize, usize);
