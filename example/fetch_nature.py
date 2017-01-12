from pyliterature import Pyliterature

url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'
keyword = 'DFT'

liter = Pyliterature(url, keyword)
print(liter.text)
print('===================================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')