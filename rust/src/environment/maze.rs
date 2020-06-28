use crate::config::Config;
use crate::environment::Environment;
use crate::{Action, Reward, State};
use std::error;

pub struct Maze {
    goal_reward: Reward,
    dead_reward: Reward,
    default_reward: Reward,

    height: usize,
    width: usize,
    maze: Vec<Vec<char>>,

    start: Position,
    goal: Position,

    pos: Position,
}

impl Maze {
    pub fn new(config: &Config) -> Result<Box<Self>, Box<dyn error::Error>> {
        let goal_reward: Reward = config.get("ENV_GOAL_REWARD")?.parse()?;
        let dead_reward: Reward = config.get("ENV_DEAD_REWARD")?.parse()?;
        let default_reward: Reward = config.get("ENV_DEFAULT_REWARD")?.parse()?;

        let height: usize = config.get("ENV_HEIGHT")?.parse()?;
        let width: usize = config.get("ENV_WIDTH")?.parse()?;

        let maze = Maze::parse_maze(height, width, &config.get("ENV_MAZE")?);

        let start = (1, 1);
        let goal = (height as i32 - 2, width as i32 - 2);

        let pos = start;

        Ok(Box::new(Maze {
            goal_reward,
            dead_reward,
            default_reward,
            height,
            width,
            maze,
            start,
            goal,
            pos,
        }))
    }

    fn parse_maze(height: usize, width: usize, maze_str: &str) -> Vec<Vec<char>> {
        let maze_chars: Vec<char> = maze_str.chars().collect();
        let mut res = vec![vec!['\0'; width]; height];
        for h in 0..height {
            for w in 0..width {
                let pos = (h as i32, w as i32);
                let s = Maze::pos_to_s(&pos, width);
                res[h][w] = maze_chars[s];
            }
        }
        res
    }

    fn pos_to_s(pos: &Position, width: usize) -> State {
        pos.0 as usize * width + pos.1 as usize
    }

    fn is_goal(&self, pos: &Position) -> bool {
        *pos == self.goal
    }

    fn is_in_maze(&self, pos: &Position) -> bool {
        0 <= pos.0 && pos.0 < self.height as i32 && 0 <= pos.1 && pos.1 < self.width as i32
    }

    fn is_in_wall(&self, pos: &Position) -> bool {
        self.maze[pos.0 as usize][pos.1 as usize] == '#'
    }
}

impl Environment for Maze {
    fn s_space(&self) -> State {
        self.height * self.width
    }

    fn a_space(&self) -> Action {
        4
    }

    fn s(&self) -> State {
        Maze::pos_to_s(&self.pos, self.width)
    }

    fn r(&self) -> Reward {
        if self.is_goal(&self.pos) {
            self.goal_reward
        } else if !self.is_in_maze(&self.pos) || self.is_in_wall(&self.pos) {
            self.dead_reward
        } else {
            self.default_reward
        }
    }

    fn info(&self) -> String {
        format!("{},{}", self.pos.0, self.pos.1)
    }

    fn reset(&mut self) {
        self.pos = self.start;
    }

    fn run_step(&mut self, a: Action) {
        match a {
            0 => self.pos = (self.pos.0 - 1, self.pos.1),
            1 => self.pos = (self.pos.0 + 1, self.pos.1),
            2 => self.pos = (self.pos.0, self.pos.1 - 1),
            _ => self.pos = (self.pos.0, self.pos.1 + 1),
        }
    }

    fn is_done(&self) -> bool {
        self.is_goal(&self.pos) || !self.is_in_maze(&self.pos) || self.is_in_wall(&self.pos)
    }

    fn is_success(&self) -> bool {
        self.is_goal(&self.pos)
    }
}

type Position = (i32, i32);
