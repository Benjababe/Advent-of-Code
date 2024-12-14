use std::{
    collections::HashSet,
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

use regex::Regex;

const DAY: &str = "14";

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

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut robots: Vec<(i64, i64, i64, i64)> = Vec::new();
    let (height, width): (i64, i64) = (103, 101);

    let re: Regex = Regex::new(r"p=(\d+),(\d+)\sv=(.+),(.+)").unwrap();

    for line in lines {
        if let Some(caps) = re.captures(&line) {
            let x: i64 = caps.get(1).unwrap().as_str().parse().unwrap();
            let y: i64 = caps.get(2).unwrap().as_str().parse().unwrap();
            let dx: i64 = caps.get(3).unwrap().as_str().parse().unwrap();
            let dy: i64 = caps.get(4).unwrap().as_str().parse().unwrap();
            robots.push((x, y, dx, dy));
        }
    }

    let loop_limit: i64 = if p2 { 10001 } else { 101 };
    for i in 1..loop_limit {
        let mut seen: HashSet<(i64, i64)> = HashSet::new();
        let mut no_overlap: bool = true;

        for j in 0..robots.len() {
            let (x, y, dx, dy) = robots[j];
            let mut nx: i64 = (x + dx) % width;
            let mut ny: i64 = (y + dy) % height;

            if nx < 0 {
                nx += width;
            }
            if ny < 0 {
                ny += height;
            }

            robots[j] = (nx, ny, dx, dy);

            if seen.contains(&(nx, ny)) {
                no_overlap = false;
            }
            seen.insert((nx, ny));
        }

        if no_overlap && p2 {
            return i;
        }
    }

    let mut quads: Vec<i64> = vec![0, 0, 0, 0];
    for (x, y, _, _) in robots {
        let (mid_x, mid_y): (i64, i64) = (width / 2, height / 2);

        if x < mid_x && y < mid_y {
            quads[0] += 1;
        } else if x > mid_x && y < mid_y {
            quads[1] += 1;
        } else if x > mid_x && y > mid_y {
            quads[2] += 1;
        } else if x < mid_x && y > mid_y {
            quads[3] += 1;
        }
    }

    return quads[0] * quads[1] * quads[2] * quads[3];
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = get_lines(big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p(lines.clone(), false);
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p(lines.clone(), true);
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
