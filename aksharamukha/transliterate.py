from aksharamukha import GeneralMap
from aksharamukha.gimeltra import Transliterator
from . import Convert,PostOptions,PostProcess,PreProcess
from . import ConvertFix
from . import ScriptRegistry as SR
from . import Options
from . import Context
import json
import requests
import html
import itertools
from collections import Counter
import unicodedata
import collections
import yaml
import warnings
import langcodes
import os

#import sys
#sys.stdout = None

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
            script_name = unicodedata.name(uchar).split(' ')[0].lower()
            if script_name != 'old':
                scripts.append(script_name)
            else:
                scripts.append(unicodedata.name(uchar).split(' ')[1].lower())
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
    elif inputScript == 'Dives':
        inputScript = 'DivesAkuru'
    elif inputScript == 'Persian':
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
    elif inputScript == 'Syriac':
        inputScript = 'Syre'
        eastern_dia = 'ܲ ܵ ܝܼ ܘܼ ܸ ܹ ܘܿ'.split(' ')
        if any(char in text for char in eastern_dia):
            inputScript = 'Syrn'
        western_dia = 'ܰ ܺ ܶ ّ ܽ'.split(' ')
        if any(char in text for char in western_dia):
            inputScript = 'Syrj'
    elif inputScript == 'Arabic':
        inputScript = 'Arab'
        persian_char = 'چ گ ژ پ هٔ'.split(' ')
        if any(char in text for char in persian_char):
            inputScript = 'Arab-Fa'
        urdu_char = 'ڈ ٹ ڑ ھ'.split(' ')
        if any(char in text for char in urdu_char):
            inputScript = 'Urdu'
        shahmukh_char = 'ݨ لؕ مھ نھ یھ رھ لھ وھ'.split(" ")
        if any(char in text for char in shahmukh_char):
            inputScript = 'Shahmukhi'
    elif inputScript == 'Latin':
        diacritics = ['ā', 'ī', 'ū', 'ṃ', 'ḥ', 'ś', 'ṣ', 'ṇ', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'ḻ', 'ṉ', 'ṟ', 'ṭ', 'ḍ', 'ṅ', 'ñ']
        Itrans = ['R^i', 'R^I', 'L^i', 'L^I', '.N', '~N', '~n', 'Ch', 'sh', 'Sh']
        semitic = ['ʾ', 'ʿ', 'š', 'w']
        BurmeseRomanLoC = ['´', '˝', 'ʻ']
        if 'ʰ' in text:
            inputScript = 'Titus'
        elif any(char in text for char in semitic):
            inputScript = 'Latn'
        elif any(char in text for char in BurmeseRomanLoC):
            inputScript = 'BurmeseRomanLoC' ## Change for other LoC schemese
        elif any(char in text for char in diacritics):
            if 'ē' in text or 'ō' in text or 'r̥' in text:
                inputScript = 'ISO'
            else:
                inputScript = 'IAST'
        elif any(char in text for char in Itrans):
            inputScript = 'Itrans'
        else:
            inputScript = 'HK'
    elif SR.get(inputScript).is_indic or SR.get(inputScript).is_latin or inputScript in ['Hiragana', 'Katakana']:
        pass
    else:
        from . import gimeltra
        tr = gimeltra.Transliterator()
        inputScript = tr.auto_script(text)

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

# --- convert() pipeline stages -----------------------------------------
# Extracted verbatim from convert() below, one labeled block at a time -
# no logic changes, same variables in and out. See the refactor plan:
# convert() is 330 lines of ~14 sequentially-interleaved concerns sharing
# the same handful of mutable variables (src, tgt, preoptions,
# postoptions, nativize); breaking it into named stages is being done
# incrementally, lowest-risk stages first, each independently verified.

def _apply_indic_dandas_preoption(src, tgt, txt, preoptions, postoptions):
    ## this has to be before preprocess.preprocess
    if 'indicDandas' in postoptions:
        if SR.get(src).is_pipe_script and '|' in txt:
            txt = PreProcess.RetainPipeDanda(txt, src)
        elif GeneralMap.CrunchList('SignMap', src)[1] == '।':
            preoptions = preoptions + ['RetainDevangariDanda']
        else:
            if not SR.get(tgt).is_transliteration:
                postoptions = postoptions + ['Dot2Dandas']
            else:
                postoptions = postoptions + ['Dot2Pipes']

    return txt, preoptions, postoptions

