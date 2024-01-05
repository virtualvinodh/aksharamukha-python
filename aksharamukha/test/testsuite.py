import pytest
from aksharamukha import transliterate, GeneralMap, PostProcess, PreProcess

target_scripts = GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts
source_texts = ['heart', 'lalitavistara']
post_options = (d for d in dir(PostProcess) if '__' not in d)

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

class TestPostOptions:
    @pytest.mark.parametrize("post_options", post_options)
    def test_postoptions(self, post_options):
        import json

        with open('test_texts/test_postoptions.json', 'r', encoding= 'utf8') as f:
            texts = json.load(f)
        try:
            testcases = texts[post_options]

            for testcase in testcases:
                for case in testcase["cases"]:
                    assert transliterate.process(testcase["source"], testcase["target"], case[0], post_options=[post_options]) == case[1]
        except KeyError:
            assert 1 == 1
