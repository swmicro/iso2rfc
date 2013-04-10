#!/usr/bin/python
# -*- coding: utf-8 -*-

## This script converts UEFI *.UNI file with ISO-639 format to a new RFC-4646
#  Usage: iso2rfc -i <inputfile.uni> -o <outputfile.uni>
#
#  @author swmicro@gmail.com (Vyacheslav)
#  


import getopt, codecs, re, sys


iso2rfc_dic = {
    'eng':'en-US',
    'fra':'fr-FR',
    'spa':'es-ES',
    'ger':'de-DE',
    'rus':'ru-RU',
    'zho':'zh-chs',
    'chi':'zh-cht',
    'kor':'ko-KR',
    'jpn':'ja-JP',
    'ita':'it-IT',
    'dan':'da-DK',
    'fin':'fi-FI',
    'dut':'nl-NL',
    'nor':'nb-NO',
    'por':'pt-BR',
    'swe':'sv-FI',  
    'afk':'af-ZA',    # Afrikaans (South Africa)
    'sqi':'sq-AL',    # Albanian (Albania)
    'gsw':'gsw-FR',   # Alsatian (France)
    'amh':'am-ET',    # Amharic (Ethiopia)
    'arg':'ar-DZ',    # Arabic (Algeria)
    'arh':'ar-BH',    # Arabic (Bahrain)
    'are':'ar-EG',    # Arabic (Egypt)
    'ari':'ar-IQ',    # Arabic (Iraq)
    'arj':'ar-JO',    # Arabic (Jordan)
    'ark':'ar-KW',    # Arabic (Kuwait)
    'arb':'ar-LB',    # Arabic (Lebanon)
    'arl':'ar-LY',    # Arabic (Libya)
    'arm':'ar-MA',    # Arabic (Morocco)
    'aro':'ar-OM',    # Arabic (Oman)
    'arq':'ar-QA',    # Arabic (Qatar)
    'ara':'ar-SA',    # Arabic (Saudi Arabia)
    'ars':'ar-SY',    # Arabic (Syria)
    'art':'ar-TN',    # Arabic (Tunisia)
    'aru':'ar-AE',    # Arabic (U.A.E.)
    'ary':'ar-YE',    # Arabic (Yemen)
    'hye':'hy-AM',    # Armenian (Armenia)
    'asm':'as-IN',    # Assamese (India)
    'aze':'az-AZ',    # Azeri (Azerbaijan)
    'bas':'ba-RU',    # Bashkir (Russia)
    'euq':'eu-ES',    # Basque (Basque)
    'bel':'be-BY',    # Belarusian (Belarus)
    'bng':'bn-BD',    # Bengali (Bangladesh)
    'bsc':'bs-Cyrl-BA',    # Bosnian (Cyrillic, Bosnia and Herzegovina)
    'bsb':'bs-Latn-BA',    # Bosnian (Latin, Bosnia and Herzegovina)
    'bre':'br-FR',    # Breton (France)
    'bgr':'bg-BG',    # Bulgarian (Bulgaria)
    'cat':'ca-ES',    # Catalan (Catalan)
    'zhh':'zh-HK',    # Chinese (Hong Kong S.A.R.)
    'zhm':'zh-MO',    # Chinese (Macao S.A.R.)
    'chs':'zh-CN',    # Chinese (People's Republic of China)
    'zhi':'zh-SG',    # Chinese (Singapore)
    'cht':'zh-TW',    # Chinese (Taiwan)
    'cos':'co-FR',    # Corsican (France)
    'hrv':'hr-HR',    # Croatian (Croatia)
    'hrb':'hr-BA',    # Croatian (Latin, Bosnia and Herzegovina)
    'csy':'cs-CZ',    # Czech (Czech Republic)
#    'dan':'da-DK',    # Danish (Denmark)
    'prs':'prs-AF',   # Dari (Afghanistan)
    'div':'div-MV',   # Divehi (Maldives)
    'nlb':'nl-BE',    # Dutch (Belgium)
    'nld':'nl-NL',    # Dutch (Netherlands)
    'ena':'en-AU',    # English (Australia)
    'enl':'en-BZ',    # English (Belize)
    'enc':'en-CA',    # English (Canada)
    'enb':'en-029',   # English (Caribbean)
    'enn':'en-IN',    # English (India)
    'eni':'en-IE',    # English (Ireland)
    'enj':'en-JM',    # English (Jamaica)
    'enm':'en-MY',    # English (Malaysia)
    'enz':'en-NZ',    # English (New Zealand)
    'enp':'en-PH',    # English (Republic of the Philippines)
    'ene':'en-SG',    # English (Singapore)
    'ens':'en-ZA',    # English (South Africa)
    'ent':'en-TT',    # English (Trinidad and Tobago)
#    'eng':'en-GB',    # English (United Kingdom)
    'enu':'en-US',    # English (United States)
    'enw':'en-ZW',    # English (Zimbabwe)
    'eti':'et-EE',    # Estonian (Estonia)
    'fos':'fo-FO',    # Faroese (Faroe Islands)
    'fpo':'fil-PH',   # Filipino (Philippines)
#    'fin':'fi-FI',    # Finnish (Finland)
    'frb':'fr-BE',    # French (Belgium)
    'frc':'fr-CA',    # French (Canada)
#    'fra':'fr-FR',    # French (France)
    'frl':'fr-LU',    # French (Luxembourg)
    'frm':'fr-MC',    # French (Principality of Monaco)
    'frs':'fr-CH',    # French (Switzerland)
    'fyn':'fy-NL',    # Frisian (Netherlands)
    'glc':'gl-ES',    # Galician (Galician)
    'kat':'ka-GE',    # Georgian (Georgia)
    'dea':'de-AT',    # German (Austria)
    'deu':'de-DE',    # German (Germany)
    'dec':'de-LI',    # German (Liechtenstein)
    'del':'de-LU',    # German (Luxembourg)
    'des':'de-CH',    # German (Switzerland)
    'ell':'el-GR',    # Greek (Greece)
    'kal':'kl-GL',    # Greenlandic (Greenland)
    'guj':'gu-IN',    # Gujarati (India)
    'hau':'ha-NG',    # Hausa (Nigeria)
    'heb':'he-IL',    # Hebrew (Israel)
    'hin':'hi-IN',    # Hindi (India)
    'hun':'hu-HU',    # Hungarian (Hungary)
    'isl':'is-IS',    # Icelandic (Iceland)
    'ibo':'ig-NG',    # Igbo (Nigeria)
    'ind':'id-ID',    # Indonesian (Indonesia)
    'iuk':'iu-Latn-CA',    # Inuktitut (Latin, Canada)
    'ius':'iu-Cans-CA',    # Inuktitut (Syllabics, Canada)
    'ire':'ga-IE',    # Irish (Ireland)
    'xho':'xh-ZA',    # isiXhosa (South Africa)
    'zul':'zu-ZA',    # isiZulu (South Africa)
#    'ita':'it-IT',    # Italian (Italy)
    'its':'it-CH',    # Italian (Switzerland)
#    'jpn':'ja-JP',    # Japanese (Japan)
    'kdi':'kn-IN',    # Kannada (India)
    'kkz':'kk-KZ',    # Kazakh (Kazakhstan)
    'khm':'km-KH',    # Khmer (Cambodia)
    'qut':'qut-GT',   # K'iche (Guatemala)
    'kin':'rw-RW',    # Kinyarwanda (Rwanda)
    'swk':'sw-KE',    # Kiswahili (Kenya)
    'knk':'kok-IN',   # Konkani (India)
#    'kor':'ko-KR',    # Korean (Korea)
    'kyr':'ky-KG',    # Kyrgyz (Kyrgyzstan)
    'lao':'lo-LA',    # Lao (Lao P.D.R.)
    'lvi':'lv-LV',    # Latvian (Latvia)
    'lth':'lt-LT',    # Lithuanian (Lithuania)
    'dsb':'wee-DE',   # Lower Sorbian (Germany)
    'lbx':'lb-LU',    # Luxembourgish (Luxembourg)
    'mki':'mk-MK',    # Macedonian (Former Yugoslav Republic of Macedonia)
    'msb':'ms-BN',    # Malay (Brunei Darussalam)
    'msl':'ms-MY',    # Malay (Malaysia)
    'mym':'ml-IN',    # Malayalam (India)
    'mlt':'mt-MT',    # Maltese (Malta)
    'mri':'mi-NZ',    # Maori (New Zealand)
    'mpd':'arn-CL',   # Mapudungun (Chile)
    'mar':'mr-IN',    # Marathi (India)
    'mwk':'moh-CA',   # Mohawk (Mohawk)
    'mon':'mn-MN',    # Mongolian (Cyrillic, Mongolia)
    'mng':'mn-Mong-CN',    # Mongolian (Traditional Mongolian, PRC)
    'nep':'ne-NP',    # Nepali (Nepal)
#    'nor':'nb-NO',    # Norwegian, Bokml (Norway)
    'non':'nn-NO',    # Norwegian, Nynorsk (Norway)
    'oci':'oc-FR',    # Occitan (France)
    'ori':'or-IN',    # Oriya (India)
    'pas':'ps-AF',    # Pashto (Afghanistan)
    'far':'fa-IR',    # Persian
    'plk':'pl-PL',    # Polish (Poland)
    'ptb':'pt-BR',    # Portuguese (Brazil)
    'ptg':'pt-PT',    # Portuguese (Portugal)
    'pan':'pa-IN',    # Punjabi (India)
    'qub':'quz-BO',   # Quechua (Bolivia)
    'que':'quz-EC',   # Quechua (Ecuador)
    'qup':'quz-PE',   # Quechua (Peru)
    'rom':'ro-RO',    # Romanian (Romania)
    'rmc':'rm-CH',    # Romansh (Switzerland)
#    'rus':'ru-RU',    # Russian (Russia)
    'smn':'smn-FI',   # Sami, Inari (Finland)
    'smj':'smj-NO',   # Sami, Lule (Norway)
    'smk':'smj-SE',   # Sami, Lule (Sweden)
    'smg':'se-FI',    # Sami, Northern (Finland)
    'sme':'se-NO',    # Sami, Northern (Norway)
    'smf':'se-SE',    # Sami, Northern (Sweden)
    'sms':'sms-FI',   # Sami, Skolt (Finland)
    'sma':'sma-NO',   # Sami, Southern (Norway)
    'smb':'sma-SE',   # Sami, Southern (Sweden)
    'san':'sa-IN',    # Sanskrit (India)
    'srn':'sr-Cyrl-BA',    # Serbian (Cyrillic, Bosnia and Herzegovina)
    'srb':'sr-Cyrl-SP',    # Serbian (Cyrillic, Serbia)
    'srs':'sr-Latn-BA',    # Serbian (Latin, Bosnia and Herzegovina)
    'srl':'sr-Latn-SP',    # Serbian (Latin, Serbia)
    'nso':'nso-ZA',   # Sesotho sa Leboa (South Africa)
    'tsn':'tn-ZA',    # Setswana (South Africa)
    'sin':'si-LK',    # Sinhala (Sri Lanka)
    'sky':'sk-SK',    # Slovak (Slovakia)
    'slv':'sl-SI',    # Slovenian (Slovenia)
    'ess':'es-AR',    # Spanish (Argentina)
    'esb':'es-BO',    # Spanish (Bolivia)
    'esl':'es-CL',    # Spanish (Chile)
    'eso':'es-CO',    # Spanish (Colombia)
    'esc':'es-CR',    # Spanish (Costa Rica)
    'esd':'es-DO',    # Spanish (Dominican Republic)
    'esf':'es-EC',    # Spanish (Ecuador)
    'ese':'es-SV',    # Spanish (El Salvador)
    'esg':'es-GT',    # Spanish (Guatemala)
    'esh':'es-HN',    # Spanish (Honduras)
    'esm':'es-MX',    # Spanish (Mexico)
    'esi':'es-NI',    # Spanish (Nicaragua)
    'esa':'es-PA',    # Spanish (Panama)
    'esz':'es-PY',    # Spanish (Paraguay)
    'esr':'es-PE',    # Spanish (Peru)
    'esu':'es-PR',    # Spanish (Puerto Rico)
    'esn':'es-ES',    # Spanish (Spain)
    'est':'es-US',    # Spanish (United States)
    'esy':'es-UY',    # Spanish (Uruguay)
    'esv':'es-VE',    # Spanish (Venezuela)
    'svf':'sv-FI',    # Swedish (Finland)
    'sve':'sv-SE',    # Swedish (Sweden)
    'syr':'syr-SY',   # Syriac (Syria)
    'taj':'tg-TJ',    # Tajik (Tajikistan)
    'tzm':'tzm-DZ',   # Tamazight (Algeria)
    'tam':'ta-IN',    # Tamil (India)
    'ttt':'tt-RU',    # Tatar (Russia)
    'tel':'te-IN',    # Telugu (India)
    'tha':'th-TH',    # Thai (Thailand)
    'bob':'bo-CN',    # Tibetan (PRC)
    'trk':'tr-TR',    # Turkish (Turkey)
    'tuk':'tk-TM',    # Turkmen (Turkmenistan)
    'uig':'ug-CN',    # Uighur (PRC)
    'ukr':'uk-UA',    # Ukrainian (Ukraine)
    'hsb':'wen-DE',   # Upper Sorbian (Germany)
    'urd':'ur-PK',    # Urdu (Islamic Republic of Pakistan)
    'uzb':'uz-UZ',    # Uzbek (Uzbekistan)
    'vit':'vi-VN',    # Vietnamese (Vietnam)
    'cym':'cy-GB',    # Welsh (United Kingdom)
    'wol':'wo-SN',    # Wolof (Senegal)
    'sah':'sah-RU',   # Yakut (Russia)
    'iii':'ii-CN',    # Yi (PRC)
    'yor':'yo-NG'     # Yoruba (Nigeria)
    }

def replace_words(text):
    rc = re.compile('|'.join(map(re.escape, iso2rfc_dic)))
    def translate(match):
        return iso2rfc_dic[match.group(0)]
    return rc.sub(translate, text)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    help_string = 'Usage: iso2rfc -i <inputfile.uni> -o <outputfile.uni>'
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:],"hi:o:",["ifile=","ofile="])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, help_string
        return 2

    for opt, arg in opts:
        if opt == '-h':
            print help_string
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    try:
        with codecs.open(inputfile, 'r', 'utf-16') as f:
            content_str = f.read()
            f.close()
    except IOError as e:
        print 'Error: input file does not exist'
        return

    o = codecs.open(outputfile, 'w', 'utf-16')
    pattern = r'(#string\s+\S+\s+#language\s+)(\S+)'
    for line in content_str.splitlines():
        str = re.search(pattern, line, re.IGNORECASE)
        if str:
            str = replace_words(str.group(2))
            line = re.sub(pattern, r'\1' + str, line, re.IGNORECASE)
        o.write(line + '\n')
    o.close()

if __name__ == "__main__":
    sys.exit(main())

