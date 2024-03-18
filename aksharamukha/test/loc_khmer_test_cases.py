from aksharamukha import transliterate

import unittest

test_strings_rev = [
  ('អ អា អិ អី អុ អូ អេ អោ អៃ អៅ អំ អះ', '‛a ‛ā ‛i ‛ī ‛u ‛ū ‛e ‛o ‛ai ‛au ‛aṃ ‛aḥ'),
  ('អឹ អឺ អែ អៀ អឿ អើ', '‛ẏ ‛ȳ ‛ae ‛ia ‛ẏa ‛oe'),
  ('អ័ អ៍ អ៎ ខ័អ', '‛ă ‛a˚ ‛a’ khă‛ʹ'),
  ('ជ្អ ផ្អា ខ្អេ ជជ្អ', 'j‛a ph‛ā kh‛e jaj‛ʹ'),
  ('អ៊ អ៊ា អ៊ូ', '‛′a ‛′ā ‛′ū'),
  ('ឥ ឦ ឧ ឩ ឬ ឫ ឮ ឯ ឰ ឱ ឳ ឪ', 'i ī u ū ṝ ṛ ḹ ae ai o au ýu'),
  ('គ គា គិ គី គុ គូ គេ គៃ គោ គៅ កំ គះ', 'ga gā gi gī gu gū ge gai go gau kaṃ gaḥ'),
  ('កឹ គឺ គែ គៀ គឿ ឈើ', 'kẏ gȳ gae gia gẏa jhoe'),
  ('គ័ គ័ខ', 'gă găkh'),
  ('គគ៍ ខខ៎ ខខ៏ គ៍គ ខ៎ ខ៏ គខ៏ អ្នករ៉ូ', 'gag˚ khakh’ khakhʻ ga˚g kha’ khaʻ gakhʻ ‛ʹnakar″ū'),
  ('ជោះ', 'joaḥ'),
  ('អាឃ់ខ អៈឃ អខ់', '‛âghakh ‛àgh ‛ákh'),
  ('គ គខ ឋ៎ សទ្រ', 'ga gakh ṭha’ sadr'),
  ('ពឋ៎ឋ ពឋ៎ ឋ៎ព ឋ៎ឋ៎ ពឋ៏ឋ ពឋ៏ ឋ៏ព ឋ៏ឋ៏ ជក៌ឋ ជខ៌', 'baṭha’ṭh baṭh’ ṭha’b ṭha’ṭh’ baṭhaʻṭh baṭhʻ ṭhaʻb ṭhaʻṭhʻ jarkaṭh jarkh'),
  ('ទឆ៍ ឆឈ៎ វ៉វ៉', 'dach˚ chajh’ v″av″'),
  ('ឋវ៉ឋ ឋវ៉ ង៉ង៉ ង៉', 'ṭhav″aṭh ṭhav″ ṅ″aṅ″ ṅ″a'),
  ('ដល់ អធិបតេយ្យ', 'ṭál ‛adhipateyy'),
  ('ឆយ៍ តត់ កិក់ គគ់្ខ', 'chay˚ tát kík gágkh'),
  ('តត់ កិក់ សាគ់', 'tát kík sâg'),
  ('អាឃ់ខ អៈឃ អខ់', '‛âghakh ‛àgh ‛ákh'),
  ('ហអ្ន អ្នា ហខ្អ ហខ្អេ', 'ha‛ʹn ‛ʹnā hakh‛ʹ hakh‛e'),
  ('ក្រខ្វាក់ ក្សត្រិយ៍ សុី បុឹ អាត្ម័ន តត់ កាគ់', 'krakhvâk ksatriy˚ s′ī p″ẏ ‛ātmăn tát kâg')
]

test_strings_irrev = [
  ('តត់ កិក់ គគ់្ខ គក្ខ់ សាគ់', 'tát kík gágkh gákkh sâg'),
  ('៖ ៕ ។', ': . .'),
  ('ឲ្យ ឱ្យ', 'oy oy'),
  ('ឭ', 'ḷ')
]
class TestStringMethods(unittest.TestCase):
  def test_khmer_roman_loc(self):
    for khmer, loc in test_strings_rev + test_strings_irrev:
      self.assertEqual(transliterate.process('Khmer', 'RomanLoC', khmer), loc)

  def test_roman_loc_khmer(self):
    for khmer, loc in test_strings_rev:
      self.assertEqual(transliterate.process('RomanLoC', 'Khmer', loc), khmer)

if __name__ == '__main__':
  unittest.main()