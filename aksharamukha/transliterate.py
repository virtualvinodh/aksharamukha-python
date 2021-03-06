import re
from . import Convert,PostOptions,PostProcess,PreProcess
from . import ConvertFix
import json
import requests
import html
import itertools
from collections import Counter
import unicodedata
import io
import collections
'''import yaml
import warnings
import langcodes'''

def removeA(a):
    if a.count('a') == 1:
        return a.replace('a', '')

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def auto_detect(text, plugin = False):
    scripts = []

    for uchar in text:
        try:
            scripts.append(unicodedata.name(uchar).split(' ')[0].lower())
        except ValueError:
            pass
            # print('Script not found')

    counts = Counter(scripts)
    script_percent = []

    for script, count  in counts.items():
        percent = count/len(scripts) * 100
        script_percent.append((percent, script))

    #print(sorted(script_percent))

    if not plugin:
        if len(script_percent) > 0:
            script = sorted(script_percent)[-1][1]
        else:
            script = ''
    else:
        #print('here')
        if len(script_percent) > 0:
            if sorted(script_percent)[-1][1] == 'latin':
                script = sorted(script_percent)[-2][1]
            else:
                script = sorted(script_percent)[-1][1]
        else:
            script = ''

    #print('the script is')
    #print(script)
    inputScript = script[0].upper() + script[1:]

    laoPali = ['ຆ', 'ຉ', 'ຌ', 'ຎ', 'ຏ', 'ຐ', 'ຑ', 'ຒ', 'ຓ', 'ຘ', 'ຠ', 'ຨ', 'ຩ', 'ຬ', '຺']

    if inputScript == 'Bengali':
        if 'ৰ' in text or 'ৱ' in text:
            inputScript = 'Assamese'
    elif inputScript == 'Lao':
        if any(char in text for char in laoPali):
            inputScript = 'LaoPali'
    elif inputScript == 'Batak':
        inputScript = 'BatakKaro'
    elif inputScript == 'Myanmar':
        inputScript = 'Burmese'

        mon = ['ၚ', 'ၛ', '္ည', 'ၞ', 'ၟ', 'ၠ', 'ဳ', 'ဨ']
        if any([char in text for char in mon]):
            inputScript = 'Mon'

        countSub = {'Shan': 0, 'TaiLaing': 0, 'KhamtiShan': 0}

        text = text.replace('ႃ', '')

        for uchar in text:
            try:
                char = unicodedata.name(uchar).lower()
            except:
                pass
            if 'shan' in char:
                countSub['Shan'] += 1
            elif 'tai laing' in char:
                countSub['TaiLaing'] += 1
            elif 'khamti' in char:
                countSub['KhamtiShan'] += 1

        import operator
        sorted_x = sorted(countSub.items(), key=operator.itemgetter(1))

        if countSub['Shan'] > 0 or countSub['TaiLaing'] > 0 or countSub['KhamtiShan'] > 0:
            inputScript = sorted_x[-1][0]


        #shan = ['ႃ', '\u1086', '\u1084', 'ၵ', 'ၶ', 'ၷ', 'ꧠ', 'ၸ', 'ꧡ', 'ꩡ', 'ꧢ', 'ၺ', 'ꩦ', 'ꩧ', 'ꩨ', 'ꩩ', 'ꧣ', 'ၻ', 'ꩪ', 'ၼ','ၽ', 'ꧤ', 'ႁ', 'ꩮ', 'ၹ', 'ၾ']
        #if any([char in text for char in shan]):
            #inputScript = 'Shan'

    elif inputScript == 'Meetei':
        inputScript = 'MeeteiMayek'
    elif inputScript == 'Old':
        inputScript = 'OldPersian'
    elif inputScript == 'Phags-pa':
        inputScript = 'PhagsPa'
    elif inputScript == 'Ol':
        inputScript = 'Santali'
    elif inputScript == 'Sora':
        inputScript = 'SoraSompeng'
    elif inputScript == 'Syloti':
        inputScript = 'SylotiNagri'
    elif inputScript == 'Tai':
        inputScript = 'TaiTham'
    elif inputScript == 'Warang':
        inputScript = 'WarangCiti'
    elif inputScript == 'Siddham':
        preOptions = 'siddhamUnicode'
    elif inputScript == 'Cyrillic':
        inputScript = 'RussianCyrillic'
    elif inputScript == 'Zanabazar':
        inputScript = 'ZanabazarSquare'
    elif inputScript == 'Arabic':
        inputScript = 'Urdu'
        shahmukh_char = 'ݨ لؕ مھ نھ یھ رھ لھ وھ'.split(" ")
        if any(char in text for char in shahmukh_char):
            inputScript = 'Shahmukhi'
    elif inputScript == 'Latin':
        diacritics = ['ā', 'ī', 'ū', 'ṃ', 'ḥ', 'ś', 'ṣ', 'ṇ', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'ḻ', 'ṉ', 'ṟ', 'ṭ', 'ḍ', 'ṅ', 'ñ']
        Itrans = ['R^i', 'R^I', 'L^i', 'L^I', '.N', '~N', '~n', 'Ch', 'sh', 'Sh']
        if 'ʰ' in text:
            inputScript = 'Titus'
        elif any(char in text for char in diacritics):
            if 'ē' in text or 'ō' in text or 'r̥' in text:
                inputScript = 'ISO'
            else:
                inputScript = 'IAST'
        elif any(char in text for char in Itrans):
            inputScript = 'Itrans'
        else:
            inputScript = 'HK'

    return inputScript

