# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\u0D85',
            '\u0D86',
            '\u0D89',
            '\u0D8A',
            '\u0D8B',
            '\u0D8C',
            '\u0D8D',
            '\u0D8E',
            '\u0D8F',
            '\u0D90',
            '\u0D92',
            '\u0D93',
            '\u0D95',
            '\u0D96',
            ]

SouthVowelMap = [
                '\u0D91',
                '\u0D94',
                ]

ModernVowelMap = [
                 '\u0D87',
                 '\u0D86\u02BC',
                 ]

SinhalaVowelMap = [
                  '\u0D88'
                  ]

VowelSignMap =  [
                '\u0DCF',
                '\u0DD2',
                '\u0DD3',
                '\u0DD4',
                '\u0DD6',
                '\u0DD8',
                '\u0DF2',
                '\u0DDF',
                '\u0DF3',
                '\u0DDA',
                '\u0DDB',
                '\u0DDD',
                '\u0DDE',
                ]

SouthVowelSignMap = [
                    '\u0DD9',
                    '\u0DDC',
                    ]

ModernVowelSignMap =[
                    '\u0DD0',
                    '\u0DCF\u02BC']

SinhalaVowelSignMap = [
                      '\u0DD1'
                      ]

AyogavahaMap = [
               '\u0D81',
               '\u0D82',
               '\u0D83'
               ]

ViramaMap =  [
             '\u0DCA'
             ]

ConsonantMap =  [
                '\u0D9A',
                '\u0D9B',
                '\u0D9C',
                '\u0D9D',
                '\u0D9E',

                '\u0DA0',
                '\u0DA1',
                '\u0DA2',
                '\u0DA3',
                '\u0DA4',

                '\u0DA7',
                '\u0DA8',
                '\u0DA9',
                '\u0DAA',
                '\u0DAB',

                '\u0DAD',
                '\u0DAE',
                '\u0DAF',
                '\u0DB0',
                '\u0DB1',

                '\u0DB4',
                '\u0DB5',
                '\u0DB6',
                '\u0DB7',
                '\u0DB8',

                '\u0DBA',
                '\u0DBB',
                '\u0DBD',
                '\u0DC0',

                '\u0DC1',
                '\u0DC2',
                '\u0DC3',
                '\u0DC4'
                ]

SouthConsonantMap = [
                    '\u0DC5',
                    '\u0DC5\u00B7',
                    '\u0DBB\u00B7',
                    '\u0DB1\u00B7'
                    ]

NuktaConsonantMap =  [
                     '\u0D9A\u00B7',
                     '\u0D9B\u00B7',
                     '\u0D9C\u00B7',
                     '\u0DA2\u00B7',
                     '\u0DA9\u00B7',
                     '\u0DAA\u00B7',
                     '\u0DC6',
                     '\u0DBA\u00B7'
                     ]

SinhalaConsonantMap =[
                     '\u0D9F',
                     '\u0DA6',
                     '\u0DAC',
                     '\u0DB3',
                     '\u0DB9'
                      ]

NuktaMap = [
           '\u00B7'
           ]

OmMap = [
        '\u0D95\u0D82'
        ]

SignMap =[
         '\u0028\u0D85\u0029',
         '\u002E',
         '\u002E\u002E'
         ]

Aytham =[AyogavahaMap[2]+'\u02BC']

NumeralMap = [
             '\u0DE6',
             '\u0DE7',
             '\u0DE8',
             '\u0DE9',
             '\u0DEA',
             '\u0DEB',
             '\u0DEC',
             '\u0DED',
             '\u0DEE',
             '\u0DEF',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
