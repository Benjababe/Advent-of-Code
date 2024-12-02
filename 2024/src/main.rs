use std::env;

mod day_01;

fn main() {
    let args: Vec<String> = env::args().collect();
    let big_boy: bool = args.contains(&"bigboy".to_string()) || args.contains(&"bb".to_string());

    day_01::solve(big_boy);
}
