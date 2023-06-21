import pytest
from aksharamukha import transliterate, GeneralMap

target_scripts = GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts
source_texts = ['heart', 'lalitavistara']

def text_compare(source_script, target_script, source_text):
    with open('test_texts/test_' + source_script + '_' + target_script +  '_' + source_text + '.txt', 'r', encoding= 'utf8') as fo:
        with open('test_texts/source_' + source_script + '_' + source_text + '.txt', 'r', encoding= 'utf8') as fi:
            assert transliterate.process(source_script, target_script, fi.read()) == fo.read()

class TestOverall:
    @pytest.mark.parametrize("source_script", ['Devanagari', 'IAST'])
    @pytest.mark.parametrize("target_script", target_scripts)
    @pytest.mark.parametrize("source_text", source_texts)
    def test_overall(self, source_script, target_script, source_text):
        text_compare(source_script, target_script, source_text)