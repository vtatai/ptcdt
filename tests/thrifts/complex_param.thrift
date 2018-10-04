struct Xtruct {
  1: string string_thing
  4: byte byte_thing
  9: i32 i32_thing
  11: i64 i64_thing
}

struct Xtruct2 {
  1: byte byte_thing
  2: Xtruct struct_thing
  3: i32 i32_thing
}

service ThriftTest {
  void testNest(1: Xtruct thing, 2: Xtruct2 thing2)
}
