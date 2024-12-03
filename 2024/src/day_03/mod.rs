use regex::Regex;
use std::{
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "03";

fn get_lines(big_boy: bool) -> Vec<String> {
    let filename: &str = if big_boy { "big_boy" } else { "input" };
    let input_file: String = format!("src/day_{DAY}/{filename}.txt");

    let file: File = File::open(input_file).expect("Unable to open file");
    let reader: BufReader<File> = BufReader::new(file);
    return reader
        .lines()
        .map(|line| line.expect("Unable to read line"))
        .collect();
}

fn find_all_indexes(text: &str, substring: &str) -> Vec<usize> {
    let mut indexes: Vec<usize> = Vec::new();
    let mut start: usize = 0;

    while let Some(index) = text[start..].find(substring) {
        let actual_index: usize = start + index;
        indexes.push(actual_index);
        start = actual_index + 1;
    }

    return indexes;
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
    let pattern: &str = r"mul\((\d{1,3}),(\d{1,3})\)";
    let re: Regex = Regex::new(pattern).unwrap();

    for line in lines {
        let mut cur: usize;
        let mut muls: Vec<(i64, i64)> = Vec::new();

        for (_, [l, r]) in re.captures_iter(&line).map(|c| c.extract()) {
            muls.push((l.parse::<i64>().unwrap(), r.parse::<i64>().unwrap()));
        }

        let mut do_indexes: Vec<usize> = find_all_indexes(&line, "do()");
        let mut dont_indexes: Vec<usize> = find_all_indexes(&line, "don't()");
        let mul_indexes: Vec<usize> = re.find_iter(&line).map(|m| m.start()).collect();

        for (i, v) in mul_indexes.iter().enumerate() {
            cur = *v;

            while do_indexes.len() > 0 && do_indexes[0] < *v {
                if do_indexes[0] < cur {
                    do_mul = true;
                    cur = do_indexes[0];
                }
                do_indexes.remove(0);
            }

            while dont_indexes.len() > 0 && dont_indexes[0] < *v {
                if dont_indexes[0] < cur {
                    do_mul = false;
                    cur = dont_indexes[0]
                }
                dont_indexes.remove(0);
            }

            if do_mul {
                score += muls[i].0 * muls[i].1;
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
