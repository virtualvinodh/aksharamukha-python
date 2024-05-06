from aksharamukha import transliterate

import unittest

test_strings_rev = [
  ('ᨠᩢᨠ ᨠᩡ ᨠᩥ ᨠᩦ ᨠᩩ ᨠᩪ ᨠᩮ ᨠᩮᩡ ᨠᩰᩡ ᨠᩰ ᨠ᩠ᨿᨠ ᨠ᩠ᩅᩫᩡ ᨠ᩠ᩅᩫ ᨠ᩠ᩅᨠ', 'kaka kaḥ ki kī ku kū ke keḥ koḥ ko kèka kauḥ kau kauka'),
  ('ᨠᩰᩬᩡ ᨠᩫᨠ ᨠᩳ ᨠᩬᨠ ᨠᩯᩡ ᨠᩯ ᨠᩧ ᨠᩨ ᨠᩮᩨᩬᩡ ᨠᩮᩨᩬ ᨠᩮᩨᨠ ᨠᩱ ᨠᩱ᩠ᨿ ᨠ᩠ᩅᩭ ᨠᩭ ᨠᩴ᩠ᨿ ᨠᩮᩢᩣ', 'kǫḥ kǫḥka kǫ kǫka kæḥ kæ kư kư̄ kœḥ kœ kœka kai kaiy koi kǫi keo kao'),
  ('ᩋ ᩋᩣ ᩍ ᩎ ᩏ ᩐ ᩑ ᩋᩡ ᩒᩡ ᩑᩡ', 'a ā i ī u ū e aḥ oḥ eḥ'),
  ('ᩔ ᨬᩚ ᩈ', 'ssa ñña sa'),
  ('ᩋᩢᨠ ᩋᩡ ᩋ᩠ᨿᨠ ᩋ᩠ᩅᩫᩡ ᩋ᩠ᩅᩫ ᩋ᩠ᩅᨠ', 'aka aḥ èka auḥ au auka'),
  ('ᩋᩰᩬᩡ ᩋᩫᨠ ᩋᩳ ᩋᩬᨠ ᩋᩯᩡ ᩋᩯ ᩋᩧ ᩋᩨ ᩋᩮᩨᩬᩡ ᩋᩮᩨᩬ ᩋᩮᩨᨠ ᩋᩱ ᩋᩱ᩠ᨿ ᩋ᩠ᩅᩭ ᩋᩭ ᩋᩴ᩠ᨿ ᩋᩮᩢᩣ', 'ǫḥ ǫḥka ǫ ǫka æḥ æ ư ư̄ œḥ œ œka ai aiy oi ǫi eo ao'),
  ('ᩍ᩵ ᩍ᩶ ᩍ᩷ ᩍ᩸ ᩍ᩹', 'i′ i″ iˆ iᴶ iʵ')
]

test_strings_irrev = [
 ('ᨠᩤ', 'kā'),
  ('ᨠᨠ᩠ᨿ ᨠᨠ᩠ᩅ', 'kakya kakva')
]

test_strings_irrev = [
]
class TestStringMethods(unittest.TestCase):
  def test_tham_roman_loc(self):
    for tham, loc in test_strings_rev + test_strings_irrev:
      self.assertEqual(transliterate.process('TaiTham', 'RomanLoC', tham), loc)

  def test_roman_loc_tham(self):
    for tham, loc in test_strings_rev:
      self.assertEqual(transliterate.process('RomanLoC', 'TaiTham', loc), tham)

if __name__ == '__main__':
  unittest.main()