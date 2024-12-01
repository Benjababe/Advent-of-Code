use const_format::concatcp;
use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
};

const DAY: &str = "_DAY_";
const INPUT_FILE: &str = concatcp!("src/day_", DAY, "/input.txt");

fn get_lines() -> Vec<String> {
    let file = File::open(INPUT_FILE).expect("Unable to open file");
    let reader = BufReader::new(file);
    return reader
        .lines()
        .map(|line| line.expect("Unable to read line"))
        .collect();
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {
		
    }

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {
		
    }

    return score;
}

pub fn solve() {
    let lines = get_lines();

    let sc1 = solve_p1(lines.clone());
    println!("Part 1: {}", sc1);

    let sc2 = solve_p2(lines.clone());
    println!("Part 2: {}", sc2);
}