# Unified LoC (Library of Congress romanization) dispatch. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention and how
# to add a new script. Every LoC-enabled script gets up to 4 functions,
# auto-discovered purely by name - no registry/dict to maintain:
#   <Script>ToRomanLocPre / <Script>ToRomanLocPost   (native -> LoC Roman)
#   RomanLocTo<Script>Pre / RomanLocTo<Script>Post   (LoC Roman -> native)
# None are mandatory - most scripts only need one or two. For scripts
# that share a pivot (KhuenTham/TaiTham/LaoTham/LueTham all route
# through 'ThamLoC'), the lookup tries the script's own name first, then
# falls back to the shared pivot name - so KhuenTham can override with
# its own function (see ScriptProcessing/KhuenTham.py) while the others
# automatically share the pivot-level implementation with zero extra code.

def _loc_option_names(script, to_roman, direction):
    """Candidate function names for a script's LoC pre/post option, own
    name first then pivot name as fallback. to_roman=True for the
    native->Roman direction, False for Roman->native. direction is
    'Pre' or 'Post'."""
    names = [script]
    pivot = SR.get(script).loc_pivot_name
    if pivot and pivot != script:
        names.append(pivot)
    for name in names:
        yield (name + 'ToRomanLoc' + direction) if to_roman else ('RomanLocTo' + name + direction)

def _apply_loc_option(module, script, to_roman, direction, options_list, prepend):
    for fname in _loc_option_names(script, to_roman, direction):
        if hasattr(module, fname):
            if prepend:
                options_list.insert(0, fname)
            else:
                options_list.append(fname)
            return

# The two "not LoC-associated" cases (src-side and tgt-side) really are
# clean mirrors of each other - unified here.
def _resolve_loc_fallback_target(script):
    if SR.get(script).is_semitic:
        return 'ISO233'
    else:
        return 'ISO'

# nativize=False is preserved specifically for the 4 scripts that used
# to route through the old "east-Asian LoC" special case (Burmese, Shan,
# Khmer, and the Tham-family, via their pivot names) - not fully
# understood well enough downstream to risk generalizing to every LoC
# script in this pass, so kept as an explicit, narrow carry-over rather
# than silently changed.
_LOC_NATIVIZE_FALSE_PIVOTS = {'Burmese', 'ShanLoC', 'KhmerLoC', 'ThamLoC'}

def _resolve_loc_when_source_is_loc_script(src, tgt, txt, preoptions, postoptions, nativize):
    pivot = SR.get(src).loc_pivot_name
    if SR.get(pivot).loc_tgt_map:
        tgt = pivot + tgt
    elif SR.get(pivot).loc_tgt_iso:
        tgt = 'ISO'

    # order matters: pre-options APPEND (run after any user-supplied
    # preoptions), post-options PREPEND (run before any user-supplied
    # postoptions) - applied uniformly for every LoC script now.
    _apply_loc_option(PreProcess, src, True, 'Pre', preoptions, prepend=False)
    _apply_loc_option(PostProcess, src, True, 'Post', postoptions, prepend=True)
    if pivot in _LOC_NATIVIZE_FALSE_PIVOTS:
        nativize = False

    src = pivot
    return src, tgt, txt, preoptions, postoptions, nativize

def _resolve_loc_when_target_is_loc_script(src, tgt, txt, preoptions, postoptions, nativize, ctx):
    pivot = SR.get(tgt).loc_pivot_name
    if SR.get(pivot).loc_tgt_map:
        src = pivot + src
    elif SR.get(pivot).loc_tgt_iso:
        src = 'ISO'

    _apply_loc_option(PreProcess, tgt, False, 'Pre', preoptions, prepend=False)
    _apply_loc_option(PostProcess, tgt, False, 'Post', postoptions, prepend=True)
    if pivot in _LOC_NATIVIZE_FALSE_PIVOTS:
        nativize = False

    tgt = pivot
    return src, tgt, txt, preoptions, postoptions, nativize

