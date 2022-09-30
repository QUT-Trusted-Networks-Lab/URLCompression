from dahuffman import HuffmanCodec
import pandas
import sys
import spacy
from timeit import default_timer as timer

prefixStrings = ['https://','http://','www.']

common_word_replace = ['١','٠','٭','٪','ى','٣','؁','و','ه','˘','˔','˛','ʿ','ʾ','ʱ']



def findSuffix(URLs):
    """
    Finds most common suffix strings in list

    :param: List of URLs
    :return: List of 4 most common suffix from URL
    """
    error = 0
    suffix_dict = {}
    for URL in URLs:
        try:
            if URL[URL.rindex('.'):] in suffix_dict:
                suffix_dict[URL[URL.rindex('.'):]] += 1
            else:
                suffix_dict[URL[URL.rindex('.'):]] = 1
        except:
            error += 1
    print(list(dict(sorted(suffix_dict.items(), key=lambda item: item[1])[-10:]).keys()))
    print(list(dict(sorted(suffix_dict.items(), key=lambda item: item[1])[-10:]).values()))
    return(list(dict(sorted(suffix_dict.items(), key=lambda item: item[1])[-4:]).keys()))

def stripHeaderStrings(URL,suffixsStrings):
    """
    removes the prefix and suffix from URL strings

    :param 1: String URL
    :param 2: List of Suffix strings
    :return: URL without prefix or suffix strings
    """
    head_url = URL
    if len(prefixStrings) + len(suffixsStrings) > 7:
        return("Error Too Many Strings for Storage in Header")

    for prefix in prefixStrings:
        if prefix in head_url[0:len(prefix)]:
            head_url = head_url[len(prefix):]

    for suffix in suffixsStrings:
        if suffix in head_url[len(head_url) - len(suffix):]:
            head_url = head_url[0:len(head_url) - len(suffix)]

    return head_url

def findCommonWords(URL):
    token_dict = {}
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(URL[0:20000], disable= ['ner','parser'])
    for token in doc:
        if len(token.text) > 2:
            if str(token.text) in token_dict:
                token_dict[str(token.text)] += 1
            else:
                token_dict[str(token.text)] = 1

    common_list = list(dict(sorted(token_dict.items(), key=lambda item: item[1])[-(len(common_word_replace)):]).keys())
    return(common_list)

def replaceCommonWords(URL,common_words):
    for x in range(len(common_words)):
        if common_words[x] in URL:
            URL = URL.replace(common_words[x],common_word_replace[x])
    return URL



URLs = pandas.read_csv(sys.argv[1],sep = '\t',header = None)
URLs = URLs[0].values.tolist()



suffixString = findSuffix(URLs)
f = open("suffix.txt","w")
for item in suffixString:
    f.writelines([item+'\n'])
f.close()



URL_list = []
URL_list_for_common = []


for URL in URLs:
    URL = stripHeaderStrings(URL,suffixString)
    URL_list.append(URL)
    URL_list_for_common.append(URL.replace('/',' ').replace('.',' ').replace('-',' '))

common_list = findCommonWords(''.join(URL_list_for_common))

f = open("commons.txt","w")
for item in common_list:
    f.writelines([item+'\n'])
f.close()


new_list = []
for URL in URL_list:
    new_list.append(replaceCommonWords(URL,common_list))


codec = HuffmanCodec.from_data(''.join(new_list))
codec.save("codec")