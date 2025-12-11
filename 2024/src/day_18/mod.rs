use crate::helper::input;
use std::{collections::HashSet, time::Instant};

const DAY: &str = "18";
static OFFSETS: &'static [(i64, i64)] = &[(-1, 0), (1, 0), (0, -1), (0, 1)];

fn in_grid(grid: &Vec<Vec<char>>, pos: (i64, i64)) -> bool {
    return pos.0 >= 0
        && pos.0 < (grid[0].len() as i64)
        && pos.1 >= 0
        && pos.1 < (grid.len() as i64);
}

fn get_x_y_line(line: &String) -> (usize, usize) {
    let spl: Vec<&str> = line.split(',').collect();
    let x: usize = spl[0].parse().unwrap();
    let y: usize = spl[1].parse().unwrap();
    return (x, y);
}

fn get_steps(grid: &Vec<Vec<char>>) -> i64 {
    let mut queue: Vec<(i64, i64, i64)> = vec![(0, 0, 0)];
    let mut visited: HashSet<(i64, i64)> = HashSet::new();

    while queue.len() > 0 {
        let (x, y, steps) = queue.remove(0);
        if visited.contains(&(x, y)) {
            continue;
        }

        visited.insert((x, y));
        if x == (grid[0].len() as i64 - 1) && y == (grid.len() as i64 - 1) {
            return steps;
        }

        for (dx, dy) in OFFSETS {
            let (nx, ny) = (x + dx, y + dy);
            if !in_grid(grid, (nx, ny)) || grid[ny as usize][nx as usize] == '#' {
                continue;
            }
            queue.push((nx, ny, steps + 1));
        }
    }

    return -1;
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let size: usize = 71;
    let pre_bytes: usize = 1024;
    let mut grid: Vec<Vec<char>> = vec![vec!['.'; size]; size];

    for i in 0..pre_bytes {
        let (x, y) = get_x_y_line(&lines[i]);
        grid[y][x] = '#';
    }

    let steps: i64 = get_steps(&grid);
    return steps;
}

fn solve_p2(mut lines: Vec<String>) -> String {
    let size: usize = 71;
    let mut grid: Vec<Vec<char>> = vec![vec!['.'; size]; size];

    for line in &lines {
        let (x, y) = get_x_y_line(line);
        grid[y][x] = '#';
    }

    lines.reverse();
    for line in &lines {
        let (x, y) = get_x_y_line(line);
        grid[y][x] = '.';

        let steps: i64 = get_steps(&grid);
        if steps != -1 {
            return line.clone();
        }
    }

    return String::new();
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = input::get_lines(DAY, big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: String = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
