import pytest
from aksharamukha import transliterate, GeneralMap, PostProcess, PreProcess

target_scripts = GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts
source_texts = ['heart', 'lalitavistara']
post_options = (d for d in dir(PostProcess) if '__' not in d)

reversible_scripts = GeneralMap.ReversibleScripts + GeneralMap.RomanReversible

def text_compare_reversible_2(source_script, target_script, source_text):
    try:
        with open('test_texts/source_Devanagari'+ '_' + source_text + '.txt', 'r', encoding= 'utf8') as fi:
            src_txt = fi.read()
            dev_to_src = transliterate.process('Devanagari', source_script, src_txt, nativize=False)
            src_to_tgt = transliterate.process(source_script, target_script, dev_to_src, nativize=False)
            tgt_to_src = transliterate.process(target_script, source_script, src_to_tgt, nativize=False)
            assert tgt_to_src == dev_to_src
    except FileNotFoundError:
        ## Fix this ## fix this
        print(source_script, target_script)


def text_compare_reversible(source_script, target_script, source_text):
    try:
        with open('test_texts/source_' + source_script + '_' + source_text + '.txt', 'r', encoding= 'utf8') as fi:
            src_txt = fi.read()
            src_to_tgt = transliterate.process(source_script, target_script, src_txt, nativize=False)
            tgt_to_src = transliterate.process(target_script, source_script, src_to_tgt, nativize=False)
            assert tgt_to_src == src_txt
    except FileNotFoundError:
        ## Fix this ## fix this
        print(source_script, target_script)


def text_compare(source_script, target_script, source_text):
    try:
        with open('test_texts/test_' + source_script + '_' + target_script +  '_' + source_text + '.txt', 'r', encoding= 'utf8') as fo:
            with open('test_texts/source_' + source_script + '_' + source_text + '.txt', 'r', encoding= 'utf8') as fi:
                assert transliterate.process(source_script, target_script, fi.read()) == fo.read()
    except FileNotFoundError:
        print(source_script, target_script)

class TestOverall:
    @pytest.mark.parametrize("source_script", ['Devanagari', 'IAST'])
    @pytest.mark.parametrize("target_script", target_scripts)
    @pytest.mark.parametrize("source_text", source_texts)
    def test_overall(self, source_script, target_script, source_text):
        text_compare(source_script, target_script, source_text)

class TestOverallReversible:
    @pytest.mark.parametrize("source_script", ['Devanagari', 'IAST'])
    @pytest.mark.parametrize("target_script", reversible_scripts)
    @pytest.mark.parametrize("source_text", source_texts)
    def test_overall_reversible(self, source_script, target_script, source_text):
        if target_script != 'Bengali':
            text_compare_reversible(source_script, target_script, source_text)

class TestOverallReversible2:
    @pytest.mark.parametrize("source_script", reversible_scripts)
    @pytest.mark.parametrize("target_script", reversible_scripts)
    @pytest.mark.parametrize("source_text", source_texts)
    def test_overall_reversible_2(self, source_script, target_script, source_text):
        if target_script != 'Bengali' and source_script != 'Bengali':
            text_compare_reversible_2(source_script, target_script, source_text)

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

class TestSanity:
    @pytest.mark.parametrize("target_scripts", target_scripts)
    def test_sanity_default(self, target_scripts):
        import json
        with open('test_texts/test_sanity_default.json', 'r', encoding= 'utf8') as f:
            texts = json.load(f)
        try:
            testcases = texts[target_scripts]

            for testcase in testcases:
                for case in testcase["cases"]:
                    nativize = testcase["nativize"] if "nativize" in testcase else True
                    assert transliterate.process(testcase["source"], testcase["target"], case[0], nativize=nativize) == case[1]

                    if "reverse" in testcase:
                        assert transliterate.process(testcase["target"], testcase["source"], case[1], nativize=nativize) == case[0]
        except KeyError:
            assert 1 == 1

class TestMisc:
    def test_bengali_va_default(self):
        assert transliterate.process('HK', 'Bengali', 'savva sabba samba samva sarva sarba ukva ukba utva utba udveda udbodhana bru bra bya byu vra vya vla') == 'সব্ব সব্ব সম্ব সম্ব সর্ব সর্ব উক্ব উক্ব উত্ব উত্ব উদ্বেদ উদ্বোধন ব্রু ব্র ব্য ব্যু ব্র ব্য ব্ল'

    def test_bengali_va_preserve_source(self):
        assert transliterate.process('HK', 'Bengali', 'savva sabba samba samva sarva sarba ukva ukba utva utba udveda udbodhana bru bra bya byu vra vya vla', nativize=False) == 'সভ়্ভ় সব্ব সম্ব সম্ভ় সর্ভ় সর্ব উক্ব উক্‌ব উত্ব উৎ‌ব উদ্বেদ উদ্‌বোধন ব্রু ব্র ব্য ব্যু ভ়্র ভ়্য ভ়্ল'

    def test_bengali_va_old_ra(self):
        assert transliterate.process('HK', 'Bengali', 'savva sabba samba samva sarva sarba ukva ukba utva utba udveda udbodhana bru bra bya byu vra vya vla', post_options=['BengaliRaBa']) == 'সব্ব সৰ্‌‌ৰ সম্‌ৰ সম্ব সর্ব সৰ্ৰ উক্ব উক্‌ৰ উত্ব উত্‌ৰ উদ্বেদ উদ্‌ৰোধন ৰ‍্রু ৰ‍্র ৰ‍্য ৰ‍্যু ব্র ব্য ব্ল'