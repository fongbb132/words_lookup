import urllib2
import xml.etree.ElementTree as ET
import re
import constants
file = open('sample.txt', 'w')

def fwrite(message):
    file.write(message+" " )

def output(word):
    global key 
    requeset_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=%s'%(word, constants.key) 
    respond = urllib2.urlopen(requeset_url).read()
    try: 
        root = ET.fromstring(respond)
    except:
        print word 
        return
    root = root.find('entry')
    if root is None:
        print word
        return 
    partOfSpeechs  = root.findall('fl')
    sx = []
    fwrite( root.find('ew').text.strip())
    for partOfSpeech in partOfSpeechs:
        fwrite('[{0}] '.format(partOfSpeech.text))
    fwrite("\n\tdef: ") 
    for definition in root.find('def').findall('dt'):
        d = re.sub(r'^\s+|\s*:\s*|\s+$', '', definition.text).strip()
        if  d : 
            fwrite(d +";")

        for s in definition.findall('sx'):
            if s.text.strip() is not None:
                sx.append(s.text.strip())
    if len(sx) > 0 : 
        fwrite("\n")
        fwrite("\tsynonyms: ") 
    for s in sx:
        fwrite(s.strip()+",")

words = [] 

with open('words.txt','r') as f:
    data = f.readlines()
    for line in data:
        words.append(line.strip())

for word in words:
    output(word)
    fwrite('\n\n')
file.close()