# Cross check with inded convert() funciton within autodetect
# scripts available here must be added there
def detect_preoptions(text, inputScript):
    preoptions = []
    if inputScript == 'Thai':
        textNew = text.replace('ห์', '')
        if '\u035C' in text or '\u0325' in text or 'งํ' in text or '\u0E47' in text:
            preoptions = ['ThaiPhonetic']
        elif '์' in textNew and ('ะ' in text):
            preoptions = ['ThaiSajjhayawithA']
        elif '์' in textNew:
            preoptions = ['ThaiSajjhayaOrthography']
        elif 'ะ' in text or 'ั' in text:
            preoptions =  ['ThaiOrthography']
    elif inputScript == 'Lao' or inputScript == 'LaoPali':
        textNew = text.replace('ຫ໌', '')
        if '໌' in textNew and ('ະ' in text):
            preoptions = ['LaoSajhayaOrthographywithA']
        elif '໌' in textNew:
            preoptions = ['LaoSajhayaOrthography']
        elif 'ະ' in text or 'ັ' in text:
            preoptions = ['LaoTranscription']
    elif inputScript == 'Urdu':
            preoptions = ['UrduShortNotShown']

    return preoptions

def convert(src, tgt, txt, nativize, preoptions, postoptions):
    tgtOld = ""

    if src == "Itrans" and '##' in txt:
        textNew = [[i,word] for i, word in enumerate(txt.split("##")) if (i%2 == 0)]
        textRest = [(i,word) for i, word in enumerate(txt.split("##")) if (i%2 == 1)]

        txt = json.dumps(textNew).replace("\\n", "\n")

    if tgt == "" or tgt == "Ignore":
        return txt
    if preoptions == [] and postoptions == [] and nativize == False and src == tgt:
        return txt

    if src == tgt and (src != 'Hiragana' and src != 'Katakana'):
        tgtOld = tgt
        tgt = "Devanagari"

    txt = PreProcess.PreProcess(txt,src,tgt)

    if 'siddhammukta' in postoptions and tgt == 'Siddham':
        tgt = 'SiddhamDevanagari'
    if 'siddhamap' in postoptions and tgt == 'Siddham':
        tgt = 'SiddhamDevanagari'
    if 'siddhammukta' in preoptions and src == 'Siddham':
        src = 'SiddhamDevanagari'
    if 'LaoNative' in postoptions and tgt == 'Lao':
        tgt = 'Lao2'
    if 'egrantamil' in preoptions and src == 'Grantha':
        src = 'GranthaGrantamil'
    if 'egrantamil' in postoptions and tgt == 'Grantha':
        tgt = 'GranthaGrantamil'
    if 'nepaldevafont' in postoptions and tgt == 'Newa':
        tgt = 'Devanagari'
    if 'ranjanalantsa' in postoptions and tgt == 'Ranjana':
        tgt = 'Tibetan'
        nativize = False
    if 'ranjanawartu' in postoptions and tgt == 'Ranjana':
        tgt = 'Tibetan'
        nativize = False
    if 'SoyomboFinals' in postoptions and tgt == 'Soyombo':
        txt = '\u02BE' + txt

    for options in preoptions:
      txt = getattr(PreProcess, options)(txt)

    srcOld = ""

    if src == 'Hiragana' or src == 'Katakana':
        txt = PreProcess.JapanesePreProcess(src, txt, preoptions)
        srcOld = 'Japanese'
        src = 'ISO'

    if tgt == 'Hiragana' or tgt == 'Katakana':
        txt = PostProcess.JapanesePostProcess(src, tgt, txt, nativize, postoptions)

    if src == "Oriya" and tgt == "IPA":
        txt = ConvertFix.OriyaIPAFixPre(txt)

    if src == "Itrans" and '##' in txt:
        #print('I am here tyring to do things')
        transliteration = ''
        for i, word in enumerate(txt.split("##")):
            if (i%2 == 0):
                transliteration += Convert.convertScript(word, src, tgt)
            else:
                transliteration += word
    else:
        transliteration = Convert.convertScript(txt, src, tgt)

    if srcOld == 'Japanese' and tgt != 'Devanagari' and 'siddhammukta' not in postoptions:
        transliteration = Convert.convertScript(transliteration, "Devanagari", "ISO")

    if src == tgtOld:
        tgt = tgtOld
        transliteration = Convert.convertScript(transliteration, "Devanagari", tgt)

    if nativize:
      transliteration =  PostOptions.ApplyScriptDefaults(transliteration, src, tgt)
      if tgt != 'Tamil':
        transliteration = PostProcess.RemoveDiacritics(transliteration)
      else:
        transliteration = PostProcess.RemoveDiacriticsTamil(transliteration)

    if 'RemoveDiacritics' in postoptions:
      if tgt == 'Tamil':
        postoptions = map(lambda x: 'RemoveDiacriticsTamil' if x == 'RemoveDiacritics' else x, postoptions)

    for options in postoptions:
      transliteration = getattr(PostProcess, options)(transliteration)

    if src == "Tamil" and tgt == "IPA":
        r = requests.get("http://anunaadam.appspot.com/api?text=" + txt + "&method=2")
        r.encoding = r.apparent_encoding
        transliteration = r.text

    if src == "Oriya" and tgt == "IPA":
        transliteration = ConvertFix.OriyaIPAFix(transliteration)

    if src == "Itrans" and '##' in txt:
        textConv = {**dict(list(json.loads(transliteration.replace("\n", "\\n")))), ** dict(textRest)}
        textConv = collections.OrderedDict(sorted(textConv.items()))
        transliteration = "".join(textConv.values())

    return transliteration

