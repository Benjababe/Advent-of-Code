use std::{
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "25";

fn get_lines(big_boy: bool) -> Vec<String> {
    let filename: &str = if big_boy { "bigboy" } else { "input" };
    let input_file: String = format!("src/day_{DAY}/{filename}.txt");

    OpenOptions::new()
        .write(true)
        .create(true)
        .open(input_file.clone())
        .expect("Unable to open file");

    let file: File = File::open(input_file.clone()).expect("Unable to open file");

    let reader: BufReader<File> = BufReader::new(file);
    return reader
        .lines()
        .map(|line| String::from(line.expect("Unable to read line").trim()))
        .collect();
}

fn solve_p(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut i: usize = 0;
    let mut locks: Vec<Vec<i64>> = Vec::new();
    let mut keys: Vec<Vec<i64>> = Vec::new();
    let max_h: i64 = 5;

    while i < lines.len() {
        let mut tmp_lines: Vec<String> = Vec::new();
        let mut v: Vec<i64> = Vec::new();
        let out: &mut Vec<Vec<i64>>;

        while i < lines.len() && lines[i].trim().len() != 0 {
            tmp_lines.push(lines[i].clone());
            i += 1;
        }

        if tmp_lines[0].chars().nth(0).unwrap() == '#' {
            out = &mut locks;
        } else {
            out = &mut keys;
            tmp_lines.reverse();
        }

        for x in 0..tmp_lines[0].len() {
            let mut h: i64 = 0;
            for y in 1..tmp_lines.len() {
                if tmp_lines[y].chars().nth(x).unwrap() == '#' {
                    h += 1;
                }
            }
            v.push(h);
        }

        (*out).push(v);
        i += 1;
    }

    for key in keys {
        for lock in locks.clone() {
            let mut can: bool = true;
            for i in 0..key.len() {
                if (key[i] + lock[i]) > max_h {
                    can = false;
                }
            }

            if can {
                score += 1;
            }
        }
    }

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = get_lines(big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);
}
