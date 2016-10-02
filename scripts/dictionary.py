import re
#import enchant
from sys import stderr

badchars_pattern = re.compile("[^a-zA-Z\s]")

wiki_match_badchars = re.compile("[^A-Za-z0-9_\,\.\(\)\-\s]")
wiki_sub_remove = re.compile("[\"\(\)\,:]")
wiki_sub_replace = re.compile("[\-_/]")
#enchant_dict_us = enchant.Dict('en_US')
#enchant_dict_gb = enchant.Dict('en_GB') 


def build_custom_dict() :
        science_dict = set()
        path = '/home/evly/tmt/'
        # wikipedia titles contain all kinds of weird characters
        # at the beginning and end of lines, filter these ones out...
        for wordlist in (path+'custom_scientific_US_ascii.txt', path+'custom_scientific_UK_ascii.txt', path+'wiktionary_english_only.txt') :
            with open(wordlist) as f :
                for line in f :
                    line = line.strip()

                    if line[0] in ".(!&'*+-/0123456789@?=;\"" :
                        continue

                    line = wiki_sub_remove.sub('', line)
                    line = wiki_sub_replace.sub(' ', line)

                    for i in line.strip().split() :
                        if i.upper() == i :
                            continue

                        if not badchars_pattern.search(i) :
                            science_dict.add(i.lower())

            print >> stderr, "added %s, %d words in dict" % (wordlist, len(science_dict))

        return science_dict


with open('/home/evly/tmt/english.txt', 'w') as words :
    words.write(str('\n'.join(build_custom_dict())))
words.closed
