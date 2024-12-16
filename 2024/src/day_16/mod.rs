use std::{
    collections::HashSet,
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "16";

static OFFSETS: &'static [(i64, i64)] = &[(1, 0), (0, -1), (-1, 0), (0, 1)];

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

    let mut queue: Vec<(i64, i64, i64, i64, Vec<(i64, i64)>)> = vec![(0, 0, x, y, vec![])];

    while queue.len() > 0 {
        let (points, dir, x, y, path) = queue.remove(0);

        if grid[y as usize][x as usize] == 'E' {
            if p2 {
                for (px, py) in path {
                    best_spots.insert((px, py));
                }

                while queue.len() > 0 && queue[0].0 == points {
                    let (_, _, tx, ty, t_path) = queue.remove(0);
                    if tx != x || ty != y {
                        continue;
                    }

                    for (px, py) in t_path {
                        best_spots.insert((px, py));
                    }
                }

                return (best_spots.len() as i64) + 1;
            } else {
                return points;
            }
        }

        for rot in -1_i64..2_i64 {
            let mut tmp_dir: i64 = (dir + rot) % 4;
            if tmp_dir < 0 {
                tmp_dir += 4;
            }
            let tmp_points: i64 = rot.abs() * 1000 + points + 1;
            let (dx, dy) = OFFSETS[tmp_dir as usize];

            if grid[(y + dy) as usize][(x + dx) as usize] != '#'
                && !visited.contains(&(tmp_dir, x + dx, y + dy))
            {
                let mut new_path: Vec<(i64, i64)> = path.clone();
                new_path.push((x, y));
                queue.push((tmp_points, tmp_dir, x + dx, y + dy, new_path));
            }
        }

        visited.insert((dir, x, y));
        queue.sort_by(|a, b| a.0.cmp(&b.0));
    }

    return 0;
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
