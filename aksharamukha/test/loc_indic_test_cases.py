from aksharamukha import transliterate

import unittest

test_strings_rev = {
  'Assamese': [('কৎ', 'kaṯ'), ('কৱ কষ', 'kawa kasha'), ('কঽ কে কো কৃ কং ওঁ', 'ka’ ke ko kr̥ kaṃ ōṃ'), ('কঁদ কঁপ কাঁ কাঁশ', 'kan̐da kan̐pa kām̐ kām̐śa'), ('কংদ কংপ', 'kaṃda kaṃpa')],
  'Balinese': [('ᬅᬜ ᬅᬗ ᬅᬯ ᬗ᬴ ᬗ᬴ᬷ ᬧ᬴ᭀ ᬚ᬴ᬾ', 'aña anga awa ‘a ‘ī fo ze'), \
               ('ᬅᭂ ᬅᭃ ᬓᭂ ᬓᭃ ᬋ ᬌ ᬍ ᬎ ᬓᬼ ᬓᬽ', 'ĕ ö kĕ kö rĕ rö lĕ lö klĕ klö'), \
                ('ᬓᬃᬧ ᬓᬧ᭄ᬭ ᬓᬧ᭄ᬬ ᬓᬵᬃᬬ', 'karpa kapra kapya kārya'), ('ᬓᬾ ᬓᭀ', 'ke ko')],
  'Bengali': [('কৎ', 'kaṯ'), ('কষ', 'kasha'), ('কঽ কে কো কৃ কং ওঁ', 'ka’ ke ko kr̥ kaṃ ōṃ'), ('কঁদ কঁপ কাঁ কাঁশ', 'kan̐da kan̐pa kām̐ kām̐śa'), ('কংদ কংপ', 'kaṃda kaṃpa')],
  'Gujarati': [('ષિષી કં કળત્ર કંય કં ઍ કૅ ઑ કૉ', 'shishī kaṃ kaḷatra kaṃya kaṃ ê kê ô kô'), ('કે કો કૃ કં ૐ', 'ke ko kr̥ kaṃ oṃ')],
  'Kannada': [('ಕಳ ಕಱೀ ಕೞ', 'kaḷa kaṟī kal̤a')],
  'Limbu': [('ᤀᤣ ᤀᤧ ᤀᤥ ᤀᤨ ᤁ᤹ᤕᤥ ᤕᤢ᤺ᤔᤠ ᤌᤠ᤺ᤒᤧ ᤁᤩ ᤁᤪ ᤁᤫ ᤁᤰ ᤁᤴ ᤁᤵ', 'e ĕ o ŏ kaḥyo yu’mā thā’bĕ kya kra kva kak kan kap')],
  'Malayalam': [('കു് കറ്റ കള കഴ', 'kȧ kaṯṯa kaḷa kaḻa')],
  'Oriya': [('କେ କୋ ୱ ଷ କଁପ କଁଝ କଁ କଁଯ', 'ke ko wa sha kan̐pa kan̐jha kam̐ kam̐ya'), ('କେ କୋ କୃ କଂ ଓଁ', 'ke ko kr̥ kaṃ oṃ')],
  'Devanagari': [('के को कृ कँय कँद कँड', 'ke ko kr̥ kam̐ya kan̐da kan̐ḍa'), ('के को कृ कं ॐ', 'ke ko kr̥ kaṃ oṃ')],
  'Gurmukhi': [('ਕਲੵ ਸ਼ ਖ਼ ਗ਼ ਵ ਅੱਧਕ ਅੱਦਕ', 'kaḷa sha k͟ha g͟ha wa addhaka addaka'), \
               ('ਅੰਯ ਅੰ ਅੰਨ ਅੰ ਕੀਂ', 'am̆ya am̆ am̆na am̆ kīṃ'), ('ਕੇ ਕੋ ਕ੍ਰੁ ਕੰ ੴ', 'ke ko kru kam̆ oṁ')],
  'Sinhala': [('ඇ ඈ කැ කෑ කළ කං කංශ', 'ă â kă kâ kaḷa kaṃ kaṃśa'), \
              ('කේ කෝ කෘ කං ඕං', 'kē kō kr̥ kaṃ ōṃ')],
  'Telugu': [('కే కో కృ కం కంశ కఁ కఁశ', 'kē kō kr̥ kaṃ kaṃśa kam̐ kam̐śa'), ('అఁగ అఁద అఁడ అఁబ అఁజ', 'an̐ga an̐da an̐ḍa an̐ba an̐ja'), ('కే కో కృ కం ఓం', 'kē kō kr̥ kaṃ ōṃ')],
  'Tibetan': [('ཅ ཆ ཇ ཇྷ ཙ ཚ ཛ ཛྷ ཤ ཉ ནྒ ཝ', 'ca cha ja jha tsa tsha dza dzha sha nya nga wa'), \
              ('ཞ ཟ འ ྅', 'zha za ’a `'), ('ཏྶ ནྱ ནྒ ནྟ ཏྭ ཏྐ', 'tʹsa nʹya nga nta twa tka'), \
                ('ཀེ ཀོ ཀྲྀ ཀཾ ༀ', 'ke ko kr̥ kaṃ oṃ')]

}