def _resolve_loc_dispatch(src, tgt, txt, preoptions, postoptions, nativize, ctx):
    ## ALA-LC Romanizations
    ## process as follows, if source is associated with LoC script
    if tgt == 'RomanLoC' and SR.get(src).is_loc_script:
        src, tgt, txt, preoptions, postoptions, nativize = _resolve_loc_when_source_is_loc_script(src, tgt, txt, preoptions, postoptions, nativize)

    ## if source is not associated with LoC script
    if tgt == 'RomanLoC' and not SR.get(src).is_loc_script:
        tgt = _resolve_loc_fallback_target(src)

    ## Switches for Target scripts
    ## if target is associated with the loc Script
    if src == 'RomanLoC' and SR.get(tgt).is_loc_script:
        src, tgt, txt, preoptions, postoptions, nativize = _resolve_loc_when_target_is_loc_script(src, tgt, txt, preoptions, postoptions, nativize, ctx)

    ## if target is not associated with the loc Script
    if src == 'RomanLoC' and not SR.get(tgt).is_loc_script:
        src = _resolve_loc_fallback_target(tgt)

    return src, tgt, txt, preoptions, postoptions, nativize

def _resolve_semitic_iso_pivot(src, tgt, txt, preoptions, postoptions, nativize):
    ## Semitic ISO Standards
    ### same as below use intermediates to convert non-associated input/output
    if tgt in GeneralMap.semiticISO.keys():
        if GeneralMap.semiticISO[tgt] != src:
            txt = convert(src, GeneralMap.semiticISO[tgt], txt, nativize, preoptions, postoptions)
            src = GeneralMap.semiticISO[tgt]

        if GeneralMap.semiticISO[tgt] == src:
            preoptions = [tgt + 'Target'] + preoptions
            postoptions =  [tgt + 'Target'] + postoptions
            nativize = False
            tgt = 'Latn'

    if src in GeneralMap.semiticISO.keys():
        if GeneralMap.semiticISO[src] == tgt:
            #print('here1')
            preoptions = [src + 'Source'] + preoptions
            postoptions = [src + 'Source'] + postoptions
            src = 'Latn'
        else:
            #print('here2')
            txt = convert(src, GeneralMap.semiticISO[src], txt, nativize, preoptions, postoptions)
            src = GeneralMap.semiticISO[src]

    return src, tgt, txt, preoptions, postoptions, nativize

def _verify_semitic_iso_consistency():
    # Unlike LoC's per-script options (mostly optional, hasattr()-checked
    # at dispatch time), every GeneralMap.semiticISO entry unconditionally
    # needs all four Target/Source functions - _resolve_semitic_iso_pivot
    # above always appends both, with no existence guard. Fail at import
    # time instead of deep inside Options.call_pre_option/call_post_option
    # the first time a real conversion hits a missing one (as PersianDMG
    # did - see KNOWN_BUGS.md).
    for name in GeneralMap.semiticISO:
        for suffix in ('Target', 'Source'):
            fname = name + suffix
            assert hasattr(PreProcess, fname), 'PreProcess.' + fname + ' is missing'
            assert hasattr(PostProcess, fname), 'PostProcess.' + fname + ' is missing'

_verify_semitic_iso_consistency()

def _resolve_semitic_indic_naming(src, tgt, txt, preoptions, postoptions, nativize):
    ## Semitic Switches - Add Shahmukhi/Sindhi later
    IndicSemiticMapping = { 'Hebrew': 'Hebr', 'Thaana': 'Thaa', 'Urdu': 'Arab-Ur', 'Shahmukhi': 'Arab-Pa'}

    if (SR.get(tgt).is_semitic or tgt in GeneralMap.semiticISO.keys()) and src in IndicSemiticMapping.keys():
        src = IndicSemiticMapping[src]
    if (SR.get(src).is_semitic or src in GeneralMap.semiticISO.keys()) and tgt in IndicSemiticMapping.keys():
        tgt = IndicSemiticMapping[tgt]
    if src in IndicSemiticMapping.keys() and tgt in IndicSemiticMapping.keys():
        src = IndicSemiticMapping[src]
        tgt = IndicSemiticMapping[tgt]

    # preserve semitic pattern
    if not nativize and src == 'Hebrew':
        src = 'Hebr'
    if not nativize and src == 'Urdu':
        src = 'Arab-Ur'
    if not nativize and src == 'Shahmukhi':
        src = 'Arab-Pa'
    if not nativize and src == 'Thaana':
        src = 'Thaa'

    if src in ['Arab-Ur', 'Arab-Pa'] and SR.get(tgt).is_indic:
        txt += '׍'

    ## Semitic to Urdu this is not needed
    #if src in GeneralMap.SemiticScripts and src not in ['Arab-Fa', 'Arab', 'Latn'] and (tgt in ['Urdu', 'Shahmukhi']):
    #    tgt = 'Arab-Fa'

    ## recheck this the logic is missing :: This is not required
    """if src in ['Urdu', 'Shahmukhi'] and tgt == 'Arab':
        #print('Semiticizing Urdu')
        txt = PreProcess.semiticizeUrdu(txt)
        txt = PreProcess.ArabizePersian(txt)
        src = "Arab-Fa"
        tgt = "Arab"

    if src in ['Urdu', 'Shahmukhi'] and tgt == 'Arab-Fa':
        txt = PreProcess.semiticizeUrdu(txt)
        src = "none"
        tgt = "none"

    if src == 'Arab-Fa' and tgt == 'Arab':
        txt = PreProcess.ArabizePersian(txt)
        #src = "none"
        #tgt = "none"

    if src  == 'Arab' and tgt == 'Arab-Fa':
        txt = PreProcess.perisanizeArab(txt)
        src = "none"
        tgt = "none"

    if src  == 'Arab' and tgt in ['Urdu', 'Shahmukhi']:
        txt = PreProcess.perisanizeArab(txt)
        src = "none"
        tgt = "Arab-Fa"

    if src in 'Arab-Fa' and tgt in ['Urdu', 'Shahmukhi']:
        src = "none"
        tgt = "none" """

    ## Semitic Naivization : remove pesky Nuktas
    if nativize:
        if SR.get(src).is_semitic and SR.get(tgt).is_indic:
            txt += "׌"

    tgtOld = ""
    if src == tgt and (src != 'Hiragana' and src != 'Katakana') and not SR.get(src).is_semitic:
        tgtOld = tgt
        tgt = "Devanagari"

    return src, tgt, txt, preoptions, postoptions, nativize, tgtOld

