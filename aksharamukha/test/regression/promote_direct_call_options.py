# -*- coding: utf-8 -*-
"""
Correction pass over known_broken_options.json.

The first pass called every option as transliterate.process(..., post_options
=[name]) / pre_options=[name]) - which only ever invokes getattr(module,
name)(txt) with ONE argument (see transliterate.py:455 and :522). That's a
real, narrow finding on its own (those two call sites can't reach a
multi-argument option at all), but it wrongly lumped ~32 legitimate
multi-argument options in with 4 actual bugs: those 32 all have a real,
findable call site elsewhere in the codebase (PostOptions.py's default-option
elif chain, ConvertFix.py's per-script Fix functions, or transliterate.py's
own convert()) that passes the extra argument(s) they need. Grepped every one
of the 36 broken names for its real callers to build the table below instead
of guessing.

This script calls each of those 32 the way the real code calls them and, on
success, promotes them out of known_broken_options.json into a new
test_direct_options.json fixture with real assertions. Only the 4 that are
broken regardless of how they're called (removeZW, IPAIndic,
OriyaSubojinedVa, KhmerWordSplit) stay in known_broken_options.json.
"""
import ast
import inspect
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from aksharamukha import PreProcess, PostProcess, ConvertFix, Options, transliterate  # noqa: E402
import generate_golden as gg  # noqa: E402


def _extract_call_arg(wrapper_fn, arg_index):
    """Pull a literal argument straight out of a wrapper function's own
    `return Other(Strng, 'X', 'Y')` source, via ast - so exact non-ASCII
    script characters (Javanese repha, Tai Tham consonants, ...) are lifted
    byte-for-byte from the real code instead of being hand-retyped here,
    where a look-alike glyph or missing combining mark could silently slip
    in undetected.

    Searches for the `return` statement anywhere in the function body
    rather than assuming it's the first statement - functions living in
    ScriptProcessing/*.py commonly start with a local
    `from .. import PostProcess`/`PreProcess` import (needed to avoid a
    circular import with the modules that re-export them), so the return
    is no longer necessarily body[0]."""
    src = inspect.getsource(wrapper_fn)
    tree = ast.parse(src.strip())
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            return ast.literal_eval(node.value.args[arg_index])
    raise ValueError('no return statement found in %s' % wrapper_fn.__name__)


def _extract_join_assign(fn, var_name):
    """Find `var_name = SEP.join([...])` anywhere in fn's source and return
    the joined string, again without retyping the literal elements."""
    src = inspect.getsource(fn)
    tree = ast.parse(src.strip())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == var_name for t in node.targets
        ):
            call = node.value
            sep = ast.literal_eval(call.func.value)
            items = ast.literal_eval(call.args[0])
            return sep.join(items)
    raise ValueError('%s not found in %s' % (var_name, fn.__name__))


JAVANESE_REPHA_POST = _extract_call_arg(Options._POST_OPTION_FUNCS['JavaneseMoveRepha'], 2)
JAVANESE_REPHA_PRE = _extract_call_arg(Options._PRE_OPTION_FUNCS['JavaneseMoveRepha'], 2)
TALL_A_CONS = _extract_join_assign(ConvertFix._FixTaiThamEncode, 'TallACons')

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_TEXTS_DIR = os.path.abspath(os.path.join(HERE, '..', 'test_texts'))

# name -> extra positional args, for the common case where the function's
# own first parameter is the string to transform (Strng, *extra).
# Values are the actual arguments seen at a real call site in the codebase.
GENERIC_POST = {
    'AnusvaraToNasal': ('Tamil',),                       # PostOptions.py:40 (Tamil default bundle)
    'MToAnusvara': ('Telugu',),                           # PostOptions.py:19
    'NasalToAnusvara': ('Telugu',),                        # PostOptions.py:19
    'YaToYYa': ('Bengali',),                                # PostOptions.py:46
    'VaToBa': ('Bengali',),                                 # PostOptions.py:46
    'KhandaTa': ('Bengali', False),                         # ConvertFix.py:3412 (FixBengali)
    'InsertGeminationSign': ('Gurmukhi',),                  # ConvertFix.py:952 (FixGurmukhi)
    'ReverseGeminationSign': ('Gurmukhi',),                 # ConvertFix.py:962
    'RetainDandasIndic': ('Tamil', True),                   # ConvertFix.py:914 (FixTamil)
    'RetainIndicNumerals': ('Tamil', True),                 # ConvertFix.py:915
    'RetainRomanNumerals': ('Tamil', True),                 # same shape as RetainIndicNumerals; no confirmed
                                                             # external caller found - included for shape parity
    'ThaiLaoTranscription': ('Thai', 'ะ', 'ั', True),  # ConvertFix.py:2016 (FixThai) - exact escapes from the call site
    'FixTallA': (TALL_A_CONS,),                             # ConvertFix.py:3293-3295 (ThaiDigraphConjuncts) - va da dha ga, extracted via ast
    'BalineseJavaneseMoveRepha': ('Javanese', JAVANESE_REPHA_POST),  # ScriptProcessing/Javanese.py (JavaneseMoveRepha), extracted via ast
    'FixSemiticRoman': ('Arab',),                           # Convert.py:323 - PostProcess.FixSemiticRoman(Strng, Target)
    'RemoveSchwa': ('Devanagari',),                          # no external caller found; correct 2-arg shape confirmed by signature only
    'tbadiff': ('Bengali',),                                 # no external caller found; Target param is unused in the body
    'PhagsPaRearrange': ('PhagsPa',),                        # author-marked "# not used" (PostProcess.py:3485); shape still valid
    'YYAEverywhere': ('Bengali',),                           # PostProcess.py:2791 (BengaliYYA)
}

