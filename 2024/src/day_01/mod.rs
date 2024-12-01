use const_format::concatcp;
use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
};

const DAY: &str = "01";
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
    let (mut l, mut r): (Vec<i64>, Vec<i64>) = (Vec::new(), Vec::new());

    for line in lines {
        let spl: Vec<&str> = line.split("   ").collect();
        let l_num: i64 = spl[0].parse().expect("Not a valid number left");
        let r_num: i64 = spl[1].parse().expect("Not a valid number right");

        l.push(l_num);
        r.push(r_num);
    }

    l.sort();
    r.sort();

    for i in 0..l.len() {
        let diff = l[i] - r[i];
        score += diff.abs();
    }

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut l: HashSet<i64> = HashSet::new();
    let mut r: Vec<i64> = Vec::new();

    for line in lines {
        let spl: Vec<&str> = line.split("   ").collect();
        let l_num: i64 = spl[0].parse().expect("Not a valid number left");
        let r_num: i64 = spl[1].parse().expect("Not a valid number right");

        l.insert(l_num);
        r.push(r_num);
    }

    for r_num in r {
        if l.contains(&r_num) {
            score += r_num
        }
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
