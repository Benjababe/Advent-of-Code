use crate::helper::input;
use std::{collections::HashMap, time::Instant};

const DAY: &str = "19";

fn check_possible(
    memoi: &mut HashMap<String, i64>,
    designs: &Vec<String>,
    pattern: String,
    p2: bool,
) -> i64 {
    if pattern.is_empty() {
        return 1;
    }
    if memoi.contains_key(&pattern) {
        return *memoi.get(&pattern).unwrap();
    }

    let mut possibles: i64 = 0;

    for design in designs {
        if pattern.starts_with(design) {
            let tmp_pattern: String = pattern[design.len()..].to_string();
            let p: i64 = check_possible(memoi, designs, tmp_pattern, p2);
            possibles += p;
        }
    }

    memoi.insert(pattern.to_string(), possibles);
    return if p2 { possibles } else { possibles.min(1) };
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut loop_patterns: bool = false;
    let mut designs: Vec<String> = Vec::new();
    let mut memoi: HashMap<String, i64> = HashMap::new();

    for line in lines {
        if line == "" {
            loop_patterns = true;
            continue;
        }

        if !loop_patterns {
            designs = line.split(", ").map(|s: &str| s.to_string()).collect();
        } else {
            let pattern: String = line;
            score += check_possible(&mut memoi, &designs, pattern, p2);
        }
    }

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = input::get_lines(DAY, big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p(lines.clone(), false);
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p(lines.clone(), true);
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
