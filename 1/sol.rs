use std::io::{self, BufRead};
use std::collections::HashMap;


fn parse_string_nums(s: &str, snums: &HashMap<&str, &str>) -> String {
    let mn = snums
        .keys()
        .filter_map(|snum| s.find(snum).map(|i| (i, snum)))
        .min();

    let mx = snums
        .keys()
        .filter_map(|snum| s.rfind(snum).map(|i| (i , snum)))
        .max();

    if mn.is_none() {
        s.to_string()
    } else if mx == mn {
        let (i, sn) = mn.unwrap();
        format!("{}{}{}", &s[..i], snums[sn], &s[i + sn.len()..])
    } else {
        let (li, lsn) = mn.unwrap();
        let (ri, rsn) = mx.unwrap();
        let left = format!("{}{}", &s[..li], snums[lsn]);
        let mid = if li + lsn.len() <= ri{
            format!("{}", &s[li + lsn.len()..ri])
        } else {
            "".to_string()
        };
        let right = format!("{}{}{}", &s[ri..], snums[rsn], &s[ri + rsn.len()..]);
        format!("{}{}{}", left, mid, right)
    }
}

fn calibration(line: &str) -> usize {
    let digits = line
        .chars()
        .filter(|c| c.is_digit(10))
        .collect::<Vec<_>>();
    let fst = digits.first().unwrap().to_digit(10).unwrap() as usize;
    let snd = digits.last().unwrap().to_digit(10).unwrap() as usize;
    return fst * 10 + snd;
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .filter_map(|res_s| res_s.ok())
        .collect::<Vec<_>>();

    let mut snums = HashMap::new();
    snums.insert("one",   "1");
    snums.insert("two",   "2");
    snums.insert("three", "3");
    snums.insert("four",  "4");
    snums.insert("five",  "5");
    snums.insert("six",   "6");
    snums.insert("seven", "7");
    snums.insert("eight", "8");
    snums.insert("nine",  "9");

    // p1
    let p1 = lines
        .iter()
        .map(|s| calibration(s))
        .sum::<usize>();
    println!("{:?}", p1);

    // p2
    let p2 = lines
        .iter()
        .map(|s| calibration(&parse_string_nums(s, &snums)))
        .sum::<usize>();
    println!("{:?}", p2);
    
    Ok(())
}