def _apply_target_renaming_postoptions(src, tgt, txt, preoptions, postoptions, nativize):
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
    if 'BengaliRaBa' in postoptions and tgt == 'Bengali':
        tgt = 'BengaliRaBa'
        nativize = False
    if 'SoyomboFinals' in postoptions and tgt == 'Soyombo':
        txt = 'ʾ' + txt
    if  'BalineseSimplified' in postoptions and src == 'Balinese':
        tgt = 'BalineseSimpleRomanLoC'
    if  'JavaneseSimplified' in postoptions and src == 'Javanese':
        tgt = 'JavaneseSimpleRomanLoC'

    return src, tgt, txt, preoptions, postoptions, nativize

def _prepare_for_core_conversion(src, tgt, txt, preoptions, postoptions, nativize, ctx):
    # Thai/Lao "short vowels not shown" transcription mode - previously
    # signalled by splicing a private-use marker into txt itself and having
    # ConvertFix.FixThai/FixLaoPali check for it; now lives on ctx instead,
    # read by whichever Fix* function declares it wants ctx (no more
    # separate parameter threaded alongside ctx). Four preoptions feed
    # this same mode (verified by exhaustive grep, not just the two most
    # obviously-named ones - ThaiOrthography/LaoTranscription looked like
    # they might be unrelated but turned out to inject the identical
    # marker for the identical consumer).
    ctx.transcription_mode = ('ThaiPhonetic' in preoptions or 'LaoPhonetic' in preoptions
                               or 'ThaiOrthography' in preoptions or 'LaoTranscription' in preoptions)

    # src/tgt as they stand right before preoptions run - see Context.py's
    # comment on why this is set fresh here rather than once for the whole
    # convert() call.
    ctx.src = src
    ctx.tgt = tgt

    for options in preoptions:
      txt = Options.call_pre_option(options, txt, ctx=ctx)

    ### Semitic Switches
    if 'novowelshebrew' in preoptions and src == 'Hebr':
        txt = txt.replace('ַ', '')

    srcOld = ""

    ### retain Latin ###
    if (src != 'Latn'and src != 'Type' and SR.get(src).is_semitic) or \
        (SR.get(src).is_indic and SR.get(tgt).is_semitic and not SR.get(src).is_latin) or \
            (src in ['Hiragana', 'Katakana']):
        txt = PreProcess.retainLatin(txt)

    if src == 'Hiragana' or src == 'Katakana':
        txt = PreProcess.JapanesePreProcess(src, txt, preoptions)
        srcOld = 'Japanese'
        src = 'ISO'

    if tgt == 'Hiragana' or tgt == 'Katakana':
        txt = PostProcess.JapanesePostProcess(src, tgt, txt, nativize, postoptions)

    if src == "Oriya" and tgt == "IPA":
        txt = ConvertFix.OriyaIPAFixPre(txt)

    return src, tgt, txt, srcOld

