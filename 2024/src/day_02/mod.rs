use crate::helper::input;
use std::time::Instant;

const DAY: &str = "02";

fn helper_p1(report: Vec<i64>) -> i64 {
    let mut prev: i64 = report[0];
    let mut diff: i64 = 0;

    for &num in &report[1..] {
        let new_diff: i64 = prev - num;

        if (diff < 0 && new_diff > 0)
            || (diff > 0 && new_diff < 0)
            || (new_diff.abs() == 0 || new_diff.abs() > 3)
        {
            return 0;
        }

        diff = new_diff;
        prev = num;
    }

    return 1;
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {
        let report: Vec<i64> = line
            .split_whitespace()
            .map(|s| s.trim().parse().expect("Parse error"))
            .collect();
        score += helper_p1(report);
    }

    return score;
}

fn helper_p2(report: Vec<i64>) -> i64 {
    for i in 0..report.len() {
        let mut clean: bool = true;

        let mut sub_report: Vec<i64> = report.clone();
        sub_report.remove(i);

        let mut prev: i64 = sub_report[0];
        let mut diff: i64 = 0;

        for &num in &sub_report[1..] {
            let new_diff: i64 = prev - num;

            if (diff < 0 && new_diff > 0)
                || (diff > 0 && new_diff < 0)
                || (new_diff.abs() == 0 || new_diff.abs() > 3)
            {
                clean = false;
                continue;
            }

            diff = new_diff;
            prev = num;
        }

        if clean {
            return 1;
        }
    }

    return 0;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;

    for line in lines {
        let report: Vec<i64> = line
            .split_whitespace()
            .map(|s| s.trim().parse().expect("Parse error"))
            .collect();
        score += helper_p2(report);
    }

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = input::get_lines(DAY, big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