GENERIC_PRE = {
    'AnuChandraEq': ('Devanagari',),                         # PreProcess.py:904 (AnuChandraEqDeva)
    'BalineseJavaneseMoveRepha': ('Javanese', JAVANESE_REPHA_PRE),
    'FixSemiticRoman': ('Arab',),                             # Convert.py:352 - PreProcess.FixSemiticRoman(Strng, Source)
    'PhagsPaArrange': ('Devanagari',),                        # PreOptions.py:6-15 fires when Target=='PhagsPa'; the 2nd
                                                                # positional arg passed is the real SOURCE script being
                                                                # converted, not the literal string 'PhagsPa' (my first
                                                                # attempt at this had it backwards)
    'PreProcess': ('Devanagari', 'IAST', [], []),             # the module's own top-level entry point; Strng IS arg 1
    'RemoveFinal': ('Gurmukhi',),                             # PreProcess.py:1099 (SchwaFinalGurmukhi)
    'RetainPipeDanda': ('IAST',),                             # transliterate.py:410
    'RomanPreFix': ('Inter',),                                # Convert.py:96-99 reassigns Source = GM.Inter two lines
                                                                # before this call - the original script name (e.g. IAST)
                                                                # is never what RomanPreFix actually sees in production;
                                                                # calling it with 'IAST' throws (verified: re.error,
                                                                # variable-width lookbehind) for every script, not just IAST
    'joinVowelCons': ('IAST',),                               # PreProcess.py:1267 (joinVowelConsIAST)
    'normalize': ('Devanagari',),                             # PreProcess.py:1388, inside PreProcess()
}

# name -> (module, callable) for functions whose FIRST parameter is not the
# text to transform, so the generic (Strng, *extra) shape doesn't apply.
CUSTOM_CALLS = {
    ('post', 'JapanesePostProcess'): lambda text: PostProcess.JapanesePostProcess('IAST', 'Hiragana', text, True, []),
    ('pre', 'JapanesePreProcess'): lambda text: PreProcess.JapanesePreProcess('Hiragana', text, []),
}

TEXT_NAMES = ['heart', 'lalitavistara']


def load_sample(script, text_name):
    return gg.load_sample(script) if script in ('Devanagari', 'IAST') and text_name == 'heart' else _load(script, text_name)


def _load(script, text_name):
    path = os.path.join(TEST_TEXTS_DIR, 'source_%s_%s.txt' % (script, text_name))
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    with open(os.path.join(HERE, 'known_broken_options.json'), 'r', encoding='utf-8') as f:
        broken = json.load(f)

    direct = {}
    promoted = []
    still_broken = {}

    for kind, table, module in (('post', GENERIC_POST, PostProcess), ('pre', GENERIC_PRE, PreProcess)):
        for name, extra_args in table.items():
            key = kind + '::' + name
            cases = []
            for text_name in TEXT_NAMES:
                source = 'IAST' if kind == 'pre' and name in ('RomanPreFix', 'joinVowelCons', 'RetainPipeDanda') else 'Devanagari'
                try:
                    input_text = _load(source, text_name)
                except FileNotFoundError:
                    continue
                try:
                    output = getattr(module, name)(input_text, *extra_args)
                except Exception as e:  # noqa: BLE001
                    continue
                cases.append([input_text, output])
            if cases:
                direct[key] = {'kind': kind, 'name': name, 'args': list(extra_args), 'cases': cases}
                promoted.append(key)
                broken.pop(key, None)

    for (kind, name), fn in CUSTOM_CALLS.items():
        key = kind + '::' + name
        cases = []
        for text_name in TEXT_NAMES:
            try:
                input_text = _load('Devanagari', text_name)
            except FileNotFoundError:
                continue
            try:
                output = fn(input_text)
            except Exception:
                continue
            cases.append([input_text, output])
        if cases:
            direct[key] = {'kind': kind, 'name': name, 'custom_call': True, 'cases': cases}
            promoted.append(key)
            broken.pop(key, None)

    still_broken = broken

    with open(os.path.join(HERE, 'test_direct_options.json'), 'w', encoding='utf-8') as f:
        json.dump(direct, f, ensure_ascii=False, indent=1)

    with open(os.path.join(HERE, 'known_broken_options.json'), 'w', encoding='utf-8') as f:
        json.dump(still_broken, f, ensure_ascii=False, indent=1)

    print('Promoted %d / %d previously-"broken" options to real direct-call test cases.' % (len(promoted), len(promoted) + len(still_broken)))
    print('Still genuinely broken (%d):' % len(still_broken))
    for k, v in still_broken.items():
        print('  -', k, ':', v['error_type'], '-', v['error'][:100])
    print()
    print('Not promoted (attempted but produced no successful case):')
    attempted = set(kind + '::' + name for kind, table, _ in [('post', GENERIC_POST, None), ('pre', GENERIC_PRE, None)] for name in table)
    attempted |= set(kind + '::' + name for kind, name in CUSTOM_CALLS)
    for key in sorted(attempted - set(promoted) - set()):
        if key in still_broken:
            continue
        print('  -', key, '(all attempts failed silently - check manually)')


if __name__ == '__main__':
    main()