def _run_core_conversion(src, tgt, txt, postoptions, srcOld, tgtOld, ctx):
    if src == "Itrans" and '##' in txt:
        #print('I am here tyring to do things')
        transliteration = ''
        for i, word in enumerate(txt.split("##")):
            if (i%2 == 0):
                transliteration += Convert.convertScript(word, src, tgt, ctx=ctx)
            else:
                transliteration += word
    else:
        transliteration = Convert.convertScript(txt, src, tgt, ctx=ctx)

    #print(transliteration)

    if srcOld == 'Japanese' and tgt != 'Devanagari' and 'siddhammukta' not in postoptions:
        transliteration = Convert.convertScript(transliteration, "Devanagari", "ISO")
        # print(transliteration)

    if src == tgtOld:
        tgt = tgtOld
        transliteration = Convert.convertScript(transliteration, "Devanagari", tgt)

    return tgt, transliteration

def _apply_final_postprocessing(src, tgt, txt, transliteration, nativize, preoptions, postoptions, ctx):
    # src/tgt as they stand for postoptions - re-set here rather than
    # trusting whatever _prepare_for_core_conversion set, since
    # _run_core_conversion can rename tgt (tgtOld restoration) in between.
    ctx.src = src
    ctx.tgt = tgt

    ## apply phonetic mapping for Arabic beforehand if not semitic source
    if (not SR.get(src).is_semitic and tgt == 'Arab' and nativize) or 'arabicRemoveAdditionsPhonetic' in postoptions:
        transliteration = Options.call_post_option('arabicRemoveAdditionsPhonetic', transliteration, ctx=ctx)

    #print(transliteration)

    if nativize:
      transliteration =  PostOptions.ApplyScriptDefaults(transliteration, src, tgt, postoptions, ctx)
      if tgt != 'Latn':
        if tgt != 'Tamil':
            transliteration = PostProcess.RemoveDiacritics(transliteration)
        else:
            transliteration = PostProcess.RemoveDiacriticsTamil(transliteration)

    #print(transliteration)

    if 'RemoveDiacritics' in postoptions:
      if tgt == 'Tamil':
        postoptions = map(lambda x: 'RemoveDiacriticsTamil' if x == 'RemoveDiacritics' else x, postoptions)

    for options in postoptions:
      transliteration = Options.call_post_option(options, transliteration, ctx=ctx)

    if src == "Tamil" and tgt == "IPA":
        r = requests.get("http://anunaadam.appspot.com/api?text=" + txt + "&method=2")
        r.encoding = r.apparent_encoding
        transliteration = r.text

    if src == "Oriya" and tgt == "IPA":
        transliteration = ConvertFix.OriyaIPAFix(transliteration)

    ### return Latin ###
    transliteration = PreProcess.retainLatin(transliteration, reverse=True)

    ## DefaultPostProcess ##

    transliteration = PostProcess.defaultPost(src, tgt, transliteration, nativize, preoptions, postoptions)

    return transliteration

def convert(src, tgt, txt, nativize, preoptions, postoptions):
    ctx = Context.ConversionContext()

    src, tgt, txt, preoptions, postoptions, nativize = _resolve_loc_dispatch(src, tgt, txt, preoptions, postoptions, nativize, ctx)

    ## LoC Romanizattion ends here
    ## else convert the Loc input into the associated script and then convert it into Loc
    ## Text (Loc) -> Burmese -> non-Burmese
    #if src == 'BurmeseRomanLoC' and tgt != 'Burmese':
    #    txt = convert(src, "Burmese", txt, nativize, preoptions, postoptions)
    #    src = 'Burmese'

    src, tgt, txt, preoptions, postoptions, nativize = _resolve_semitic_iso_pivot(src, tgt, txt, preoptions, postoptions, nativize)

    '''if src == "Itrans" and '##' in txt:
        textNew = [[i,word] for i, word in enumerate(txt.split("##")) if (i%2 == 0)]
        textRest = [(i,word) for i, word in enumerate(txt.split("##")) if (i%2 == 1)]

        txt = json.dumps(textNew).replace("\\n", "\n")'''

    if tgt == "" or tgt == "Ignore":
        return txt
    if preoptions == [] and postoptions == [] and nativize == False and src == tgt:
        return txt

    src, tgt, txt, preoptions, postoptions, nativize, tgtOld = _resolve_semitic_indic_naming(src, tgt, txt, preoptions, postoptions, nativize)

    txt, preoptions, postoptions = _apply_indic_dandas_preoption(src, tgt, txt, preoptions, postoptions)

    txt = PreProcess.PreProcess(txt,src,tgt,postoptions,preoptions)

    src, tgt, txt, preoptions, postoptions, nativize = _apply_target_renaming_postoptions(src, tgt, txt, preoptions, postoptions, nativize)

    #if src not in GeneralMap.SemiticScripts and tgt == 'Arab' and not nativize:
        #postoptions.append('arabicRemoveAdditionsPhonetic')

    src, tgt, txt, srcOld = _prepare_for_core_conversion(src, tgt, txt, preoptions, postoptions, nativize, ctx)

    tgt, transliteration = _run_core_conversion(src, tgt, txt, postoptions, srcOld, tgtOld, ctx)

    '''if src == "Itrans" and '##' in txt:
        textConv = {**dict(list(json.loads(transliteration.replace("\n", "\\n")))), ** dict(textRest)}
        textConv = collections.OrderedDict(sorted(textConv.items()))
        transliteration = "".join(textConv.values())'''

    return _apply_final_postprocessing(src, tgt, txt, transliteration, nativize, preoptions, postoptions, ctx)

