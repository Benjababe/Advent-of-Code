use std::{
    collections::{HashMap, HashSet},
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "22";

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

fn mix(secret: i64, v: i64) -> i64 {
    return secret ^ v;
}

fn prune(secret: i64) -> i64 {
    return secret % 16777216;
}

fn process(secret: i64) -> i64 {
    let s1: i64 = prune(mix(secret, secret * 64));
    let s2: i64 = prune(mix(s1, s1 / 32));
    return prune(mix(s2, s2 * 2048));
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut seq_map: HashMap<(i64, i64, i64, i64), i64> = HashMap::new();
    let limit: usize = 2000;

    for line in lines {
        let mut secret: i64 = line.parse().unwrap();
        let mut history: Vec<i64> = vec![secret % 10];
        let mut used: HashSet<(i64, i64, i64, i64)> = HashSet::new();

        for _ in 0..limit {
            secret = process(secret);

            if !p2 {
                continue;
            }

            history.push(secret % 10);
            if history.len() < 5 {
                continue;
            }
            while history.len() > 5 {
                history.remove(0);
            }

            let seq: (i64, i64, i64, i64) = (
                history[1] - history[0],
                history[2] - history[1],
                history[3] - history[2],
                history[4] - history[3],
            );
            if used.contains(&seq) {
                continue;
            }

            used.insert(seq);
            *seq_map.entry(seq).or_insert(0) += history[4] % 10;
        }

        if !p2 {
            score += secret;
        }
    }

    if p2 {
        for val in seq_map.values() {
            if *val > score {
                score = *val;
            }
        }
    }

    return score;
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