test_strings_irrev = {
  'Assamese': [],
  'Balinese': [('ᬓ᬴ ᬳ᬴ᬷ ᬕ᬴᭄ᬯ', 'kha hī ghwa'), ('ᬓᬄ ᬓᬂ ᬓᬁ', 'kah kang kang')],
  'Bengali': [('উদ্বেগ উক্বর উব্ব ভ়ুদ', 'udvega ukvara ubba vuda')],
  'Gujarati': [('કંભિ કંઘ', 'kambhi kaṅgha')],
  'Javanese': [('ꦮ ꦝ ꦄꦝ꧀ꦝ ꦄꦚꦹ ꦡ ꦛ ꦄꦛ꧀ꦛ ꦄꦔ ꦬ', 'wa dha adhdha anyu tha tha aththa anga ra'), ('ꦲ꦳ ꦏ꦳ ꦥ꦳ ꦗ꦳ ꦒ꦳ ꦔ꦳', 'ha kha fa za gha ‘a'), ('ꦏꦴ ꦏꦷ ꦏꦹ ꦏꦼ ꦏꦼꦴ ꦏꦺ ꦏꦻ ꦏꦺꦴ ꦏꦻꦴ ꦏꦸ ꦏꦹ ꦏꦁ ꦏꦀ ꦏꦃ ꦄꦏꦿ  ꦄꦂꦏ ꦄꦏ꧀ꦭ ꦄꦏꦽ ꦄꦏ꧀ꦊ ꦄꦏꦾ', 'ka ki ku kĕ kĕ ke ke ko ko ku ku kang kang kah akra  arka akla akrĕ aklĕ akya')],
  'Kannada': [('ಕಂ ಕಂಯ ಕಂಬ ಕಂಟ', 'kaṃ kaṃya kamba kaṇṭa')],
  'Limbu': [],
  'Malayalam': [('കം കംശ കംബ കംധി', 'kaṃ kaṃśa kamba kandhi')],
  'Oriya': [('କଂପ କଂଯ', 'kampa kaṃya')],
  'Devanagari': [('कं कंय कंप', 'kaṃ kaṃya kampa')],
  'Gurmukhi': [('ਅੰਪ ਕੀਂਪ', 'ampa kīmpa')],
  'Sinhala': [('අඟ අඳ අඬ අඹ අඦ', 'aṅga anda aṇḍa amba añja'), ('අංබ අංග', 'amba aṅga')],
  'Telugu': [('అంబ అంగ', 'amba aṅga')]

}

class TestStringMethods(unittest.TestCase):
  def test_indic_roman_loc(self):
    for script, test_string in test_strings_rev.items():
      for script_str, loc_str in test_string:
        self.assertEqual(transliterate.process(script, 'RomanLoC', script_str), loc_str)

    for script, test_string in test_strings_irrev.items():
      for script_str, loc_str in test_string:
        self.assertEqual(transliterate.process(script, 'RomanLoC', script_str), loc_str)

  def test_roman_loc_indic(self):
    for script, test_string in test_strings_rev.items():
      for script_str, loc_str in test_string:
        self.assertEqual(transliterate.process('RomanLoC', script, loc_str, nativize=False, post_options=['TibetanTsheg']), script_str)

  def test_balinese_simple(self):
    script = "ᬡ ᬙ ᬣ ᬰ ᬱ ᬨ ᬖ ᬪ"
    loc = "na ca ta sa sa pa gha ba"
    self.assertEqual(transliterate.process('Balinese', 'RomanLoC', script, post_options=['BalineseSimplified']), loc)

  def test_javanese_simple(self):
    script = "ꦑ ꦡ ꦯ ꦰꦴ ꦥ ꦘ ꦓ ꦨ"
    loc = "ka ta sa sa pa nya ga ba"
    self.assertEqual(transliterate.process('Javanese', 'RomanLoC', script, post_options=['JavaneseSimplified']), loc)

  def test_hindi_marathi(self):
    script = "ऎ कॆ ऍ कॅ कॉ ऑ क़ ख़ ग़ घ़ श ट़ फ़ ष स़ कळ" #ह़
    loc = "ĕ kĕ ê kê kô ô qa k͟ha g͟ha g̳h̳a śa t̤a fa sha s̤a kaḷa" #h̤a

    self.assertEqual(transliterate.process('Devanagari', 'RomanLoC', script, post_options=['HindiMarathiRomanLoCFix']), loc)

    self.assertEqual(transliterate.process('RomanLoC', 'Devanagari', loc, pre_options=['HindiMarathiRomanLoCFix']), script)

if __name__ == '__main__':
  unittest.main()