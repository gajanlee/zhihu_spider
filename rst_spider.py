from collections import namedtuple

import requests
from bs4 import BeautifulSoup

# RST 数据集的目录
BASE_URL = "http://ixa2.si.ehu.es/rst/fitxategiak_multiling.php"
# 当前url位置
domain = BASE_URL[:BASE_URL.rfind('/')+1]

class RstNode:
    def __init__(self):
        self.children = set()
        
    def update_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    def update_children(self, child):
        self.children.add(child)
        
    def is_valid(self):
        return hasattr(self, "node_id")
    
    def is_useful(self):
        return hasattr(self, "text") and self.text
        
    def __repr__(self):
        attr_str = []
        for attr in filter(lambda x: not x.startswith("__"), dir(self)):
            if any([isinstance(getattr(self, attr), dtype) for dtype in [int, float, str]]):
                attr_str.append("%s: %s"%(attr, getattr(self, attr)))
        return '\t'.join(attr_str)
    
class RSTree:
    def __init__(self, url, rstml):
        self.url = url
        self.rstml = rstml
        self.construct_Tree(rstml.find_all("segment"), rstml.find_all("group"))
    
    """
    数据存在的问题：
        有些标号没有，如http://ixa2.si.ehu.es/rst/diskurtsoa_rs3/TERM19_A1.rs3没有id=26的情况
    """
    def construct_Tree(self, segments, groups):
        print(self.url)
        
        nodes = [RstNode() for _ in range(100)]
        for node in segments+groups:
            node_id = int(node["id"])-1
            if node_id >= len(nodes): nodes += [RstNode() for _ in range(100)] # 扩容

            if "parent" not in node: self.root = nodes[node_id]
            nodes[node_id].update_attr(node_id=node_id, 
                                 parent=int(node.get("parent", node_id+1))-1, 
                                 rel_name=node.get("relname", "root"),
                                 text=node.text.strip())
            
            nodes[nodes[node_id].parent].update_children(node_id)
        self.nodes = nodes
        
    @property
    def passage(self):
        return '\n'.join([node.text for node in self.nodes if node.is_useful()])
    
    def __repr__(self):
        return "%s\n%s\n\n" % (self.url, self.passage)

def get_trees():
    data_table = BeautifulSoup(requests.get(BASE_URL).text).find(name="table")

    Resource = namedtuple("Resource", ["name", "rs3_link"])
    resourceList = [Resource(name=tr.find_all("td")[1].a.text, 
                            rs3_link=tr.find_all("td")[4].a["href"],)
                for tr in data_table.find_all("tr")[1:-1]]
    A1_list = filter(lambda r: r.name.endswith('_A1.rs3'), resourceList)

    build_tree = lambda url: RSTree(url, BeautifulSoup(requests.get(url).text).rst)
    RSTrees = map(build_tree, [domain+a1.rs3_link for a1 in A1_list])

    return RSTrees

def main():
    get_trees()

if __name__ == "__main__":
    main()
