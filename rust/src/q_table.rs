use bincode;
use serde::{Deserialize, Serialize};
use std::error;
use std::fs;
use std::fs::File;
use std::io::prelude::*;

#[derive(Serialize, Deserialize)]
pub struct QTable {
    pub s_space: usize,
    pub a_space: usize,
    pub init_q: f64,
    pub table: Vec<Vec<f64>>,
}

impl QTable {
    pub fn new(init_q: f64, s_space: usize, a_space: usize) -> Self {
        QTable {
            s_space,
            a_space,
            init_q,
            table: vec![vec![init_q; a_space]; s_space],
        }
    }

    pub fn load(path: &str) -> Result<Self, Box<dyn error::Error>> {
        let mut file = File::open(path)?;
        let metadata = fs::metadata(path)?;
        let mut data = vec![0; metadata.len() as usize];
        file.read(&mut data)?;

        // HELP!!!
        match bincode::deserialize(&data) {
            Ok(obj) => Ok(obj),
            Err(kind) => Err(kind),
        }
    }

    pub fn save(&self, path: &str) -> Result<(), Box<dyn error::Error>> {
        let data = bincode::serialize(self)?;
        let mut file = File::create(path)?;
        file.write(&data)?;
        file.flush()?;
        Ok(())
    }
}
