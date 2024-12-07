use std::{
    cmp::Ordering,
    collections::{HashMap, HashSet},
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

const DAY: &str = "05";

fn get_lines(big_boy: bool) -> Vec<String> {
    let filename: &str = if big_boy { "bigboy" } else { "input" };
    let input_file: String = format!("src/day_{DAY}/{filename}.txt");

    let file: File = File::open(input_file).expect("Unable to open file");
    let reader: BufReader<File> = BufReader::new(file);
    return reader
        .lines()
        .map(|line| String::from(line.expect("Unable to read line").trim()))
        .collect();
}

fn solve_p1(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut phase_one: bool = true;
    let mut map: HashMap<String, HashSet<String>> = HashMap::new();

    for line in lines {
        if line.trim().len() == 0 {
            phase_one = false;
            continue;
        }

        if phase_one {
            let spl: Vec<&str> = line.split("|").collect();
            map.entry(spl[0].to_string())
                .or_default()
                .insert(spl[1].to_string());
        } else {
            let mut seen: HashSet<String> = HashSet::new();
            let mut fault: bool = false;
            let nums: Vec<&str> = line.split(",").collect();

            for num in &nums {
                seen.insert(num.to_string());

                if map.contains_key(*num) {
                    let set: Option<&HashSet<String>> = map.get(*num);
                    let intersection: HashSet<_> =
                        set.unwrap().intersection(&seen).cloned().collect();
                    if intersection.len() > 0 {
                        fault = true;
                    }
                }
            }

            if !fault {
                let num: &str = nums[nums.len() / 2];
                score += num.parse::<i64>().expect("Failed to parse str to i64");
            }
        }
    }

    return score;
}

fn valid(nums: &Vec<&str>, map: &HashMap<String, HashSet<String>>) -> bool {
    let mut seen: HashSet<String> = HashSet::new();

    for num in nums {
        seen.insert(num.to_string());

        if map.contains_key(*num) {
            let set: Option<&HashSet<String>> = map.get(*num);
            let intersection: HashSet<_> = set.unwrap().intersection(&seen).cloned().collect();
            if intersection.len() > 0 {
                return false;
            }
        }
    }

    return true;
}

fn solve_p2(lines: Vec<String>) -> i64 {
    let mut score: i64 = 0;
    let mut phase_one: bool = true;
    let mut map: HashMap<String, HashSet<String>> = HashMap::new();

    for line in lines {
        if line.trim().len() == 0 {
            phase_one = false;
            continue;
        }

        if phase_one {
            let spl: Vec<&str> = line.split("|").collect();
            map.entry(spl[0].to_string())
                .or_default()
                .insert(spl[1].to_string());
        } else {
            let mut nums: Vec<&str> = line.split(",").collect();

            if !valid(&nums, &map) {
                nums.sort_by(|n1, n2| {
                    if map.contains_key(*n1) {
                        let set: &HashSet<String> = map.get(*n1).unwrap();
                        if set.contains(*n2) {
                            return Ordering::Less;
                        }
                    }
                    return Ordering::Greater;
                });

                let num: &str = nums[nums.len() / 2];
                score += num.parse::<i64>().expect("Failed to parse str to i64");
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
