use std::env;

mod day_01;
mod day_02;
mod day_03;
mod day_04;
mod day_05;
mod day_06;
mod day_07;
mod day_08;
mod day_09;
mod day_10;
mod day_11;

fn main() {
    let args: Vec<String> = env::args().collect();
    let big_boy: bool = args.contains(&"--bigboy".to_string()) || args.contains(&"-bb".to_string());
    let all: bool = args.contains(&"--all".to_string()) || args.contains(&"-a".to_string());

    let mut days: Vec<String> = args
        .iter()
        .position(|arg| arg == "--days" || arg == "-d")
        .and_then(|i| args.get(i + 1))
        .map(|s| s.split(',').map(String::from).collect())
        .unwrap_or_else(Vec::new);

    if days.len() == 0 {
        days.push(String::from("11"));
    }
    if all {
        for i in 1..26 {
            days.push(i.to_string());
        }
    }
    days.sort();
    days.dedup();

    for day in days {
        match day.as_str() {
            "1" => day_01::solve(big_boy),
            "2" => day_02::solve(big_boy),
            "3" => day_03::solve(big_boy),
            "4" => day_04::solve(big_boy),
            "5" => day_05::solve(big_boy),
            "6" => day_06::solve(big_boy),
            "7" => day_07::solve(big_boy),
            "8" => day_08::solve(big_boy),
            "9" => day_09::solve(big_boy),
            "10" => day_10::solve(big_boy),
            "11" => day_11::solve(big_boy),
            "" | _ => eprintln!("Please provide a valid day with `(--days | -d) <num1,num2>`. Invalid day {} provided", day),
        }
    }
}
