### pyliterature
A Python web wrapper and text mining package for the scientific journal, including Nature, Science, ScienceDirect, Wiley, ACS publication, RSC publication and so on.



### Author
* Xing Wang  <xingwang1991@gmail.com>



### Dependencies

* Python >=27
* spynner
* beautifulsoup4
* nltk



#### Examples
y
```python
>>> from pyliterature import Pyliterature
>>> url = 'http://www.nature.com/nature/journal/v541/n7635/full/nature20782.html'
>>> keyword = 'DFT'
>>> liter = Pyliterature(url, keyword)
>>> liter.parser()
>>> liter.texty
>>> for sent in liter.keysents:
...    print(sent)
```

If you want to add features/improvement or report issues, feel free to send a pull request!


### TODO
* read bib list
* determine sentence from which article

