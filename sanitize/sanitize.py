import re
import nltk

debug = False
list = ''

class PPISanitize:
    def __init__(self):
        self.ppi_patterns = [
            {'token': 'NAME@EMAIL.COM', 'desc': 'email address', 'regexp': re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')},
            {'token': 'UKPOSTCODE', 'desc': 'uk postcode', 'regexp': re.compile('(gir ?0aa|GIR ?0AA|[a-pr-uwyzA-PR-UWYZ]([0-9]{1,2}|([a-hk-yA-HK-Y][0-9]([0-9abehmnprv-yABEHMNPRV-Y])?)|[0-9][a-hjkps-uwA-HJKPS-UW]) ?[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2})')},
            {'token': 'CARDNUM', 'desc': 'BCGlobal', 'regexp': re.compile('(6541|6556)[0-9]{12}')},
            {'token': 'CARDNUM', 'desc': 'Carte Blanche Card', 'regexp': re.compile('389[0-9]{11}')},
            # {'token': 'CARDNUM', 'desc': 'Mastercard', '5[1-5][0-9]{14}'},
            # {'token': 'CARDNUM', 'desc': 'JCB Card', '(?:2131|1800|35\d{3})\d{11}'},
            {'token': 'CARDNUM', 'desc': 'JCB Card', 'regexp': re.compile('(3[0-9]{18})|(3[0-9]{15})|((2131|1800)[0-9]{11})')},
            {'token': 'CARDNUM', 'desc': 'Insta Payment Card', 'regexp': re.compile('63[7-9][0-9]{13}')},
            # Amex numbers look like US phone numbers
            {'token': 'CARDNUM', 'desc': 'Amex', 'regexp': re.compile('3[47][0-9]{13}')},
            {'token': 'CARDNUM', 'desc': 'Mastercard', 'regexp': re.compile('(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})')},
            {'token': 'CARDNUM', 'desc': 'Diners Club Card', 'regexp': re.compile('3(?:0[0-5]|[68][0-9])[0-9]{11}')},
            {'token': 'CARDNUM', 'desc': 'Discover Card', 'regexp': re.compile('65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})')},
            {'token': 'CARDNUM', 'desc': 'KoreanLocalCard', 'regexp': re.compile('9[0-9]{15}')},
            {'token': 'CARDNUM', 'desc': 'Laser Card', 'regexp': re.compile('(6304|6706|6709|6771)[0-9]{12,15}')},
            {'token': 'CARDNUM', 'desc': 'Maestro Card', 'regexp': re.compile('(5018|5020|5038|5612|5893|6304|6759|6761|6762|6763|0604|6390)[0-9]{8,15}')},
            {'token': 'CARDNUM', 'desc': 'Solo Card', 'regexp': re.compile('(6334|6767)[0-9]{12}|(6334|6767)[0-9]{14}|(6334|6767)[0-9]{15}')},
            {'token': 'CARDNUM', 'desc': 'Switch Card', 'regexp': re.compile('(4903|4905|4911|4936|6333|6759)[0-9]{12}|(4903|4905|4911|4936|6333|6759)[0-9]{14}|(4903|4905|4911|4936|6333|6759)[0-9]{15}|564182[0-9]{10}|564182[0-9]{12}|564182[0-9]{13}|633110[0-9]{10}|633110[0-9]{12}|633110[0-9]{13}')},
            {'token': 'CARDNUM', 'desc': 'Union Pay Card', 'regexp': re.compile('(62[0-9]{14,17})')},
            {'token': 'CARDNUM', 'desc': 'Visa Card', 'regexp': re.compile('4[0-9]{12}(?:[0-9]{3})?')},
            {'token': 'CARDNUM', 'desc': 'Visa Master Card', 'regexp': re.compile('(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})')},
            {'token': 'POSTCODECA', 'desc': 'Canada postcode', 'regexp': re.compile('[abceghj-nprstvxyABCEGHJ-NPRSTVXY]{1}[0-9]{1}[abceghj-nprstv-zABCEGHJ-NPRSTV-Z]{1}[ ]?[0-9]{1}[abceghj-nprstv-zABCEGHJ-NPRSTV-Z]{1}[0-9]{1}')},
            ### after all the more specific matches
            
            # Problem with chomping leading and training space
            {'token': 'UKPHONE', 'desc': 'uk phone', 'regexp': re.compile('(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?')},
            {'token': ' USPHONE ', 'desc': 'US phone', 'regexp': re.compile('(1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?)')},
            {'token': 'USPHONE', 'desc': 'US phone', 'regexp': re.compile('(\s|^)(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?(\s|$)')},
            {'token': 'SSN', 'desc': 'ssn', 'regexp': re.compile('(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}')},
            {'token': 'ZIPCODEUS' , 'desc': 'zip code', 'regexp': re.compile('[0-9]{5}(-[0-9]{4})?')},
            {'token': 'ACCOUNTNO', 'desc': 'account number', 'regexp': re.compile('\d{5-12')}
        ]

SANITIZER = PPISanitize()

def tokenize(doc):
    tokenized_doc = nltk.word_tokenize(doc)
    tagged_sentences = nltk.pos_tag(tokenized_doc)
    ne_chunked_sents = nltk.ne_chunk(tagged_sentences)
    named_entities = []
    for tagged_tree in ne_chunked_sents:
        if hasattr(tagged_tree, 'label'):
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #
            entity_type = tagged_tree.label() # get NE category
            named_entities.append((entity_name, entity_type))
            doc = doc.replace(entity_name, entity_type)
    if debug:
        print(named_entities)
        print('%-20s "%s"' % ('NER', doc))
    return doc


def regexReplace( str, token, desc, regex):
    global list
    list  = list + ', ' + desc
    clean_str = re.sub(regex, token, str, re.I)
    if (debug):
        if (str != clean_str):
            print('%-20s "%s"' % (desc, clean_str))
    return clean_str


def replacePPI(str):
    global SANITIZER
    for pattern in SANITIZER.ppi_patterns:
        str = regexReplace(str, pattern['token'], pattern['desc'], pattern['regexp'])
    return str
    
def getSubstituteText(key, type):
    return ""