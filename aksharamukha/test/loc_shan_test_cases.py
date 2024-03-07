from aksharamukha import transliterate

import unittest

test_strings_rev = [
    ('ဢ', '’a'),
    ('ၵႃ ၵိ​ ၵီ​ ၵု ၵူ ၵို ၵိူ ၵေ ၵွ ၵႄ​ ၵွႆ ၵႂ် ၵၢႆ ၵေႃ ၵေႃ် ၵျ ၵြ ၵႂ ၵိူဝ် ၵူဝ် ၵဝ်', \
     'kā ki​ kī​ ku kū kui kūi ke kau kè​ koi kái kāi ko kò kya kra kva kūivʻ kō kavʻ'),
    ('ဢႃ ဢိ​ ဢီ​ ဢု ဢူ ဢို ဢိူ ဢေ ဢွ ဢႄ​ ဢွႆ ဢႂ် ဢၢႆ ဢေႃ ဢေႃ် ဢိူဝ် ဢူဝ် ဢဝ်', \
     '’ā ’i​ ’ī​ ’u ’ū ’ui ’ūi ’e ’au ’è​ ’oi ’ái ’āi ’o ’ò ’ūivʻ ’ō ’avʻ'),
    ('တြႃးတေႃ်ၸဝ်သုၵ်သီလၶၼ်း​','trāʺtòcavʻsukʻsīlakhanʻʺ​'),
    ('မွင်းဝၼ်းၶိုၼ်းႁၼ်', 'mauṅʻʺvanʻʺkhuinʻʺhanʻ'),
    ('ဢမ်ႇၶႂ်ႈၼွၼ်းၽၼ်', '’am̢ʻkhái̐naunʻʺphanʻ'),
    ('ၸိူင်းပွတ်းၽွမ်ႉႁူမ်ႈ', 'cūiṅʻʺpautʻʺphaumʻʹhūm̐ʻ'),
    ('မၢႆၼိုင်ႈ', 'māinuiṅ̐ʻ'),
    ('ၼင်းၸံးပူးဝွၵ်း', 'naṅʻʺcaṃʺpūʺvaukʻʺ'),
    ('ပရိတ်တပႃႇလိလႄႈၶေႃႈပွင်ႇၽၢႆႉတႆး', 'paritʻtapā̢lilè̐kho̐pauṅ̢ʻphāiʹtaiʺ'),
    ('ၼံႉၵႂံးၸဝ်သင်လုင်ဝၼ်ဢႆ', 'naṃʹkvaṃʺcavʻsaṅʻluṅʻvanʻ’ai'),
    ('၊ ။', ', .')
]

test_strings_rev_openclosed = [
    ('ၵေးၵဵၸ်ၷႄႉၶႅၺ်ႊပႃႊပၢထ်း','keʺkecʻgèʹkhèñʻ˝pā˝pāthʻʺ'),
    ('မဵတ်ႉတႃႇၸႅတ်ႈ', 'metʻʹtā̢cèt̐ʻ'),
    ('လေႃးၵီႇၵတ်းယဵၼ်', 'loʺkī̢katʻʺyenʻ'),
    ('ယိင်းမူၺ်သႅင်လိူၼ်', 'yiṅʻʺmūñʻsèṅʻlūinʻ'),
    ('ပိုၼ်းၽြႃးတႃႇလုၵ်ႈႁဵၼ်းပၢၼ်မႂ်ႇ', 'puinʻʺphrāʺtā̢luk̐ʻhenʻʺpānʻmái̢'),
    ('ၸၢတ်ႈၸဝ်ႈသုဝၼ်ႇၼသၢမ်ႇ', 'cāt̐ʻcav̐ʻsuvan̢ʻnasām̢ʻ'),
    ('လႅင်းမုၼ်းမႂ်ႇ', 'lèṅʻʺmunʻʺmái̢'),
    ('ၵေႇၵဵၵ်းၻႄႉၻႅသ်ႊတႃႈႀၢရ်း', 'ke̢kekʻʺdèʹdèsʻ˝tā̐xārʻʺ')
]

test_strings_irrev = [
    ('ပပ်ႉၽိုၵ်းလႃတ်ႈၵႂႃမ်းႁႃႈၽႃႇသႃႇ', 'papʻʹphuikʻʺlāt̐ʻkvāmʻʺhā̐phā̢sā̢'),
    ('တႃႇႁဵတ်းၵႃၼ်ၶိုၼ်ႈယႂ်ႇ', 'tā̢hetʻʺkānʻkhuin̐ʻyái̢'),
    ('ၶႅပ်းမႃင်ၸဝ်ႈꩪမ်ႇမၻႃႉၼ', 'khèpʻʺmāṅʻcav̐ʻdham̢ʻmadāʹna'),
    ('ၿႆၢ ၵၢ ၵႃႆ ၵေေ ၵေါ','bāi kā kāi kè ko')
]

class TestStringMethods(unittest.TestCase):
    def test_shan_roman_loc(self):
        for shan, loc in test_strings_rev + test_strings_rev_openclosed:
            self.assertEqual(transliterate.process('Shan', 'RomanLoC', shan), loc)

    def test_roman_loc_shan(self):
        for shan, loc in test_strings_rev + test_strings_rev_openclosed:
            self.assertEqual(transliterate.process('RomanLoC', 'Shan', loc), shan)

    def test_shan_roman_loc_irrev(self):
        for shan, loc in test_strings_irrev:
            self.assertEqual(transliterate.process('Shan', 'RomanLoC', shan), loc)

if __name__ == '__main__':
    unittest.main()