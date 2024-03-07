from aksharamukha import transliterate

import unittest

class TestStringMethods(unittest.TestCase):

    def test_a(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'အ'), '’a')

    def test_au(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ဩ ဪ ကော ကော်'), 'o oʻ ko koʻ')

    def test_anusvara(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ကံ ကာံ အံ အိုံ'), 'kaṃ kāṃ ’aṃ ’uiṃ')

    def test_vowels(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'အ အာ အိ အီ အု အူ အေ အဲ အော အော် အို'), \
            '’a ’ā ’i ’ī ’u ’ū ’e ’ai ’o ’oʻ ’ui')

    def test_subjoined(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'မျှ ကြွ လွှ မြွှင်း'), \
            'myha krva lvha mrvhaṅʻʺ')

    def test_virama_final(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'တက္ကသိုလ် တိရစ္ဆာန်'), \
            'takkasuilʻ tiracchānʻ')

    def test_superscript(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'သင်္ဃ ဓရ်္မ'), \
            'saṅgha dharma')

    def test_ui(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'အို တို ကို'), \
            '’ui tui kui')

    def test_tone_1(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ပို့ ပိုး'), \
            'puiʹ puiʺ')

    def test_tone_2(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ပင့်'), \
            'paṅʻʹ')

    def test_great_ssa_nna(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'တဿ ပညာ'), \
            'tassa paññā')

    def test_abbr(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', '၏ ၍ ၌ ၎'), \
            'e* r* n* l*')

    def test_punct(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', '၊ ။'), \
            ', .')

    def test_ll(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ပါဠိ'), \
            'pāḷi')

    def test_example_1(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'ကော်မီတီ ဥပုသ် ပန်းကန် ကော်ပြန့်'), \
            'koʻmītī upusʻ panʻʺkanʻ koʻpranʻʹ')

    def test_example_2(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', 'မောင်မောင်စိုးတင့် စောစိုင်မောင် ချန်ရီစိန် ကဲနက်ဘစိန် မြသီတာ ပဒေသရာဇာ', \
            pre_options=['segmentBurmeseSyllables']), \
            ' moṅʻ moṅʻ cuiʺ taṅʻʹ   co cuiṅʻ moṅʻ   khyanʻ rī cinʻ   kai nakʻ bha cinʻ   mra sī tā   pa de sa rā jā')

    def test_example_3(self):
        self.assertEqual(transliterate.process('Burmese', 'RomanLoC', '''မဟာသမိုင်းတော်ကြီးညွန့်ပေါင်း
ယောအတွင်းဝန်ဦးဖိုးလှိုင်
ဒုဋ္ဌဂါမဏိမင်းကြီးဝတ္ထု'''), \
            '''mahāsamuiṅʻʺtoʻkrīʺññvanʻʹpoṅʻʺ
yo’atvaṅʻʺvanʻūʺphuiʺlhuiṅʻ
duṭṭhagāmaṇimaṅʻʺkrīʺvatthu''')

    def test_a_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', '’a'), 'အ')

    def test_au_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese',  'o oʻ ko koʻ'), 'ဩ ဪ ကော ကော်')

    def test_anusvara_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'kaṃ kāṃ ’aṃ ’uiṃ'), 'ကံ ကာံ အံ အိုံ')
        ## wrong anu
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'kaṁ kāṁ ’aṁ ’uiṁ'), 'ကံ ကာံ အံ အိုံ')


    def test_vowels_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', '’a ’ā ’i ’ī ’u ’ū ’e ’ai ’o ’oʻ ’ui'), \
            'အ အာ အိ အီ အု အူ အေ အဲ အော အော် အို')
        # wrong accent
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'ʼa ʼā ʼi ʼī ʼu ʼū ʼe ʼai ʼo ʼoʻ ʼui'), \
            'အ အာ အိ အီ အု အူ အေ အဲ အော အော် အို')

    def test_subjoined_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese',  'myha krva lvha mrvhaṅʻʺ'), \
            'မျှ ကြွ လွှ မြွှင်း')

    def test_virama_final_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese',  'takkasuilʻ tiracchānʻ'), \
           'တက္ကသိုလ် တိရစ္ဆာန်')

    def test_superscript_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'saṅgha dharma'), \
            'သင်္ဃ ဓရ်္မ')

    def test_ui_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', '’ui tui kui'), \
            'အို တို ကို')
        ## wrong accent
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'ʼui tui kui'), \
            'အို တို ကို')

    def test_tone_1_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'puiʹ puiʺ'), \
            'ပို့ ပိုး')
        ## the wrong accents
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'pui´ pui˝'), \
            'ပို့ ပိုး')

    def test_tone_2_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'paṅʻʹ'), \
          'ပင့်')
        ## wrong accents
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'paṅʻ´'), \
          'ပင့်')

    def test_great_ssa_nna_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'tassa paññā'), \
            'တဿ ပညာ')

    def test_abbr_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'e* r* n* l*'), \
            '၏ ၍ ၌ ၎')

    def test_punct_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', ', .'), \
            '၊ ။')

    def test_ll_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'pāḷi'), \
            'ပါဠိ')

    def test_example_1_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'koʻmītī upusʻ panʻʺkanʻ koʻpranʻʹ'), \
            'ကော်မီတီ ဥပုသ် ပန်းကန် ကော်ပြန့်')

    def test_example_2_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', 'moṅʻ moṅʻ cuiʺ taṅʻʹ co cuiṅʻ moṅʻ khyanʻ rī cinʻ kai nakʻ bha cinʻ mra sī tā pa de sa rā jā', \
            post_options=['removeSegmentSpacesBurmese']), \
            'မောင်မောင်စိုးတင့်စောစိုင်မောင်ချန်ရီစိန်ကဲနက်ဘစိန်မြသီတာပဒေသရာဇာ')

    def test_example_3_rev(self):
        self.assertEqual(transliterate.process('RomanLoC', 'Burmese', '''mahāsamuiṅʻʺtoʻkrīʺññvanʻʹpoṅʻʺ
yo’atvaṅʻʺvanʻūʺphuiʺlhuiṅʻ
duṭṭhagāmaṇimaṅʻʺkrīʺvatthu'''), \
            '''မဟာသမိုင်းတော်ကြီးညွန့်ပေါင်း
ယောအတွင်းဝန်ဦးဖိုးလှိုင်
ဒုဋ္ဌဂါမဏိမင်းကြီးဝတ္ထု''')

if __name__ == '__main__':
    unittest.main()