def process(src, tgt, txt, nativize = True, post_options = [], pre_options = []):
    '''with open("aksharamukha/aksharamukha-scripts.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)'''

    if src == 'autodetect':
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)

    # font hack warning
    '''font_hack_warning = tgt + ' users hacked fonts to display the script. In the absence of this font, you text may appear different. \n See: https://aksharamukha.appspot.com/describe/' + tgt + ' for the font used'
    if tgt in data_loaded and 'font_hack' in data_loaded[tgt]:
        warnings.warn(font_hack_warning)'''

    return convert(src, tgt, txt, nativize, pre_options, post_options)

'''
def process_script_tag(src_tag, tgt_tag, txt, nativize = True, post_options = [], pre_options = []):
    # Read YAML file
    import os
    cwd = os.getcwd()
    with open("aksharamukha/aksharamukha-scripts.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    for name in data_loaded.keys():
        if data_loaded[name]['script'].lower() == src_tag.lower():
            src = name
        if data_loaded[name]['script'].lower() == tgt_tag.lower():
            tgt = name

    return convert(src, tgt, txt, nativize, pre_options, post_options)

def process_lang_tag(src_tag, tgt_tag, txt, nativize = True, post_options = [], pre_options = []):
    # Read YAML file
    import os
    cwd = os.getcwd()
    with open("aksharamukha/wikitra2-data.yaml", 'r', encoding='utf8') as stream:
        data_loaded = yaml.safe_load(stream)

    src = []
    tgt = []
    for scrpt in data_loaded.keys():
        for lang in data_loaded[scrpt]:
            if lang == src_tag:
                src.append((len(data_loaded[scrpt]), scrpt))
            if lang == tgt_tag:
                tgt.append((len(data_loaded[scrpt]), scrpt))

    src_pop = sorted(src, reverse=True)[0][1]
    tgt_pop = sorted(tgt, reverse=True)[0][1]
    if len(src) > 1:
        warn = "Multiple scripts associated with the input language. The most popular one '" + src_pop + "' has been selected"
        warnings.warn(warn)
    if len(tgt) > 1:
        warn = "Multiple scripts associated with the target language. The most popular one '" + tgt_pop + "' has been selected"
        warnings.warn(warn)

    return process_script_tag(src_pop, tgt_pop, txt, nativize = True, post_options = [], pre_options = [])

def process_lang_name(src_name, tgt_name, txt, nativize = True, post_options = [], pre_options = []):
    src = langcodes.find(src_name)
    tgt = langcodes.find(tgt_name)

    return process_lang_tag(str(src), str(tgt), txt, nativize = True, post_options = [], pre_options = [])
'''
## add the new libraries to requiesments.txt in both folders