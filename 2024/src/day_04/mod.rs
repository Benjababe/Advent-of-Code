use std::{
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "04";

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

fn solve_p1(lines: Vec<String>) -> i64 {
    const PADDING: usize = 4;
    let mut score: i64 = 0;
    let l: usize = if lines.len() > 0 { lines[0].len() } else { 0 };

    let offsets: Vec<((i64, i64), (i64, i64), (i64, i64))> = vec![
        ((0, -1), (0, -2), (0, -3)),
        ((0, 1), (0, 2), (0, 3)),
        ((-1, 0), (-2, 0), (-3, 0)),
        ((1, 0), (2, 0), (3, 0)),
        ((-1, -1), (-2, -2), (-3, -3)),
        ((-1, 1), (-2, 2), (-3, 3)),
        ((1, -1), (2, -2), (3, -3)),
        ((1, 1), (2, 2), (3, 3)),
    ];

    let mut lines_cl: Vec<Vec<char>> = lines
        .into_iter()
        .map(|line| line.chars().collect())
        .collect();

    for _i in 0..PADDING {
        lines_cl.insert(0, vec![' '; l]);
        lines_cl.push(vec![' '; l]);
    }
    for i in 0..lines_cl.len() {
        for _i in 0..PADDING {
            lines_cl[i].insert(0, ' ');
            lines_cl[i].push(' ');
        }
    }

    for y in PADDING..(lines_cl.len() - PADDING) {
        for x in PADDING..(lines_cl[y].len() - PADDING) {
            if lines_cl[y][x] != 'X' {
                continue;
            }

            let y_i: i64 = y as i64;
            let x_i: i64 = x as i64;

            for offset in offsets.iter() {
                if lines_cl[(y_i + offset.0 .0) as usize][(x_i + offset.0 .1) as usize] == 'M'
                    && lines_cl[(y_i + offset.1 .0) as usize][(x_i + offset.1 .1) as usize] == 'A'
                    && lines_cl[(y_i + offset.2 .0) as usize][(x_i + offset.2 .1) as usize] == 'S'
                {
                    score += 1;
                }
            }
        }
    }

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    const PADDING: usize = 1;
    let mut score: i64 = 0;
    let l: usize = if lines.len() > 0 { lines[0].len() } else { 0 };

    let mut lines_cl: Vec<Vec<char>> = lines
        .into_iter()
        .map(|line| line.chars().collect())
        .collect();

    for _i in 0..PADDING {
        lines_cl.insert(0, vec![' '; l]);
        lines_cl.push(vec![' '; l]);
    }
    for i in 0..lines_cl.len() {
        for _i in 0..PADDING {
            lines_cl[i].insert(0, ' ');
            lines_cl[i].push(' ');
        }
    }

    for y in PADDING..(lines_cl.len() - PADDING) {
        for x in PADDING..(lines_cl[y].len() - PADDING) {
            if lines_cl[y][x] != 'A' {
                continue;
            }

            let tl: char = lines_cl[y - 1][x - 1];
            let bl: char = lines_cl[y + 1][x - 1];
            let tr: char = lines_cl[y - 1][x + 1];
            let br: char = lines_cl[y + 1][x + 1];

            if tl == 'M' && bl == 'S' && tr == 'M' && br == 'S' {
                score += 1
            }
            if tl == 'S' && bl == 'S' && tr == 'M' && br == 'M' {
                score += 1
            }
            if tl == 'M' && bl == 'M' && tr == 'S' && br == 'S' {
                score += 1
            }
            if tl == 'S' && bl == 'M' && tr == 'S' && br == 'M' {
                score += 1
            }
        }
    }

    return score;
}

pub fn solve(big_boy: bool) {
    let lines: Vec<String> = get_lines(big_boy);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Day {} Part 1: {}, Took: {:?}", DAY, sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Day {} Part 2: {}, Took: {:?}", DAY, sc2, d2);
}
