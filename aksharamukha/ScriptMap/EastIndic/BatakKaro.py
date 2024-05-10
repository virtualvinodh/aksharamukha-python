# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\u1BC0',
            '\u1BC0\u02BD',
            '\u1BE4',
            '\u1BE4\u02BD',
            '\u1BE5',
            '\u1BE5\u02BD',
            '\u1BD2\u1BEC\u02BD',
            '\u1BD2\u1BEC\u02BD',
            'ᯞᯬ\u02BD',
            'ᯞᯬ\u02BD',
            '\u1BE4\u02BD',
            '\u1BC0\u1BE4\u02BD',
            '\u1BE5\u02BD',
            '\u1BC0\u1BE5\u02BD',
            ]

SouthVowelMap = [
                '\u1BE4\u02BD',
                '\u1BE5\u02BD',
                ]

ModernVowelMap = [
                 '\u1BE4\u02BD',
                 '\u1BC0\u02BD',
                 ]

SinhalaVowelMap = [
                  '\u1BE4\u02BD'
                  ]

VowelSignMap =  [
                '\u02BD',
                '\u1BEB',
                '\u1BEB\u02BD',
                '\u1BEC',
                '\u1BEC\u02BD',
                '\u1BD2\u1BEC\u02BD',
                '\u1BD2\u1BEC\u02BD',
                'ᯞᯬ\u02BD',
                'ᯞᯬ\u02BD',
                '\u1BE9\u02BD',
                '\u1BE4\u02BD',
                '\u1BED\u02BD',
                '\u1BE5\u02BD',
                ]

SouthVowelSignMap = [
                     '\u1BE9',
                     '\u1BED',
                    ]

ModernVowelSignMap =[
                     '\u1BE7',
                     '\u02BD',
                    ]

SinhalaVowelSignMap = [
                      '\u1BE9\u02BD'
                      ]

AyogavahaMap = [
               '\u1BF0\u02BD',
               '\u1BF0',
               '\u1BF1'
               ]

ViramaMap =  [
             '\u1BF3'
             ]

ConsonantMap =  [
                '\u1BC2',
                '\u1BC2\u02BD',
                '\u1BCE',
                '\u1BCE\u02BD',
                '\u1BDD',

                '\u1BE1',
                '\u1BE1\u02BD',
                '\u1BD0',
                '\u1BD0\u02BD',
                '\u1BC9\u02BD',

                '\u1BD7\u02BD',
                '\u1BD7\u02BD',
                '\u1BD1\u02BD',
                '\u1BD1\u02BD',
                '\u1BC9\u02BD',

                '\u1BD7',
                '\u1BD7\u02BD',
                '\u1BD1',
                '\u1BD1\u02BD',
                '\u1BC9',

                '\u1BC7',
                '\u1BC7\u02BD',
                '\u1BC6',
                '\u1BC6\u02BD',
                '\u1BD4',

                '\u1BDB',
                '\u1BD2',
                '\u1BDE',
                '\u1BCB',

                '\u1BD8\u02BD',
                '\u1BD8\u02BD',
                '\u1BD8',
                '\u1BC0\u02BD'
                ]

SouthConsonantMap = [
                    '\u1BDE\u02BD',
                    '\u1BDE\u02BD',
                    '\u1BD2\u02BD',
                    '\u1BC9\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\u1BC2\u02BD',
                     '\u1BC2\u02BD',
                     '\u1BCE\u02BD',
                     '\u1BD0\u02BD',
                     '\u1BD1\u02BD',
                     '\u1BD1\u02BD',
                     '\u1BC7\u02BD',
                     '\u1BDB\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\u1BF0\u1BCE\u02BD',
                     '\u1BF0\u1BD0\u02BD',
                     '\u1BE2\u02BD',
                     '\u1BE2',
                     '\u1BE3',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        'ᯥᯔ᯳\u02BD'
        ]

SignMap =[
         "'",
         '\u002E',
         '\u002E'
         ]

Aytham =[AyogavahaMap[2]+'\u02BC']

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
