use std::{
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "_DAY_";



fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {}

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {}

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = get_lines(big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