def process(src, tgt, txt, nativize = True, post_options = [], pre_options = [], param="default"):
    if param == "default":
        return process_default(src, tgt, txt, nativize, post_options, pre_options)

    if param == "script_code":
        return process_script_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_code":
        return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)

    if param == "lang_name":
        return process_lang_name(src, tgt, txt, nativize, post_options, pre_options)

import functools

@functools.lru_cache(maxsize=None)
def _load_data(file_path):
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + file_path, 'r', encoding='utf8') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def convert_default(src, tgt, txt, nativize = True, post_options = [], pre_options = []):
    data_loaded = _load_data("/yaml/aksharamukha-scripts.yaml")

    scriptList = list(SR.SCRIPTS.keys())

    post_options = Options.normalize_post_options(post_options)
    pre_options = Options.normalize_pre_options(pre_options)

    # font hack warning
    font_hack_warning = tgt + ' uses an hacked font to display the script. In the absence of this font, you text may appear different. \n See: https://www.aksharamukha.com/describe/' + tgt + ' for the font used'

    if tgt in data_loaded and 'font_hack' in data_loaded[tgt]:
        warnings.warn(font_hack_warning)

    if src not in scriptList:
        script_not_found = 'Source script: ' + src + ' not found in the list of scripts supported. The text will not be transliterated.'
        warnings.warn(script_not_found)

    if tgt not in scriptList:
        script_not_found = 'Target script: ' + tgt + ' not found in the list of scripts supported. The text will not be transliterated.'
        warnings.warn(script_not_found)

    if (tgt == 'RomanLoC' and not SR.get(src).is_loc_script):
        script_not_found = 'The LoC romanization of ' + src + ' is not yet supported. The output text will be rendered using ISO 233 if Semitic else ISO 15919. See: https://www.aksharamukha.com/loc'
        warnings.warn(script_not_found)

    if (src == 'RomanLoC' and not SR.get(tgt).is_loc_script):
        script_not_found = 'The LoC romanization of ' + tgt + ' is not yet supported. The input text will be treated as if it was ISO 233 if Semitic else ISO 15919.. See: https://www.aksharamukha.com/loc'
        warnings.warn(script_not_found)

    return convert(src, tgt, txt, nativize, pre_options, post_options)

def process_default(src, tgt, txt, nativize, post_options, pre_options):
    scriptList = [name for name, d in SR.SCRIPTS.items() if d.is_indic or d.is_latin]
    scriptListLower = list(map(lambda x: x.lower(), scriptList))

    if src == 'autodetect':
        src = auto_detect(txt)
        #print('The autodetection is ' + src)
        pre_options = detect_preoptions(txt, src)
    elif src.lower() in scriptListLower:
        src = [script_id for script_id in scriptList if src.lower() == script_id.lower()][0]

    if tgt.lower() in scriptListLower:
        tgt = [script_id for script_id in scriptList if tgt.lower() == script_id.lower()][0]

    return convert_default(src, tgt, txt, nativize, post_options, pre_options)


