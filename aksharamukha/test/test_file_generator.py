from aksharamukha import transliterate, GeneralMap

target_scripts = GeneralMap.IndicScripts + GeneralMap.Roman + GeneralMap.SemiticScripts

source_scripts = ['Devanagari', 'IAST']
source_texts = ['heart', 'lalitavistara', 'short']

for source_script in source_scripts:
    for target_script in target_scripts:
        for text in source_texts:
            with open('test_texts/test_' + source_script + '_' + target_script +  '_' + text + '.txt', 'w') as fo:
                with open('test_texts/source_' + source_script + '_' + text + '.txt', 'r') as fi:
                    fo.write(transliterate.process(source_script, target_script, fi.read()))
