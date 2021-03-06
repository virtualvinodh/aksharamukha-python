from aksharamukha import transliterate

print(transliterate.process('HK', 'Siddham', 'buddhaH'))

print(transliterate.process('autodetect', 'IAST', 'ꯃꯤꯇꯩ_ꯃꯌꯦꯛ'))

print(transliterate.process('HK', 'Tamil', 'maMgaLa', False))

print(transliterate.process('HK', 'Tamil', 'bRhaspati gaMgA', False, post_options = ['TamilSubScript','TamilRemoveApostrophe']))

print(transliterate.process('Thai', 'Devanagari', 'พุทธัง สะระณัง คัจฉามิ', pre_options=['ThaiOrthography']))

print(transliterate.process('autodetect', 'IAST', 'พุทธัง สะระณัง คัจฉามิ'))

print(transliterate.process('autodetect', 'Vatteluttu', 'พุทธัง สะระณัง คัจฉามิ'))

print(transliterate.auto_detect('ꯃꯤꯇꯩ_ꯃꯌꯦꯛ'))

print(transliterate.process('Devanagari', 'IAST', 'धर्म भारत की श्रमण परम्परा से निकला धर्म और दर्शन है', pre_options=['RemoveSchwaHindi']))

print(transliterate.process_script_tag('deva', 'taml', 'धर्म भारत की '))

print(transliterate.process_lang_tag('hi', 'te', 'धर्म भारत की '))

print(transliterate.process_lang_name('hindi', 'telugu', 'धर्म भारत की '))