def process_script_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    # Read YAML file
    data_loaded = _load_data("/yaml/aksharamukha-scripts.yaml")

    data_loaded_wiki = _load_data("/yaml/wikitra2-data.yaml")

    src = []
    tgt = []

    if src_tag == 'Syrc':
        src_tag = 'Syre'
        warnings.warn("Please specify the variety of Syriac script for the source: Estrangelo (Syre), Eastern (Syrn) or Wester (Syrj). Defaulting to Syre")
    if tgt_tag == 'Syrc':
        tgt_tag = 'Syre'
        warnings.warn("Please specify the variety of Syriac script for the target: Estrangelo (Syre), Eastern (Syrn) or Wester (Syrj). Defaulting to Syre")

    # loop through yaml to find match
    for scrpt in data_loaded.keys():
        scrpt_tag = data_loaded[scrpt]['script']

        # get the popuation of each language of the script
        if 'lang' in data_loaded[scrpt].keys():
            lang_tag = data_loaded[scrpt]['lang'].split(',')[0]
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]['lang'].split(',')))
        else:
            population = 0
            lang = ''

        #print(scrpt_tag, lang_tag)
        if scrpt_tag in data_loaded_wiki.keys() and lang_tag in data_loaded_wiki[scrpt_tag].keys():
            population = data_loaded_wiki[scrpt_tag][lang_tag]['population']
        else:
            population = 0

        # find the match in the file
        if '-' not in src_tag and data_loaded[scrpt]['script'].lower() == src_tag.lower():
            src.append((population, scrpt))

        if '-' not in tgt_tag and data_loaded[scrpt]['script'].lower() == tgt_tag.lower():
            tgt.append((population, scrpt))

        #print(population)
        # if hypthenated find the exact match
        if '-' in tgt_tag:
            lang_part = tgt_tag.split('-')[0].lower()
            script_part = tgt_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part.lower() and 'lang' in data_loaded[scrpt].keys() and lang_part.lower() in lang:
                tgt.append((0, scrpt))

        if '-' in src_tag:
            lang_part = src_tag.split('-')[0].lower()
            script_part = src_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part.lower() and 'lang' in data_loaded[scrpt].keys() and lang_part.lower() in lang:
                src.append((0, scrpt))

    if src_tag.lower() in ['latn', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. la-IAST or la-HK to select a particular scheme"
        warnings.warn(warn)

        src = [(0, 'ISO')]

    if tgt_tag.lower() in ['latn', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. la-IAST or la-HK to select a particular scheme"
        warnings.warn(warn)

        tgt = [(0, 'ISO')]

    # if latin ignore la and get the following part
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['latn', 'en', 'eng']:
        src = [(0, src_tag.split('-')[1])]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['latn', 'en', 'eng']:
        tgt = [(0, tgt_tag.split('-')[1])]

    if src_tag == 'autodetect':
        src = [(0, auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    elif SR.get(src_tag).is_semitic:
            src_pop = src_tag
    else:
        raise Exception('Source script code: ' + src_tag + ' not found')

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    elif SR.get(tgt_tag).is_semitic:
        tgt_pop = tgt_tag
    else:
        raise Exception('Target script code: ' + tgt_tag + ' not found')

    if len(src) > 1:
        warn = "Multiple orthographies, " + ','.join(map(lambda x: x[1], src)) + ", are associated with the input script. The most popular '" + src_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. ur-Arab or pa-Arab to select a particular orthography"

        warnings.warn(warn)
    if len(tgt) > 1:
        warn = "Multiple orthographies: " + ', '.join(map(lambda x: x[1], tgt)) + " are associated with the target script. The most popular '" + tgt_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. ur-Arab or pa-Arab to select a particular orthography"
        warnings.warn(warn)

    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)

def process_lang_tag(src_tag, tgt_tag, txt, nativize, post_options, pre_options):
    # Read YAML file
    data_loaded = _load_data("/yaml/aksharamukha-scripts.yaml")

    data_loaded_wiki = _load_data("/yaml/wikitra2-data.yaml")

    src = []
    tgt = []

    # iterate through the yaml file
    for scrpt in data_loaded.keys():
        if 'lang' in data_loaded[scrpt].keys():
            lang = list(map(lambda x: x.lower(), data_loaded[scrpt]['lang'].split(',')))
        else:
            lang = ''

        scrpt_tag = data_loaded[scrpt]['script']

        # try to get the popular script from wiktionary file
        if scrpt_tag in data_loaded_wiki.keys():
            script_count = len(data_loaded_wiki[scrpt_tag])
        else:
            script_count = 1

        # trying to find the match in the yaml file
        if src_tag.lower() in lang:
            src.append((script_count, scrpt))

        if tgt_tag.lower() in lang:
            tgt.append((script_count, scrpt))

        if '-' in tgt_tag:
            lang_part = tgt_tag.split('-')[0].lower()
            script_part = tgt_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                tgt.append((0, scrpt))

        if '-' in src_tag:
            lang_part = src_tag.split('-')[0].lower()
            script_part = src_tag.split('-')[1].lower()

            if scrpt_tag.lower() == script_part and lang_part in lang:
                src.append((0, scrpt))

    if src_tag.lower() in ['sa','san', 'pi', 'pli']:
        warn = "The input language: " + src_tag + " is script-agnostic and can be written in multiple scripts. The most popular 'Devanagari' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. sa-Gran or sa-Sidd to select a particular script"
        warnings.warn(warn)

        src = [(0, 'Devanagari')]

    if tgt_tag.lower() in ['sa','san', 'pi', 'pli']:
        warn = "The ouptput language: " + tgt_tag + " is script-agnostic and can be written in multiple scripts. The most popular 'Devanagari' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. sa-Gran or sa-Sidd to select a particular script"
        warnings.warn(warn)

        tgt = [(0, 'Devanagari')]

    # if sa-deva ignore sanskrita and only get deva
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['sa','san', 'pi', 'pli']:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]['script']

            if scrpt_tag.lower() == src_tag.split('-')[1].lower():
                src = [(0, scrpt)]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['sa','san', 'pi', 'pli']:
        for scrpt in data_loaded.keys():
            scrpt_tag = data_loaded[scrpt]['script']

            if scrpt_tag.lower() == tgt_tag.split('-')[1].lower():
                tgt = [(0, scrpt)]

    if src_tag.lower() in ['la', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. Latn-IAST or Latn-HK to select a particular scheme"
        warnings.warn(warn)

        src = [(0, 'ISO')]

    if tgt_tag.lower() in ['la', 'en', 'eng']:
        warn = "Latin has multiple transcription schemes. 'ISO 15919' has been selected by default"
        warn += "\n Please use a transcription format e.g. Latn-IAST or Latn-HK to select a particular scheme"
        warnings.warn(warn)

        tgt = [(0, 'ISO')]

    # if latin ignore la and get the following part
    if '-' in src_tag and src_tag.split('-')[0].lower() in ['la', 'en', 'eng']:
        src = [(0, src_tag.split('-')[1])]

    if '-' in tgt_tag and tgt_tag.split('-')[0].lower() in ['la', 'en', 'eng']:
        tgt = [(0, tgt_tag.split('-')[1])]

    if src_tag == 'autodetect':
        src = [(0,auto_detect(txt))]
        pre_options = detect_preoptions(txt, src)

    if len(src) > 0:
        src_pop = sorted(src, reverse=True)[0][1]
    else:
        raise Exception('Source language code: ' + src_tag + ' not found')

    if len(tgt) > 0:
        tgt_pop = sorted(tgt, reverse=True)[0][1]
    else:
        raise Exception('Target language code: ' + tgt_tag + ' not found')

    if len(src) > 1:
        warn = "Multiple scripts " + ','.join(map(lambda x: x[1], src)) + " associated with the input language. The most popular '" + src_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. pa-Guru or pa-Arab to select a particular script"
        warnings.warn(warn)
    if len(tgt) > 1:
        warn = "Multiple scripts " + ','.join(map(lambda x: x[1], tgt)) + " associated with the target language. The most popular '" + tgt_pop + "' has been selected"
        warn += "\n Please use the format lang_code-script_code e.g. pa-Guru or pa-Arab to select a particular script"
        warnings.warn(warn)

    return process_default(src_pop, tgt_pop, txt, nativize, post_options, pre_options)

def process_lang_name(src_name, tgt_name, txt, nativize, post_options, pre_options):
    if src_name == 'autodetect':
        src = auto_detect(txt)
        pre_options = detect_preoptions(txt, src)
    else:
        src = str(langcodes.find(src_name))

    tgt = str(langcodes.find(tgt_name))

    return process_lang_tag(src, tgt, txt, nativize, post_options, pre_options)

@functools.lru_cache(maxsize=None)
def get_semitic_json():
    from pathlib import Path
    cwd = Path(Path(__file__).parent)
    with open(Path(cwd, "json/gimeltra_data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

@functools.lru_cache(maxsize=None)
def getOptions(script):
    #json.load('')
    return

## add the new libraries to requiesments.txt in both folders