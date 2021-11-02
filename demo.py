from aksharamukha import transliterate

print(transliterate.process('hk', 'siddham', 'buddhaH'))

print(transliterate.process('autodetect', 'iast', 'ꯃꯤꯇꯩ_ꯃꯌꯦꯛ'))

print(transliterate.process('HK', 'Tamil', 'maMgaLa', False))

print(transliterate.process('HK', 'Tamil', 'bRhaspati gaMgA', False, post_options = ['TamilSubScript','TamilRemoveApostrophe']))

print(transliterate.process('Thai', 'Devanagari', 'พุทธัง สะระณัง คัจฉามิ', pre_options=['ThaiOrthography']))

print(transliterate.process('autodetect', 'IAST', 'พุทธัง สะระณัง คัจฉามิ'))

print(transliterate.process('autodetect', 'Vatteluttu', 'พุทธัง สะระณัง คัจฉามิ'))

print(transliterate.auto_detect('ꯃꯤꯇꯩ_ꯃꯌꯦꯛ'))

print(transliterate.process('Devanagari', 'IAST', 'धर्म भारत की श्रमण परम्परा से निकला धर्म और दर्शन है', pre_options=['RemoveSchwaHindi']))

print(transliterate.process('deva', 'taml', 'धर्म भारत की ', param="script_code"))

print(transliterate.process('hi', 'ur', 'धर्म भारत की ', param="lang_code"))

print(transliterate.process('sanskrit', 'telugu', 'धर्म भारत की ', param="lang_name"))

print(transliterate.process('hindi', 'kannada', 'धर्म भारत की ', param="lang_name"))

print(transliterate.process('devanagari', 'granthapandya', 'धर्म'))

print(transliterate.process('hi', 'pa', 'धर्म भारत की ', param="lang_code"))
print(transliterate.process('deva', 'arab', 'धर्म भारत की ', param="script_code"))
print(transliterate.process('autodetect', 'latn-iast', 'धर्म भारत की ', param="script_code"))
print(transliterate.process('la-hK', 'pa-guru', 'namo buddhAya', param="lang_code"))

print(transliterate.process('hi-Deva', 'hi-kthi', 'धर्म भारत की ', param="lang_code"))
print(transliterate.process('hi-Deva', 'mak', 'धर्म भारत की ', param="lang_code"))
print(transliterate.process('hi-Deva', 'cyrl', 'धर्म भारत की ', param="script_code"))
print(transliterate.process('sa-Deva', 'ru', 'धर्म भारत की ', param="lang_code"))



## multiple orthographies associated with script example

