from dahuffman import HuffmanCodec
import os
import sys
import pandas
from timeit import default_timer as timer
import brotlicffi


# Read Suffix File To List
suffixFile = open("Suffix.txt",'r')
suffixStrings = suffixFile.read()
suffixList = suffixStrings[0:-1].split("\n")
suffixFile.close()

# Read Common File To List
commonStringsFile = open("commons.txt","r")
commonStrings = commonStringsFile.read()
commonList = commonStrings[0:-1].split("\n")
commonStringsFile.close()

# Load Huffman Codec
codec = HuffmanCodec.load('codec')


# Initialise Prefix Strings
prefixStrings = ['https://','http://','www.']

# Initialise Common Word Replacement Chars
commonWordReplacements = ['١','٠','٭','٪','ى','٣','؁','و','ه','˘','˔','˛','ʿ','ʾ','ʱ']


def StripHeaders(URL):
    """
    Remove the prefix and suffix from URL strings
    :param 1:  URL string
    :return 1: URL string without prefix and suffix
    :return 2: Integer representing header byte
    """

    headURL = URL
    headerInt = 0

    for prefix in prefixStrings:
        if headURL.startswith(prefix):
            headerInt += pow(2,(6-prefixStrings.index(prefix)))
            headURL = headURL[len(prefix):]

    for suffix in suffixList:
        if suffix in headURL[len(headURL) - len(suffix):]:
            headerInt += pow(2,len(suffixList) - (suffixList.index(suffix) + 1))
            headURL = headURL[0:len(headURL) - len(suffix)]
            break

    return headURL,headerInt


def ReplaceCommonStrings(URL):
    """
    Replace common strings in URL strings with characters
    :param:  URL string
    :return: URL string with common strings replaced
    """
    for word in range(len(commonList)):
        if commonList[word] in URL:
            URL = URL.replace(commonList[word],commonWordReplacements[word])
    return URL


def GenerateBinaryHeader(headerInt):
    """
    Generates byte object for URL header 
    :param:  Integer representation of header
    :return: Byte object for URL header 
    """
    header = bin(headerInt).replace("0b",'')
    header = header.rjust(8,'0')
    binaryHeader = (str(header))
    binaryHeader = int(binaryHeader[::-1],2).to_bytes(1,'little')
    return binaryHeader


def Compress(URL):
    """
    Compress a URL using hybrid approach
    :param:  URL string
    :return: Compressed URL as byte object
    """

    urlReplacedWords,headerInt = StripHeaders(URL)
    urlReplacedWords = ReplaceCommonStrings(urlReplacedWords)
    if len(urlReplacedWords) < 150:
        try:
            compressed = codec.encode(urlReplacedWords)
            headerInt += 128
        except:
            compressed = brotlicffi.compress(urlReplacedWords.encode('utf8'),quality=6)
            headerInt += 0
    else:
        compressed = brotlicffi.compress(urlReplacedWords.encode('utf8'),quality=6)
        headerInt += 0

    headerBin = GenerateBinaryHeader(headerInt)
    compressedURL =  headerBin + compressed
    return compressedURL
    

def Decompress(URL):
    """
    Decompress a compressed URL
    :param:  Byte object compressed URL
    :return: Decompressed URL as string
    """
    preamble = ''
    postamble = ''
    header = URL[0:1]
    header = format(int.from_bytes(header,'little'),'023b')[::-1][0:8]


    if list(header)[0] == '1':
        decomp = codec.decode(URL[1:])
    else:
        decomp = brotlicffi.decompress(URL[1:]).decode('utf8')

    for x in range(len(prefixStrings)):
        if list(header)[x + 1] == '1':
            preamble += prefixStrings[x]

    for y in range(len(suffixList)):
        if list(header)[len(prefixStrings) + 1 + y] == '1':
            postamble += suffixList[y]

    for char in commonWordReplacements:
        if char in decomp:
            decomp = decomp.replace(char,commonList[commonWordReplacements.index(char)])
    return (preamble + decomp + postamble)


total_size_before = 0
total_size_after = 0

URLs = pandas.read_csv(sys.argv[1],sep = '\t',header = None)
URLs = URLs[0].values.tolist()
start = timer()
for URL in URLs:
    total_size_before += len(URL.encode('utf-8'))
    comp = Compress(URL)
    total_size_after += len(comp)

print("Compressed to:",((total_size_after+os.path.getsize('codec')+ os.path.getsize('commons.txt') + os.path.getsize('suffix.txt'))/total_size_before)*100,"%")
print("Size before compression: " + str(total_size_before) + " bytes")
print("Size after compression : " + str(total_size_after) + " bytes")
print("Compressed in: ", timer() - start, " Seconds")
