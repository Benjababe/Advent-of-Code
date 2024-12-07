use std::{
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

use regex::Regex;

const DAY: &str = "07";

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
        .map(|line| line.expect("Unable to read line"))
        .collect();
}

fn get_digit_count(mut num: i64) -> u32 {
    let mut count: u32 = 0;
    while num > 0 {
        num /= 10;
        count += 1;
    }
    return count;
}

fn helper(target: i64, total: i64, nums_left: &Vec<i64>, p2: bool) -> bool {
    if nums_left.len() == 0 {
        return target == total;
    }

    let num_add: i64 = total + nums_left[0];
    let num_mul: i64 = total * nums_left[0];
    let mut num_app: i64 = 0;

    if p2 {
        let digit_count: u32 = get_digit_count(nums_left[0]);
        num_app = total * 10i64.pow(digit_count) + nums_left[0];
    }

    let mut new_nums_left: Vec<i64> = nums_left.clone();
    new_nums_left.remove(0);

    return helper(target, num_add, &new_nums_left, p2)
        || helper(target, num_mul, &new_nums_left, p2)
        || (p2 && helper(target, num_app, &new_nums_left, p2));
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut target: i64 = 0;
    let re_target: Regex = Regex::new(r"^(\d+):").unwrap();
    let re_num: Regex = Regex::new(r"\s(\d+)\b").unwrap();

    for line in lines {
        if let Some(cap) = re_target.captures(line.trim()) {
            target = cap
                .get(1)
                .expect("Target was unable to be retrieved")
                .as_str()
                .parse::<i64>()
                .unwrap();
        }

        let mut nums: Vec<i64> = re_num
            .captures_iter(line.trim())
            .map(|cap| {
                cap.get(1)
                    .expect("Number was unable to be retrieved")
                    .as_str()
                    .parse::<i64>()
                    .unwrap()
            })
            .collect();

        let total: i64 = nums[0];
        nums.remove(0);

        if helper(target, total, &nums, p2) {
            score += target;
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
