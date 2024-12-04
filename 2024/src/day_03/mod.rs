use regex::Regex;
use std::{
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "03";

fn get_lines(big_boy: bool) -> Vec<String> {
    let filename: &str = if big_boy { "bigboy" } else { "input" };
    let input_file: String = format!("src/day_{DAY}/{filename}.txt");

    let file: File = File::open(input_file).expect("Unable to open file");
    let reader: BufReader<File> = BufReader::new(file);
    return reader
        .lines()
        .map(|line| line.expect("Unable to read line"))
        .collect();
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let pattern: &str = r"mul\((\d{1,3}),(\d{1,3})\)";
    let re: Regex = Regex::new(pattern).unwrap();

    for line in lines {
        for matches in re.captures_iter(&line) {
            let l: i64 = matches[1].parse().unwrap();
            let r: i64 = matches[2].parse().unwrap();
            score += l * r;
        }
    }

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut do_mul: bool = true;
    let pattern: &str = r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)";
    let re: Regex = Regex::new(pattern).unwrap();

    for line in lines {
        for matches in re.captures_iter(&line) {
            if matches[0].to_string() == "do()" {
                do_mul = true;
            } else if matches[0].to_string() == "don't()" {
                do_mul = false;
            } else if do_mul {
                let l: i64 = matches[1].parse().unwrap();
                let r: i64 = matches[2].parse().unwrap();
                score += l * r;
            }
        }
    }

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = get_lines(big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Part 1: {}, Took: {:?}", sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Part 2: {}, Took: {:?}", sc2, d2);
}
