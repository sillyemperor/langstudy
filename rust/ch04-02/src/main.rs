fn main() {
  let s = String::from("hello");
  let s1 = &s[1..3];
  s.clear();
  println!("{}", s1);
}

