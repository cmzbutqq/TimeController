"""_summary_
    配置文件交互
"""
import json
from helper import *

file_path="config/user.json"

jval_t = Union[dict,list,str,int,float,bool,None]
jkey_t = Union[str,int]
@singleton
@dataclass
class Config:
    __slots__ = ["pth","cfg"]
    cfg:dict
    pth:str
    def __init__(self, path:str) -> None:
        self.cfg = {}
        self.pth = ""
        self.load(path)
        
    def load(self,path:str)->None: # json -> cfg:dict 将文件中的内容加载到实例中
        with open(path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
            self.pth = path
    
    def save(self,path:str)->None: # cfg:dict -> json 将实例中的更改保存到文件中
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, indent=4, ensure_ascii=False)
            self.pth = path
    
    def get(self,*keys)->jval_t: # 通过keys找到值 这个值你可以直接使用和更改 更改会同步到这个class的实例
        cur=self.cfg
        for key in keys:
            cur = cur[key]
        return cur
    
    def keys(self,*keys)->tuple[jkey_t]: # 通过keys找到值 返回这个值的所有key
        cur = self.get(*keys)
        if type(cur) == dict:
            return tuple(cur.keys())
        elif type(cur) == list:
            return tuple(range(len(cur)))
        else:
            return []

if __name__ == "__main__":
    c1=Config(file_path)
    c2=Config(file_path)
    # dprint(c1,c2)
    print(c1==c2 , c1 is c2 , len({c1:1,c2:1}))