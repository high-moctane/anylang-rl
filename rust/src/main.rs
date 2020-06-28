use rust::Runner;
use std::env;

fn main() {
    let runner = Runner::new(env::args()).unwrap();
    runner.run().unwrap();
}
