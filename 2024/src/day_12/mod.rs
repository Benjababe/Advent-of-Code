use std::{
    collections::{HashMap, HashSet},
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "12";
static OFFSETS: &'static [(i64, i64)] = &[(-1, 0), (1, 0), (0, -1), (0, 1)];

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
        && pos.0 < (grid[0].len() as i64)
        && pos.1 >= 0
        && pos.1 < (grid.len() as i64);
}

fn get_perimieter(grid: &Vec<Vec<char>>, x: i64, y: i64) -> i64 {
    let (ux, uy) = (x as usize, y as usize);
    let c: char = grid[uy][ux];
    let mut peri: i64 = 4;

    if x > 0 && grid[uy][ux - 1] == c {
        peri -= 1;
    }
    if x < (grid[0].len() as i64 - 1) && grid[uy][ux + 1] == c {
        peri -= 1;
    }
    if y > 0 && grid[uy - 1][ux] == c {
        peri -= 1;
    }
    if y < (grid.len() as i64 - 1) && grid[uy + 1][ux] == c {
        peri -= 1
    }

    return peri;
}

fn get_corners(grid: &Vec<Vec<char>>, x: i64, y: i64) -> i64 {
    let (ux, uy) = (x as usize, y as usize);
    let c: char = grid[uy][ux];
    let mut corners: i64 = 0;

    // Outer corners
    // Top left
    if (y <= 0 || grid[uy - 1][ux] != c) && (x <= 0 || grid[uy][ux - 1] != c) {
        corners += 1;
    }
    // Top right
    if (y <= 0 || grid[uy - 1][ux] != c) && (ux == (grid[0].len() - 1) || grid[uy][ux + 1] != c) {
        corners += 1;
    }
    // Bottom left
    if (uy == (grid.len() - 1) || grid[uy + 1][ux] != c) && (x <= 0 || grid[uy][ux - 1] != c) {
        corners += 1;
    }
    // Bottom right
    if (uy == (grid.len() - 1) || grid[uy + 1][ux] != c)
        && (ux == (grid[0].len() - 1) || grid[uy][ux + 1] != c)
    {
        corners += 1;
    }

    // Inner corners
    // Top corners
    if y > 0 && grid[uy - 1][ux] == c {
        // Left
        if x > 0 && grid[uy][ux - 1] == c && grid[uy - 1][ux - 1] != c {
            corners += 1
        }
        // Right
        if ux < (grid[0].len() - 1) && grid[uy][ux + 1] == c && grid[uy - 1][ux + 1] != c {
            corners += 1
        }
    }

    // Bottom corners
    if uy < (grid.len() - 1) && grid[uy + 1][ux] == c {
        if x > 0 && grid[uy][ux - 1] == c && grid[uy + 1][ux - 1] != c {
            corners += 1
        }
        if ux < (grid[0].len() - 1) && grid[uy][ux + 1] == c && grid[uy + 1][ux + 1] != c {
            corners += 1;
        }
    }

    return corners;
}

fn traverse(
    grid: &Vec<Vec<char>>,
    x: i64,
    y: i64,
    visited: &mut HashSet<(i64, i64)>,
    areas: &mut HashMap<char, i64>,
    multiplier: &mut HashMap<char, i64>,
    p2: bool,
) {
    if visited.contains(&(x, y)) || !in_grid(&grid, (x, y)) {
        return;
    }

    let c: char = grid[y as usize][x as usize];

    if !p2 {
        *multiplier.entry(c).or_default() += get_perimieter(&grid, x, y);
    } else {
        *multiplier.entry(c).or_default() += get_corners(&grid, x, y);
    }
    *areas.entry(c).or_default() += 1;
    visited.insert((x, y));

    for (dx, dy) in OFFSETS {
        let (nx, ny) = (x + dx, y + dy);
        if !in_grid(grid, (nx, ny))
            || grid[ny as usize][nx as usize] != grid[y as usize][x as usize]
        {
            continue;
        }

        traverse(grid, nx, ny, visited, areas, multiplier, p2);
    }
}

fn solve_p(lines: Vec<String>, p2: bool) -> i64 {
    let mut score: i64 = 0;
    let mut visited: HashSet<(i64, i64)> = HashSet::new();
    let mut grid: Vec<Vec<char>> = Vec::new();

    for line in lines {
        let row: Vec<char> = line.chars().collect();
        grid.push(row);
    }

    for (y, row) in grid.clone().into_iter().enumerate() {
        for (x, _) in row.into_iter().enumerate() {
            let mut areas: HashMap<char, i64> = HashMap::new();
            let mut multiplier: HashMap<char, i64> = HashMap::new();

            traverse(
                &grid,
                x as i64,
                y as i64,
                &mut visited,
                &mut areas,
                &mut multiplier,
                p2,
            );

            for (k, v) in multiplier.iter() {
                score += v * areas[k];
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
