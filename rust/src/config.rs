use std::collections::HashMap;
use std::error;
use std::fmt;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

pub struct Config {
    cfg: HashMap<String, String>,
}

impl Config {
    pub fn new(path: &str) -> Result<Self, Box<dyn error::Error>> {
        let file = File::open(path)?;
        let buf_reader = BufReader::new(file);

        let mut cfg = HashMap::new();

        for line in buf_reader.lines() {
            let line = line?.trim().to_string();
            if line == "" {
                continue;
            }

            let items: Vec<&str> = line.trim().split("=").collect();
            if items.len() != 2 {
                return Err(Box::new(ConfigParseError::new(&line)));
            }

            cfg.insert(items[0].to_string(), items[1].to_string());
        }

        Ok(Config { cfg })
    }

    pub fn get(&self, key: &str) -> Result<String, NoKeyError> {
        match self.cfg.get(key) {
            Some(val) => Ok(val.to_string()),
            None => Err(NoKeyError::new(key)),
        }
    }
}

#[derive(Debug)]
pub struct ConfigParseError {
    line: String,
}

impl ConfigParseError {
    fn new(line: &str) -> Self {
        ConfigParseError {
            line: line.to_string(),
        }
    }
}

impl error::Error for ConfigParseError {}

impl fmt::Display for ConfigParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid line: {}", self.line)
    }
}

#[derive(Debug)]
pub struct NoKeyError {
    key: String,
}

impl NoKeyError {
    fn new(key: &str) -> Self {
        NoKeyError {
            key: key.to_string(),
        }
    }
}

impl error::Error for NoKeyError {}

impl fmt::Display for NoKeyError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "key not found: {}", self.key)
    }
}
