from pyliterature import Pyliterature


# read url from bib file
urls = []
file = open('example.bib')
lines = file.readlines()
for line in lines:
    if 'url' in line:
        url = line.split('=')[1].split('{')[1].split('}')[0]
        urls.append(url)

#----------------------------------------
# read old database file
keyword = 'catalytic'
liter = Pyliterature()
liter.read_database(keyword)
# find new url not in the database
urls_new = []
for url in urls:
    if url not in liter.url_list:
        urls_new.append(url)

#-----------------------------------
# load text from new url html
for url in urls_new:
    liter.url = url
    print(url + '\n\n')
    liter.parser()

# parse keysnets from text
liter.url = None
liter.keyword = keyword
print(liter.text)
liter.parser()
liter.save_database()
print('===================================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')
