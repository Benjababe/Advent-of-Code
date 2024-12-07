use std::env;

mod day_01;
mod day_02;
mod day_03;
mod day_04;
mod day_05;
mod day_07;

fn main() {
    let args: Vec<String> = env::args().collect();
    let big_boy: bool = args.contains(&"--bigboy".to_string()) || args.contains(&"-bb".to_string());

    let mut days: Vec<String> = args
        .iter()
        .position(|arg| arg == "--days" || arg == "-d")
        .and_then(|i| args.get(i + 1))
        .map(|s| s.split(',').map(String::from).collect())
        .unwrap_or_else(Vec::new);

    if days.len() == 0 {
        days.push(String::from("7"));
    }

    for day in days {
        match day.as_str() {
            "1" => day_01::solve(big_boy),
            "2" => day_02::solve(big_boy),
            "3" => day_03::solve(big_boy),
            "4" => day_04::solve(big_boy),
            "5" => day_05::solve(big_boy),
            "7" => day_07::solve(big_boy),
            "" | _ => eprintln!("Please provide a valid day with (--days | -d) <num1,num2>"),
        }
    }
}
