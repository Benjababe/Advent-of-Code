use crate::helper::input;
use priority_queue::PriorityQueue;
use std::{cmp::Reverse, collections::HashSet, time::Instant};

const DAY: &str = "16";

static OFFSETS: &'static [(i64, i64)] = &[(1, 0), (0, -1), (-1, 0), (0, 1)];

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut visited: HashSet<(i64, i64, i64)> = HashSet::new();
    let mut best_spots: HashSet<(i64, i64)> = HashSet::new();
    let mut grid: Vec<Vec<char>> = Vec::new();
    let (mut x, mut y): (i64, i64) = (1, 1);

    for (ty, line) in lines.iter().enumerate() {
        let row: Vec<char> = line.chars().collect();
        for (tx, c) in row.iter().enumerate() {
            if *c == 'S' {
                x = tx as i64;
                y = ty as i64;
            }
        }
        grid.push(row);
    }

    let mut p_queue: PriorityQueue<(i64, i64, i64, Vec<(i64, i64)>), Reverse<i64>> =
        PriorityQueue::new();
    p_queue.push((0, x, y, vec![]), Reverse(0));

    while p_queue.len() > 0 {
        let ((dir, x, y, path), points) = p_queue.pop().unwrap();

        if grid[y as usize][x as usize] == 'E' {
            if p2 {
                for (px, py) in path {
                    best_spots.insert((px, py));
                }

                while p_queue.len() > 0 {
                    let ((_, tx, ty, t_path), t_points) = p_queue.pop().unwrap();
                    if points.0 != t_points.0 {
                        break;
                    }
                    if tx != x || ty != y {
                        continue;
                    }

                    for (px, py) in t_path {
                        best_spots.insert((px, py));
                    }
                }

                return (best_spots.len() as i64) + 1;
            } else {
                return points.0;
            }
        }

        for rot in -1_i64..2_i64 {
            let mut tmp_dir: i64 = (dir + rot) % 4;
            if tmp_dir < 0 {
                tmp_dir += 4;
            }
            let tmp_points: i64 = rot.abs() * 1000 + points.0 + 1;
            let (dx, dy) = OFFSETS[tmp_dir as usize];

            if grid[(y + dy) as usize][(x + dx) as usize] != '#'
                && !visited.contains(&(tmp_dir, x + dx, y + dy))
            {
                let mut new_path: Vec<(i64, i64)> = path.clone();
                new_path.push((x, y));
                p_queue.push((tmp_dir, x + dx, y + dy, new_path), Reverse(tmp_points));
            }
        }

        visited.insert((dir, x, y));
    }

    return 0;
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
