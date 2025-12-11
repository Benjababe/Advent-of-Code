use crate::helper::input;
use std::{collections::HashMap, time::Instant};

const DAY: &str = "11";

fn get_int_len(n: i64) -> i64 {
    let mut count: i64 = 0;
    let mut cpy: i64 = n;

    while cpy > 0 {
        cpy /= 10;
        count += 1;
    }

    return count;
}

fn split_integer(n: i64) -> (i64, i64) {
    let i_len: i64 = get_int_len(n);
    let (mut l, mut r): (i64, i64) = (n, 0);

    for i in 0..(i_len / 2) {
        r = (l % 10) * 10_i64.pow(i as u32) + r;
        l /= 10;
    }

    return (l, r);
}

fn helper(stone: i64, blinks_left: i64, memoi: &mut HashMap<(i64, i64), i64>) -> i64 {
    let key: (i64, i64) = (stone, blinks_left);
    let n_blinks_left: i64 = blinks_left - 1;

    if memoi.contains_key(&key) {
        return *memoi.get(&key).expect("Unable to read memoised value");
    }
    if blinks_left == 0 {
        return 1;
    }

    let p: i64;
    if stone == 0 {
        p = helper(1, n_blinks_left, memoi);
    } else if (get_int_len(stone) % 2) == 0 {
        let (l, r) = split_integer(stone);
        p = helper(l, n_blinks_left, memoi) + helper(r, n_blinks_left, memoi);
    } else {
        p = helper(stone * 2024, n_blinks_left, memoi);
    }

    memoi.insert(key, p);
    return p;
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut memoi: HashMap<(i64, i64), i64> = HashMap::new();
    let blinks_left: i64 = if p2 { 75 } else { 25 };
    let line: Vec<i64> = lines[0]
        .split(' ')
        .map(|s| s.parse::<i64>().expect("Unable to parse number"))
        .collect();

    for stone in line {
        score += helper(stone, blinks_left, &mut memoi);
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
