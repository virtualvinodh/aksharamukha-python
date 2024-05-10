# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\u1BC0',
            '\u1BC0\u02BD',
            '\u1BE4',
            '\u1BE4\u02BD',
            '\u1BE5',
            '\u1BE5\u02BD',
            'ᯒᯮ\u02BD',
            'ᯒᯮ\u02BD',
            'ᯞᯮ\u02BD',
            'ᯞᯮ\u02BD',
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
                '\u02BD\u02BD',
                '\u1BEA',
                '\u1BEA\u02BD',
                '\u1BEE',
                '\u1BEE\u02BD',
                'ᯒᯮ\u02BD',
                'ᯒᯮ\u02BD',
                'ᯞᯮ\u02BD',
                'ᯞᯮ\u02BD',
                '\u1BE9\u02BD',
                '\u1BE4\u02BD',
                '\u1BEC\u02BD',
                '\u1BE5\u02BD',
                ]

SouthVowelSignMap = [
                     '\u1BE9',
                     '\u1BEC',
                    ]

ModernVowelSignMap =[
                     '\u1BE9\u02BD',
                     '\u02BD\u02BD',
                    ]

SinhalaVowelSignMap = [
                      '\u1BE9\u02BD'
                      ]

AyogavahaMap = [
               '\u1BF0\u02BD',
               '\u1BF0',
               '\u1BC4\u1BF2\u02BD'
               ]

ViramaMap =  [
             '\u1BF2'
             ]

ConsonantMap =  [
                '\u1BC4\u1BE6',
                '\u1BC4\u1BE6\u02BD',
                '\u1BCE',
                '\u1BCE\u02BD',
                '\u1BDD',

                '\u1BDA\u1BE6',
                '\u1BDA\u1BE6\u02BD',
                '\u1BD0',
                '\u1BD0\u02BD',
                '\u1BE0',

                '\u1BD6\u02BD',
                '\u1BD6\u02BD',
                '\u1BD1\u02BD',
                '\u1BD1\u02BD',
                '\u1BCA\u02BD',

                '\u1BD6',
                '\u1BD6\u02BD',
                '\u1BD1',
                '\u1BD1\u02BD',
                '\u1BCA',

                '\u1BC7',
                '\u1BC7\u02BD',
                '\u1BC5',
                '\u1BC5\u02BD',
                '\u1BD4',

                '\u1BDB',
                '\u1BD2',
                '\u1BDE',
                '\u1BCD',

                '\u1BDA\u02BD',
                '\u1BDA\u02BD',
                '\u1BDA',
                '\u1BC4'
                ]

SouthConsonantMap = [
                    '\u1BDE\u02BD',
                    '\u1BDE\u02BD',
                    '\u1BD2\u02BD',
                    '\u1BCA\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\u1BC4\u1BE6\u02BD',
                     '\u1BC4\u1BE6\u02BD',
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
                     '\u1BF0\u1BD1\u02BD',
                     '\u1BF0\u1BD1\u02BD',
                     '\u1BF0\u1BC5\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        'ᯥᯔ᯲\u02BD'
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
