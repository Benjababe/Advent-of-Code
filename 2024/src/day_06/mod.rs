use std::{
    collections::HashSet,
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "06";

static OFFSETS: &'static [(i64, i64)] = &[(0, -1), (1, 0), (0, 1), (-1, 0)];

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

fn in_grid(grid: &Vec<Vec<char>>, pos: (i64, i64)) -> bool {
    return pos.0 >= 0
        && (pos.0 as usize) < grid[0].len()
        && pos.1 >= 0
        && (pos.1 as usize) < grid.len();
}

fn get_new_pos(pos: (i64, i64), dir: usize) -> (i64, i64) {
    return (pos.0 + OFFSETS[dir].0, pos.1 + OFFSETS[dir].1);
}

fn helper(
    grid: &Vec<Vec<char>>,
    init: (i64, i64),
    dir: usize,
    obstacle: (i64, i64),
) -> (i64, bool) {
    let mut pos: (i64, i64) = init.clone();
    let mut cur_dir: usize = dir;
    let mut visited: HashSet<(i64, i64)> = HashSet::new();
    let mut loop_visited: HashSet<(i64, i64, usize)> = HashSet::new();
    let mut in_loop: bool = false;

    while in_grid(&grid, pos) && !in_loop {
        visited.insert(pos);
        loop_visited.insert((pos.0, pos.1, cur_dir));

        let new_pos: (i64, i64) = get_new_pos(pos, cur_dir);
        if !in_grid(&grid, new_pos) {
            break;
        }

        if (grid[new_pos.1 as usize][new_pos.0 as usize] == '#')
            || (new_pos.0 == obstacle.0 && new_pos.1 == obstacle.1)
        {
            cur_dir = (cur_dir + 1) % 4;
        } else {
            pos = new_pos;
            in_loop = loop_visited.contains(&(pos.0, pos.1, cur_dir));
        }
    }

    return (visited.len() as i64, in_loop);
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut init: (i64, i64) = (0, 0);
    let mut grid: Vec<Vec<char>> = Vec::new();

    for (y, line) in lines.iter().enumerate() {
        let row: Vec<char> = line.chars().collect();
        for (x, c) in row.iter().enumerate() {
            if *c == '^' {
                init = (x as i64, y as i64);
            }
        }
        grid.push(row);
    }

    if !p2 {
        let (walked, _): (i64, bool) = helper(&grid, init, 0, (-1, -1));
        return walked;
    }

    let height: usize = grid.len();
    let width: usize = grid[0].len();

    for y in 0..height {
        for x in 0..width {
            let (_, in_loop): (_, bool) = helper(&grid, init, 0, (x as i64, y as i64));
            if in_loop {
                score += 1;
            }
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
