# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\uA984',
            '\uA984\uA9B4',
            '\uA986',
            '\uA987',
            '\uA988',
            '\uA988\uA9B4',
            'ꦫꦶ\u02BD',
            'ꦫꦷ\u02BD',
            'ꦭꦶ\u02BD',
            'ꦭꦷ\u02BD',
            '\uA98C',
            '\uA98D',
            '\uA98E',
            '\uA98E\uA9B4',
            ]

SouthVowelMap = [
                '\uA98C\u02BD',
                '\uA98E\u02BD',
                ]

ModernVowelMap = [
                '\uA98C\u02BD',
                 '\uA984\uA9B4\u02BD',
                 ]

SinhalaVowelMap = [
                '\uA98C\u02BD',
                  ]

VowelSignMap =  [
                '\uA9B4',
                '\uA9B6',
                '\uA9B7',
                '\uA9B8',
                '\uA9B9',
            '\uA9C0ꦫꦶ\u02BD',
            '\uA9C0ꦫꦷ\u02BD',
            '\uA9C0ꦭꦶ\u02BD',
            '\uA9C0ꦭꦷ\u02BD',
                '\uA9BA',
                '\uA9BB',
                '\uA9BA\uA9B4',
                '\uA9BB\uA9B4',
                ]

SouthVowelSignMap = [
                    '\uA9BA\u02BD',
                    '\uA9BA\uA9B4\u02BD',
                    ]

ModernVowelSignMap =[
                    '\uA9BA\u02BD',
                    '\uA9B4\u02BD']

SinhalaVowelSignMap = [
                    '\uA9BA\u02BD',
                      ]

AyogavahaMap = [
               '\uA981\u02BD',
               '\uA981',
               '\uA983'
               ]

ViramaMap =  [
             '\uA9C0'
             ]

ConsonantMap =  [
                '\uA98F',
                '\uA991',
                '\uA992',
                '\uA993',
                '\uA994',

                '\uA995',
                '\uA996',
                '\uA997',
                '\uA999',
                '\uA99A',

                '\uA99B',
                '\uA99C',
                '\uA99D',
                '\uA99E',
                '\uA99F',

                '\uA9A0',
                '\uA9A1',
                '\uA9A2',
                '\uA9A3',
                '\uA9A4',

                '\uA9A5',
                '\uA9A6',
                '\uA9A7',
                '\uA9A8',
                '\uA9A9',

                '\uA9AA',
                '\uA9AB',
                '\uA9AD',
                '\uA9AE',

                '\uA9AF',
                '\uA9B0',
                '\uA9B1',
                '\uA9B2'
                ]

SouthConsonantMap = [
                    '\uA9AD\u02BD',
                    '\uA9B0\u02BD',
                    '\uA9AB\u02BD',
                    '\uA9A4\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\uA98F\u02BD',
                     '\uA991\u02BD',
                     '\uA992\u02BD',
                     '\uA997\u02BD',
                     '\uA99D\u02BD',
                     '\uA99E\u02BD',
                     '\uA9A6\u02BD',
                     '\uA9AA\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\uA981\uA992\u02BD',
                     '\uA981\uA997\u02BD',
                     '\uA981\uA99D\u02BD',
                     '\uA981\uA9A2\u02BD',
                     '\uA981\uA9A7\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD'
           ]

OmMap = [
        '\uA98E\uA981'
        ]

SignMap =[
         '\u0027',
         '|',
         '||'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']


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
