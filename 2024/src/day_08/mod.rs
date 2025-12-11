use crate::helper::input;
use std::{
    collections::{HashMap, HashSet},
    time::Instant,
};

const DAY: &str = "08";

fn get_pair_combination(v: Vec<(i64, i64)>) -> Vec<((i64, i64), (i64, i64))> {
    let mut combinations: Vec<((i64, i64), (i64, i64))> = Vec::new();
    for l in 0..v.len() - 1 {
        let i1: (i64, i64) = v[l];
        for r in (l + 1)..v.len() {
            let i2: (i64, i64) = v[r];
            combinations.push((i1, i2));
        }
    }
    return combinations;
}

fn in_grid(grid: &Vec<Vec<char>>, pos: (i64, i64)) -> bool {
    return pos.0 >= 0
        && pos.0 < (grid[0].len() as i64)
        && pos.1 >= 0
        && pos.1 < (grid.len() as i64);
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut sources: HashMap<char, Vec<(i64, i64)>> = HashMap::new();
    let mut anti_nodes: HashSet<(i64, i64)> = HashSet::new();
    let mut grid: Vec<Vec<char>> = Vec::new();

    for (y, line) in lines.iter().enumerate() {
        let row: Vec<char> = line.chars().collect();
        for (x, c) in row.iter().enumerate() {
            if *c != '.' {
                sources
                    .entry(*c)
                    .or_insert(Vec::new())
                    .push((x as i64, y as i64));
            }
        }
        grid.push(row);
    }

    for (_, coords) in sources {
        let pairs: Vec<((i64, i64), (i64, i64))> = get_pair_combination(coords);

        for ((x1, y1), (x2, y2)) in pairs {
            let (dx, dy) = (x1 - x2, y1 - y2);
            let start_mul: i64 = if p2 { 0 } else { 1 };
            let stop_mul: i64 = if p2 { i64::MAX } else { 2 };

            for mul in start_mul..stop_mul {
                let (nx1, ny1) = (x1 + dx * mul, y1 + dy * mul);
                let (nx2, ny2) = (x2 - dx * mul, y2 - dy * mul);
                let mut done = true;

                if in_grid(&grid, (nx1, ny1)) {
                    anti_nodes.insert((nx1, ny1));
                    done = false;
                }
                if in_grid(&grid, (nx2, ny2)) {
                    anti_nodes.insert((nx2, ny2));
                    done = false;
                }

                if done {
                    break;
                }
            }
        }
    }

    return anti_nodes.len() as i64;
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
