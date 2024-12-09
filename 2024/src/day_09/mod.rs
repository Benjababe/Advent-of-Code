use std::{
    fs::{File, OpenOptions},
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "09";

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
    let mut score: i64 = 0;
    let mut fs: Vec<i64> = Vec::new();
    let mut fid: i64 = 0;
    let mut is_file: bool = true;
    let line: String = lines.get(0).expect("No lines found").to_string();
    let line_vec: Vec<u32> = line
        .chars()
        .map(|c| c.to_digit(10).expect("Unable to parse digit"))
        .collect();

    for i in 0..line.len() {
        for _ in 0..line_vec[i] {
            fs.push(if is_file { fid } else { -1 });
        }

        if is_file {
            fid += 1;
        }
        is_file = !is_file;
    }

    let (mut l, mut r) = (0, fs.len() - 1);
    while l < r {
        if fs[l] != -1 {
            l += 1;
            continue;
        }
        if fs[r] == -1 {
            r -= 1;
            continue;
        }
        fs.swap(l, r);
    }

    for i in 0..fs.len() {
        if fs[i] == -1 {
            continue;
        }
        score += fs[i] * (i as i64);
    }

    return score;
}

#[derive(Clone)]
struct FileBlock {
    len: i64,
    id: i64,
    file_type: String,
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut fs: Vec<FileBlock> = Vec::new();
    let mut is_file: bool = true;
    let mut fid: i64 = 0;
    let line: String = lines.get(0).expect("No lines found").to_string();
    let line_vec: Vec<u32> = line
        .chars()
        .map(|c| c.to_digit(10).expect("Unable to parse digit"))
        .collect();

    for i in 0..line.len() {
        let l: u32 = line_vec[i];

        if l > 0 {
            fs.push(FileBlock {
                len: l as i64,
                id: if is_file { fid } else { 0 },
                file_type: if is_file {
                    "file".to_string()
                } else {
                    "blank".to_string()
                },
            });
        }

        if is_file {
            fid += 1;
        }
        is_file = !is_file;
    }

    let mut r_off: usize = 0;
    while r_off < fs.len() {
        let r: usize = fs.len() - r_off - 1;

        if fs[r].file_type == "blank" || fs[r].len <= 0 {
            r_off += 1;
            continue;
        }

        for l in 0..r {
            if fs[l].file_type == "blank" && fs[l].len >= fs[r].len {
                fs[l].len -= fs[r].len;

                fs.insert(l, fs[r].clone());
                let new_len: usize = fs.len();
                fs[new_len - r_off - 1].file_type = "blank".to_string();
                fs[new_len - r_off - 1].id = 0;

                break;
            }
        }

        r_off += 1;
    }

    let mut final_fs: Vec<i64> = Vec::new();
    for f in fs {
        if f.len == 0 {
            continue;
        }
        for _ in 0..f.len {
            final_fs.push(f.id);
        }
    }
    for i in 0..final_fs.len() {
        score += final_fs[i] * (i as i64);
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
