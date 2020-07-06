use std::collections::HashMap;
use std::env;
use std::error::Error;
use std::fmt;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[derive(Debug)]
pub struct Config {
    items: HashMap<String, String>,
}

impl Config {
    pub fn new(args: &mut env::Args) -> Result<Config, Box<dyn Error>> {
        let arg = Args::new(args)?;

        let file = File::open(&arg.config_path)?;
        let reader = BufReader::new(file);

        let mut items = HashMap::new();

        for line in reader.lines() {
            let l = String::from(line?);
            let (key, value) = Config::parse_line(&l)?;
            items.insert(key, value);
        }

        Ok(Config { items })
    }

    fn parse_line(line: &str) -> Result<(String, String), EnvParseError> {
        let key_value: Vec<&str> = line.split("=").collect();
        if key_value.len() != 2 {
            return Err(EnvParseError::new(line));
        }

        Ok((String::from(key_value[0]), String::from(key_value[1])))
    }

    pub fn get(&self, key: &str) -> Result<String, ConfigKeyNotFoundError> {
        match self.items.get(key) {
            Some(value) => Ok(String::from(value)),
            None => Err(ConfigKeyNotFoundError::new(key)),
        }
    }
}

#[derive(Debug)]
pub struct EnvParseError {
    line: String,
}

impl Error for EnvParseError {}

impl fmt::Display for EnvParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid line: {:?}", &self.line)
    }
}

impl EnvParseError {
    fn new(line: &str) -> EnvParseError {
        EnvParseError {
            line: String::from(line),
        }
    }
}

#[derive(Debug)]
pub struct ConfigKeyNotFoundError {
    key: String,
}

impl Error for ConfigKeyNotFoundError {}

impl fmt::Display for ConfigKeyNotFoundError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "config key not found: {:?}", &self.key)
    }
}

impl ConfigKeyNotFoundError {
    fn new(key: &str) -> ConfigKeyNotFoundError {
        ConfigKeyNotFoundError {
            key: String::from(key),
        }
    }
}

struct Args {
    config_path: String,
}

impl Args {
    fn new(args: &mut env::Args) -> Result<Args, ArgsParseError> {
        let args_string = args.collect::<Vec<String>>();
        if args_string.len() != 2 {
            return Err(ArgsParseError::new(&args_string[1..]));
        }

        Ok(Args {
            config_path: args_string[1].clone(),
        })
    }
}

#[derive(Debug)]
pub struct ArgsParseError {
    args: Vec<String>,
}

impl Error for ArgsParseError {}

impl fmt::Display for ArgsParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid args: {:?}", &self.args)
    }
}

impl ArgsParseError {
    fn new(args: &[String]) -> ArgsParseError {
        let mut a = vec![];
        for arg in args {
            a.push(arg.clone());
        }
        ArgsParseError { args: a }
    }
}
