from pyliterature import Pyliterature

urls = [
    'http://science.sciencemag.org/content/355/6320/49.full', 
    'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html', 
    'http://www.sciencedirect.com/science/article/pii/S1751616116301138', 
    'http://pubs.acs.org/doi/full/10.1021/acscatal.6b02960', 
]

keyword = 'DFT'
liter = Pyliterature()
for url in urls:
    print(url + '\n\n')
    liter.url = url
    liter.parser()
#
liter.url = None
liter.keyword = keyword
# print(liter.text)
liter.parser()
print('===================================================')
for keysent in liter.keysents:
    print(keysent)
    print('\n')