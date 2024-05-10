# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011EF1',
            '\U00011EF1\u02BD',
            '\U00011EF1\U00011EF3',
            '\U00011EF1\U00011EF3\u02BD',
            '\U00011EF1\U00011EF4',
            '\U00011EF1\U00011EF4\u02BD',
            '\U00011EED\U00011EF4\u02BD',
            '\U00011EED\U00011EF4\u02BD',
            '\U00011EEE\U00011EF4\u02BD',
            '\U00011EEE\U00011EF4\u02BD',
            '\U00011EF1\U00011EF5\u02BD',
            '\U00011EF1\U00011EF1\U00011EF3\u02BD',
            '\U00011EF1\U00011EF6\u02BD',
            '\U00011EF1\U00011EF1\U00011EF4\u02BD',
            ]

SouthVowelMap = [
                '\U00011EF1\U00011EF5',
                '\U00011EF1\U00011EF6',
                ]

ModernVowelMap = [
                 '\U00011EF1\U00011EF5\u02BD',
                 '\U00011EF1\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011EF1\u02BD'
                  ]

VowelSignMap =  [
                '\u02BD\u02BD',
                '\U00011EF3',
                '\U00011EF3\u02BD',
                '\U00011EF4',
                '\U00011EF4\u02BD',
                '\U00011EED\U00011EF4\u02BD',
                '\U00011EED\U00011EF4\u02BD',
                '\U00011EEE\U00011EF4\u02BD',
                '\U00011EEE\U00011EF4\u02BD',
                '\U00011EF5\u02BD',
                '\U00011EF1\U00011EF3\u02BD',
                '\U00011EF6\u02BD',
                '\U00011EF1\U00011EF4\u02BD',
                ]

SouthVowelSignMap = [
                '\U00011EF5',
                '\U00011EF6',
                    ]

ModernVowelSignMap =[
                '\U00011EF5\u02BD',
                     '\u02BD\u02BD\u02BD',
                    ]

SinhalaVowelSignMap = [
                '\U00011EF5\u02BD',
                      ]

AyogavahaMap = [
               '\U00011EE5\u02BD',
               '\U00011EE5\u02BD',
               '\u02BD\u02BD\u02BD'
               ]

ViramaMap =  [
             '\u02BE'
             ]

ConsonantMap =  [
                '\U00011EE0',
                '\U00011EE0\u02BD',
                '\U00011EE1',
                '\U00011EE1\u02BD',
                '\U00011EE2',

                '\U00011EE9',
                '\U00011EE9\u02BD',
                '\U00011EEA',
                '\U00011EEA\u02BD',
                '\U00011EEB',

                '\U00011EE6\u02BD',
                '\U00011EE6\u02BD',
                '\U00011EE7\u02BD',
                '\U00011EE7\u02BD',
                '\U00011EE8\u02BD',

                '\U00011EE6',
                '\U00011EE6\u02BD',
                '\U00011EE7',
                '\U00011EE7\u02BD',
                '\U00011EE8',

                '\U00011EE3',
                '\U00011EE3\u02BD',
                '\U00011EE4',
                '\U00011EE4\u02BD',
                '\U00011EE5',

                '\U00011EEC',
                '\U00011EED',
                '\U00011EEE',
                '\U00011EEF',

                '\U00011EF0\u02BD',
                '\U00011EF0\u02BD',
                '\U00011EF0',
                '\U00011EE0\u02BD'
                ]

SouthConsonantMap = [
                    '\U00011EEE\u02BD',
                    '\U00011EEE\u02BD',
                    '\U00011EED\u02BD',
                    '\U00011EE8\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\U00011EE0\u02BD',
                     '\U00011EE0\u02BD',
                     '\U00011EE1\u02BD',
                     '\U00011EEA\u02BD',
                     '\U00011EE7\u02BD',
                     '\U00011EE7\u02BD',
                     '\U00011EE3\u02BD',
                     '\U00011EEC\u02BD'
                     ]
SinhalaConsonantMap =[
                     '\U00011EE5\U00011EE1\u02BD',
                     '\U00011EE5\U00011EEA\u02BD',
                     '\U00011EE5\U00011EE7\u02BD',
                     '\U00011EE5\U00011EE7\u02BD',
                     '\U00011EE5\U00011EE4\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        '\U00011EF1\U00011EF6\U00011EE5\u02BD'
        ]

SignMap =[
         "\u02BD\u02BD",
         '\U00011EF7',
         '\U00011EF7\U00011EF7'
         ]

Aytham =[AyogavahaMap[2]+'\u02BC']

NumeralMap = [
             '\u06F0',
             '\u06F1',
             '\u06F2',
             '\u06F3',
             '\u06F4',
             '\u06F5',
             '\u06F6',
             '\u06F7',
             '\u06F8',
             '\u06F9',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
