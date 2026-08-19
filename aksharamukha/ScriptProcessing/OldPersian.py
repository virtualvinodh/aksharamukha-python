# -*- coding: utf-8 -*-

# OldPersian's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

def FixOldPersian(Strng,reverse=False):
    Strng = OldPersianSyllable(Strng,reverse)
    Strng = OldPersianNumeral(Strng,reverse)

    return Strng

def OldPersianSyllable(Strng,reverse=True):
    ICons = [x+'\U000103A1' for x in ['\U000103AD','\U000103B6','\U000103A9','\U000103BA','\U000103AB','\U000103B4','\U000103BC']]
    ICons_ = [x+'_\U000103A1' for x in ['\U000103AD','\U000103B6','\U000103A9','\U000103BA','\U000103AB','\U000103B4','\U000103BC']]
    ISyll = [x+'\U000103A1' for x in ['\U000103AE','\U000103B7','\U000103AA','\U000103BB','\U000103AB','\U000103B4','\U000103BC']]

    UCons = [x+'\U000103A2' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103AB','\U000103B4','\U000103BC']]
    UCons_ = [x+'_\U000103A2' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103AB','\U000103B4','\U000103BC']]
    USyll = [x+'\U000103A2' for x in ['\U000103AF','\U000103B8','\U000103A4','\U000103A6','\U000103AC','\U000103B5','\U000103BD']]

    ACons = [x+'<\U000103A0' for x in ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103A9','\U000103BA','𐎼','𐎴','𐎫']]
    ASyll = ['\U000103AD','\U000103B6','\U000103A3','\U000103A5','\U000103A9','\U000103BA','𐎼','𐎴','𐎫']

    SylAlpha = '([𐎧𐎨𐏂𐎰𐎱𐎳𐎲𐎹𐎾𐎿𐏀𐏁𐏃])'

    ListC = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'OldPersian')) + ')'

    if not reverse:
        #print(Strng)
        Strng = Strng.replace(" ","\U000103D0").replace("_","").replace("<","")
        for x,y in zip(ICons+UCons+ACons,ISyll+USyll+ASyll):
            Strng = Strng.replace(x,y)
        #print(Strng)
    else:
        Strng = re.sub('𐎻(?!\U000103A1)', '𐎻\U000103A1', Strng)

        for x,y in zip(ICons_+UCons_,ISyll+USyll):
            Strng = Strng.replace(y,x)

        Strng = re.sub(SylAlpha + '(𐎠𐎡)', r'\1<\2', Strng)
        Strng = re.sub(SylAlpha + '(𐎠𐎢)', r'\1<\2', Strng)

        Strng = re.sub(ListC + '\U000103A0', r'\1' + '_\U000103A0', Strng)
        Strng = re.sub(SylAlpha + '([\U000103A1\U000103A2])', r'\1_\2', Strng)

        Strng = re.sub('([' + "".join(ASyll) + '])' + '([\U000103A1\U000103A2])', r'\1' + '<' + '\U000103A0' + r'\2' , Strng)

        Strng = Strng.replace('𐏐',' ')



    if not reverse:
        # Replace Space with Word Sperator
        # Remove _ - (why :-/ )
        pass
        #Strng = Strng.replace(" ","\U000103D0").replace("_","").replace("<","")
    else:
        pass
        #Strng = re.sub('([\U000103AD\U000103B6\U000103A3\U000103A5\U000103A9\U000103BA])_\U000103A0(?![𐎡𐎢])',r"\1",Strng)


    ## Fix dai Vs tai

    return Strng

def OldPersianNumeral(Strng,reverse=False):
    One = '\U000103D1'
    Two = '\U000103D2'
    Ten = '\U000103D3'
    Twenty = '\U000103D4'
    Hundred = '\U000103D5'

    Numbers = sorted(map(int,re.findall("\d+", Strng)),reverse=True)

    if not reverse:
        for num in Numbers:
            hN = int(num / 100)
            tW = int((num - (hN*100)) / 20)
            tN = int((num - (hN*100) - (tW*20)) /10)
            t2 = int((num - (hN*100) - (tW*20) - (tN*10)) /2)
            n1 = int(num - (hN*100) - (tW*20) - (tN*10) - (t2*2))

            perNum = (Hundred*hN) + (Twenty*tW) + (Ten*tN) + (Two*t2) + (One*n1)

            Strng = Strng.replace(str(num),perNum)
    else:
        Strng = Strng.replace(One, '1#')
        Strng = Strng.replace(Two, '2#')
        Strng = Strng.replace(Ten, '10#')
        Strng = Strng.replace(Twenty, '20#')
        Strng = Strng.replace(Hundred, '100#')

    return Strng
