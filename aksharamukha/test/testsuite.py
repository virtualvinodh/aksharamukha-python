import pytest
from aksharamukha import transliterate, GeneralMap, PostProcess, PreProcess

target_scripts = GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts
source_texts = ['heart', 'lalitavistara']
post_options = (d for d in dir(PostProcess) if '__' not in d)

reversible_scripts = GeneralMap.ReversibleScripts + GeneralMap.RomanReversible

# Workbench-generated conversion samples (regression/workbench/conversion_samples.json,
# the Source Texts tab's 'all-fanout' button - source -> every script, both
# nativize=True and nativize=False). Round-trip candidates are derived
# straight from this, not from a separately-generated "reverse" record: any
# nativize=False fanout row whose target is a reversible script IS a
# round-trip check, by definition of what "reversible" means - generating a
# second, dedicated record for the same (source, target, nativize) pair was
# pure duplication (verified: 100% overlap before this was removed). Read
# fresh here so pytest is the actual authority on whether a round trip still
# holds, not a boolean cached at generation time that never gets re-checked.
#
# BOTH source and target must be reversible, not just target: the workbench
# also generates a reverse pair for IRREVERSIBLE targets (e.g. Urdu ->
# Devanagari, using Urdu output as input) purely for one-directional sanity
# coverage, explicitly not a round-trip claim. Since Devanagari (the target
# there) is reversible, filtering on target alone wrongly swept those in as
# round-trip candidates - real regression, caught by a sudden jump from the
# usual 9 known failures to 30.
def _load_roundtrip_samples():
    import json
    import os
    path = os.path.join('regression', 'workbench', 'conversion_samples.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf8') as f:
        samples = json.load(f)
    reversible = set(reversible_scripts)
    return [r for r in samples
            if r.get('mode') == 'fanout' and r.get('nativize') is False
            and r.get('target') in reversible and r.get('source') in reversible]

roundtrip_samples = _load_roundtrip_samples()
roundtrip_sample_ids = ['%s-%s-%s' % (r.get('label'), r.get('source'), r.get('target')) for r in roundtrip_samples]

# Free-form cases (regression/workbench's Custom Cases tab): unlike
# Post-options/Pre-options, which test one option at a time, these are a full
# transliterate.process call - source, target, nativize, and any combination
# of pre_options/post_options together.
def _load_custom_cases():
    import json
    import os
    path = os.path.join('test_texts', 'test_custom_cases.json')
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

custom_cases = _load_custom_cases()
custom_case_ids = ['%s-%s-%s' % (c.get('label') or i, c.get('source'), c.get('target')) for i, c in enumerate(custom_cases)]

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

class TestConversionSampleRoundtrips:
    @pytest.mark.parametrize("sample", roundtrip_samples, ids=roundtrip_sample_ids)
    def test_roundtrip(self, sample):
        # Bengali's va/ba merger makes it genuinely, expectedly lossy - the
        # existing TestOverallReversible/TestOverallReversible2 skip it for
        # the same reason, not a bug to chase here.
        if sample['source'] == 'Bengali' or sample['target'] == 'Bengali':
            return
        nativize = sample.get('nativize', False)
        forward = transliterate.process(sample['source'], sample['target'], sample['input'], nativize=nativize)
        backward = transliterate.process(sample['target'], sample['source'], forward, nativize=nativize)
        assert backward == sample['input']

class TestCustomCases:
    @pytest.mark.parametrize("case", custom_cases, ids=custom_case_ids)
    def test_custom_case(self, case):
        assert transliterate.process(
            case['source'], case['target'], case['input'],
            nativize=case.get('nativize', True),
            pre_options=case.get('pre_options', []),
            post_options=case.get('post_options', []),
        ) == case['output']

class TestPostOptions:
    @pytest.mark.parametrize("post_options", post_options)
    def test_postoptions(self, post_options):
        import json

        with open('test_texts/test_postoptions.json', 'r', encoding= 'utf8') as f:
            texts = json.load(f)
        try:
            testcases = texts[post_options]

            for testcase in testcases:
                nativize = testcase.get("nativize", True)
                for case in testcase["cases"]:
                    assert transliterate.process(testcase["source"], testcase["target"], case[0], nativize=nativize, post_options=[post_options]) == case[1]
        except KeyError:
            assert 1 == 1

pre_options = (d for d in dir(PreProcess) if '__' not in d)

class TestPreOptions:
    @pytest.mark.parametrize("pre_options", pre_options)
    def test_preoptions(self, pre_options):
        import json

        with open('test_texts/test_preoptions.json', 'r', encoding= 'utf8') as f:
            texts = json.load(f)
        try:
            testcases = texts[pre_options]

            for testcase in testcases:
                nativize = testcase.get("nativize", True)
                for case in testcase["cases"]:
                    assert transliterate.process(testcase["source"], testcase["target"], case[0], nativize=nativize, pre_options=[pre_options]) == case[1]
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