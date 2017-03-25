import requests
import re
from bs4 import BeautifulSoup

p = re.compile(r'^http')
hrefs = []
href_log = []
num = 0

def req(url): # на случай если произойдет разрыв сети или иной сбой подключения
    try:
        html = requests.get(url).text
        return html
    except (socket.gaierror, requests.exceptions.ConnectionError):
        req(url)

def rel_orient(href): # преобразование относительных ссылок в жесткие
    if not p.search(href):
        href_ = href.split('/')
        #print(href)
        if href_[0] == '.':
            href = '%s/%s' % ('/'.join(url_[:-1]), '/'.join(href_[1:]))
        elif href_[0] == '..':
            href = '%s/%s' % ('/'.join(url_[:-2]), '/'.join(href_[1:]))
        elif href_[0] == '':
            href = '%s/%s' % ('/'.join(SITE_[:3]), '/'.join(href_[1:]))
        else:
            if '.' in url_[-1]:
                href = '%s/%s' % ('/'.join(url_[:-1]), '/'.join(href_))
            else:
                href = '%s/%s' % ('/'.join(url_), '/'.join(href_))
    return href

def find(url): # нахождение всех ссылок на странице
    global href_log, url_
    hrefs = []
    if url[-1] == '/':
        url = url[:-1]
    url_ = url.split('/')
    html = req(url)
    soup = BeautifulSoup(html, 'html.parser')
    elems = soup.find_all('a')
    for elem in elems:
        href = elem.get('href')
        if href:
            if '#' in href:
                href = href[:href.index('#')]
            href = rel_orient(href)
            if href not in href_log:
                href_log += [href]
                hrefs += [href]
    return hrefs     

def insert(tree, Childs):
        tree.pop(-1)
        for child in Childs:
            tree.insert(len(tree), [child, []])

def expand_(tree, graph, SITE):
    global num
    if tree:
        if graph:
            print('<%s> %s' % (num, root(tree)))
        num += 1
        for subtree in subtrees(tree):
            insert(tree, find(root(tree)))
        for subtree in subtrees(tree):
            if root(subtree):
                if '.' in SITE_[-1]:
                    if '.'.join(SITE.split('.')[:-1]) in root(subtree):
                        expand_(subtree, graph, SITE)
                else:
                    if SITE in root(subtree):
                        expand_(subtree, graph, SITE)

def preorder_(tree):
    global num
    if tree:
        print(root(tree))
        num += 1
        for subtree in subtrees(tree):
            preorder_(subtree)
            
def root(tree):
    return tree[0]
def subtrees(tree):
    return tree[1:]
              
class Tree:
    def __init__(self, SITE):
        if SITE[-1] == '/':
            SITE = SITE[:-1]
        self.Tree = [SITE, []]
        self.SITE = SITE
    def expand(self, graph = True):
        global SITE_
        SITE_ = self.SITE.split('/')
        num = 0
        expand_(self.Tree, graph, self.SITE)
    def preorder(self):
        num = 0
        preorder_(self.Tree)
