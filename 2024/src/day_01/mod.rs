use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "01";

fn get_lines(big_boy: bool) -> Vec<String> {
    let filename: &str = if big_boy { "big_boy" } else { "input" };
    let input_file: String = format!("src/day_{DAY}/{filename}.txt");

    let file: File = File::open(input_file).expect("Unable to open file");
    let reader: BufReader<File> = BufReader::new(file);
    return reader
        .lines()
        .map(|line| line.expect("Unable to read line"))
        .collect();
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let (mut l, mut r): (Vec<i64>, Vec<i64>) = (Vec::new(), Vec::new());

    for line in lines {
        let spl: Vec<&str> = line.split("   ").collect();
        let l_num: i64 = spl[0].parse().expect("Not a valid number left");
        let r_num: i64 = spl[1].parse().expect("Not a valid number right");

        l.push(l_num);
        r.push(r_num);
    }

    l.sort();
    r.sort();

    for i in 0..l.len() {
        let diff: i64 = l[i] - r[i];
        score += diff.abs();
    }

    return score;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut l: HashSet<i64> = HashSet::new();
    let mut r: Vec<i64> = Vec::new();

    for line in lines {
        let spl: Vec<&str> = line.split("   ").collect();
        let l_num: i64 = spl[0].parse().expect("Not a valid number left");
        let r_num: i64 = spl[1].parse().expect("Not a valid number right");

        l.insert(l_num);
        r.push(r_num);
    }

    for r_num in r {
        if l.contains(&r_num) {
            score += r_num
        }
    }

    return score;
}

pub fn solve() {
    let lines: Vec<String> = get_lines(true);

    let s1: Instant = Instant::now();
    let sc1: i64 = solve_p1(lines.clone());
    let d1: std::time::Duration = s1.elapsed();
    println!("Part 1: {}, Took: {:?}", sc1, d1);

    let s2: Instant = Instant::now();
    let sc2: i64 = solve_p2(lines.clone());
    let d2: std::time::Duration = s2.elapsed();
    println!("Part 2: {}, Took: {:?}", sc2, d2);
}
