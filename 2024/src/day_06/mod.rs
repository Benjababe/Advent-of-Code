use std::{
    collections::HashSet,
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "06";

static OFFSETS: &'static [(i8, i8)] = &[(0, -1), (1, 0), (0, 1), (-1, 0)];

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

fn in_grid(grid: &Vec<Vec<char>>, pos: (i8, i8)) -> bool {
    return pos.0 >= 0
        && (pos.0 as usize) < grid[0].len()
        && pos.1 >= 0
        && (pos.1 as usize) < grid.len();
}

fn get_new_pos(pos: (i8, i8), dir: usize) -> (i8, i8) {
    OFFSETS[0].0;
    return (pos.0 + OFFSETS[dir].0, pos.1 + OFFSETS[dir].1);
}

fn helper(
    grid: &Vec<Vec<char>>,
    init: (i8, i8),
    dir: usize,
    obstacle: (usize, usize),
) -> (i64, bool) {
    let mut pos: (i8, i8) = init.clone();
    let mut cur_dir: usize = dir;
    let mut visited: HashSet<(i8, i8)> = HashSet::new();
    let mut loop_visited: HashSet<(i8, i8, usize)> = HashSet::new();
    let mut in_loop: bool = false;

    while in_grid(&grid, pos) && !in_loop {
        visited.insert(pos);
        loop_visited.insert((pos.0, pos.1, cur_dir));

        let new_pos: (i8, i8) = get_new_pos(pos, cur_dir);
        if grid[new_pos.1 as usize][new_pos.0 as usize] == '#' {
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
    let mut init: (i8, i8) = (0, 0);
    let mut grid: Vec<Vec<char>> = Vec::new();

    for (y, line) in lines.iter().enumerate() {
        let row: Vec<char> = line.chars().collect();
        for (x, c) in row.iter().enumerate() {
            if *c == '^' {
                init = (x as i8, y as i8);
            }
        }
        grid.push(row);
    }

    if !p2 {
        let (walked, _): (i64, bool) = helper(&grid, init, 0, (0, 0));
        return walked;
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
