# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            'â',
            'ā̂', # A
            'î', #i
            'ī̂', #I
            'û', # u
            'ū̂', # U
            'ru\u02BD',
            'rū\u02BD',
            'lu\u02BD',
            'lū\u02BD',
            'ē̂', #e
            'âŷ', #ai
            'ō̂', #o
            'âŵ' #au
            ]

SouthVowelMap = [
                'ê',
                'ô'
                ]

ModernVowelMap = [
                 'ē̂\u02BD',
                 'ā̂\u02BD'
                 ]

SinhalaVowelMap = [
                  'ê\u02BD'
                  ]

VowelSignMap =  [
            'ā', # A
            'i', #i
            'ī', #I
            'u', # u
            'ū', # U
            '\u033Dru\u02BD',
            '\u033Drū\u02BD',
            '\u033Dru\u02BD',
            '\u033Drū\u02BD',
            'ē', #e
            'aŷ', #ai
            'ō', #o
            'aŵ' #au
]

SouthVowelSignMap = ['e','o']

ModernVowelSignMap = ['e\u02BD','ā\u02BD']

SinhalaVowelSignMap = [
                  'ē\u02BD'
                  ]

AyogavahaMap = [
               'ₘ',
               'ₘ', ## Check nasalization
               'h\u033D\u02BD'
               ]

ViramaMap =  [
             '\u033D'
             ]

ConsonantMap =  [
                'k',
                'kʰ',
                'g',
                'gʰ',
                'n\u02BD',

                'č',
                'čʰ',
                'j',
                'jʰ',
                'ɲ',

                'ʈ',
                'ʈʰ',
                'ɖ',
                'ɖʰ',
                'ɳ',

                't',
                'tʰ',
                'd',
                'dʰ',
                'n',

                'p',
                'pʰ',
                'b',
                'bʰ',
                'm',

                'y',
                'r',
                'l',
                'v',

                'š',
                'ʂ',
                's',
                'h',
                ]

SouthConsonantMap = [
                    'ɭ',
                    'ɭ\u02BD',
                    'r\u02BD',
                    'n\u02BD'
                    ]

NuktaConsonantMap =  [
                     'q',
                     'ḫ',
                     'ġ',
                     'z',
                     'ɽ',
                     'ɽʰ',
                     'f',
                     'y\u02BD'
                     ]

SinhalaConsonantMap =[
                     'n\u033Dg\u02BD',
                     'n\u033Dj\u02BD',
                     'n\u033Dd\u02BD',
                     'n\u033Dd\u02BD',
                     'm\u033Db\u02BD',
                      ]

NuktaMap = [
           'Q'
           ]

OmMap = [
        'ō̂m\u033D\u02BD'
        ]

SignMap =[
         '\u02BD\u02BD\u02BD\u02BD',
         '.',
         '..'
         ]

Aytham =['h\u033D\u02BD']

NumeralMap = [
             '\u0030',
             '\u0031',
             '\u0032',
             '\u0033',
             '\u0034',
             '\u0035',
             '\u0036',
             '\u0037',
             '\u0038',
             '\u0039',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])