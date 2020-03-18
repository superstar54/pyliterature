from pyliterature import Pyliterature

url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'
keyword = 'DFT'


liter = Pyliterature(url, keyword)
# load text from url html and parse the sentences including keyword
liter.parser()

print('=================article text==================================')
# print(liter.text)

print('=================key sentences==================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')
