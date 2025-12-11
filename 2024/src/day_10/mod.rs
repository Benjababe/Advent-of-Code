use crate::helper::input;
use std::{collections::HashSet, time::Instant};

const DAY: &str = "10";
static OFFSETS: &'static [(i64, i64)] = &[(-1, 0), (1, 0), (0, -1), (0, 1)];

fn in_grid(grid: &Vec<Vec<char>>, pos: (i64, i64)) -> bool {
    return pos.0 >= 0
        && pos.0 < (grid[0].len() as i64)
        && pos.1 >= 0
        && pos.1 < (grid.len() as i64);
}

fn traverse(
    grid: &Vec<Vec<char>>,
    x: i64,
    y: i64,
    visited: &HashSet<(i64, i64)>,
) -> Vec<(i64, i64)> {
    if visited.contains(&(x, y)) || !in_grid(&grid, (x, y)) {
        return vec![];
    }
    if grid[y as usize][x as usize] == '9' {
        return vec![(x, y)];
    }

    let cur_digit = grid[y as usize][x as usize]
        .to_digit(10)
        .expect("Unable to parse digit");
    let mut peaks: Vec<(i64, i64)> = Vec::new();
    let mut new_visited: HashSet<(i64, i64)> = visited.clone();
    new_visited.insert((x, y));

    for (dx, dy) in OFFSETS {
        let (nx, ny) = (x + dx, y + dy);
        if !in_grid(&grid, (nx, ny))
            || grid[ny as usize][nx as usize] == '.'
            || grid[ny as usize][nx as usize]
                .to_digit(10)
                .expect("Unable to parse digit")
                != (cur_digit + 1)
        {
            continue;
        }

        let mut iter_peaks: Vec<(i64, i64)> = traverse(grid, nx, ny, &new_visited.clone());
        peaks.append(&mut iter_peaks);
    }

    return peaks;
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut grid: Vec<Vec<char>> = Vec::new();

    for line in lines {
        let row: Vec<char> = line.chars().collect();
        grid.push(row);
    }

    for (y, row) in grid.clone().into_iter().enumerate() {
        for (x, c) in row.into_iter().enumerate() {
            if c == '0' {
                let visited: HashSet<(i64, i64)> = HashSet::new();
                let peaks = traverse(&grid, x as i64, y as i64, &visited);

                if !p2 {
                    let peaks_set: HashSet<(i64, i64)> = peaks.into_iter().collect();
                    score += peaks_set.len() as i64;
                } else {
                    score += peaks.len() as i64;
                }
            }
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
