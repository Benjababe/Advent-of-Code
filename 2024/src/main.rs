use std::env;

mod day_01;
mod day_02;
mod day_03;
mod day_04;

fn main() {
    let args: Vec<String> = env::args().collect();
    let big_boy: bool = args.contains(&"--bigboy".to_string()) || args.contains(&"-bb".to_string());

    day_01::solve(big_boy);
    day_02::solve(big_boy);
    day_03::solve(big_boy);
    day_04::solve(big_boy);
}
