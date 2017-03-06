import requests, re
from bs4 import BeautifulSoup

hrefs = []
href_log = []
p = re.compile(r'^http')
num = 0

def find(url, SITE):
    global href_log
    hrefs = []
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        elems = soup.find_all('a')
        for elem in elems:
            href = elem.get('href')
            if href:
                if not p.search(href):
                    href = SITE + href
                if href not in href_log:
                    href_log += [href]
                    hrefs += [href]
    except:
        pass
    return hrefs        

def insert(tree, Childs):
        tree.pop(-1)
        for i in Childs:
            tree.insert(len(tree), [i, []])

def expand_(tree, graph, SITE):
    global num
    if tree:
        if graph:
            print('<%s> %s' % (num, tree[0]))
        num += 1
        for i in tree[1:]:
            insert(tree, find(tree[0], SITE))
        for i in tree[1:]:
            expand_(i, graph, SITE)

def preorder_(tree):
    global num
    if tree:
        print(tree[0])
        num += 1
        for i in tree[1:]:
            preorder_(i) 
              
class Tree:
    def __init__(self, SITE):
        self.Tree = [SITE, []]
        if SITE[-1] == '/':
            SITE = SITE[:-1]
        self.SITE = SITE
    def expand(self, graph = True):
        num = 0
        expand_(self.Tree, graph, self.SITE)
    def preorder(self):
        num = 0
        preorder_(self.Tree)
        
           

