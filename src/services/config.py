"""_summary_
    配置文件交互
"""
import json
from utils.helper import *

def cfg_path(name:str = "user"):
    return f"configs/{name}.json"

jval_t = Union[dict,list,str,int,float,bool,None]
jkey_t = Union[str,int]

@singleton
@dataclass
class Config:
    __slots__ = ["pth","cfg"]
    def __init__(self, path:str) -> None:
        self.cfg:dict   = {}
        self.pth:str    = ""
        self.load(path)
    
    def load(self,path=None)->None: # cfg:dict <- json 将文件中的内容加载到实例中
        if path is None:
            path=self.pth
        with open(path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f) # 注意：cfg的id变了
            self.pth = path # 注意：会更新pth路径
    
    def save(self,path=None)->None: # json <- cfg:dict 将实例中的更改保存到文件中
        if path is None:
            path=self.pth
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, indent=4, ensure_ascii=False)
            self.pth = path # 注意：会更新pth路径
    
    # def unsafe_get(self,*keys)->jval_t: # 通过keys找到值 这个值是引用 更改会同步到self.cfg里面
    #     cur=self.cfg                    # 注意：如果你把返回值复制给了一个变量并对它改来改去 (t=self.get('key1','key2); t['key3']=...)
    #     for key in keys:                #      t和cfg是同步改变的，我们也默认二者同步
    #         cur = cur[key]              #      但如果你调用了load()，t和cfg会失去同步(cfg指向了新的对象)
    #     return cur                      #      因此，save()随便用，load()慎用
    
    def get(self,*keys)-> Callable: 
        # 不再返回值,而是返回获得这个值的方法,这样你就可以随意save && load了
        # t = self.get(...)时，无论你save还是load，t和t()与self.cfg都是同步的
        # (除非你: x = get(...)();此时在load后x不再同步)
        def fetcher()->jval_t:
            cur=self.cfg
            for key in keys:
                cur = cur[key]
            return cur
        return fetcher

    def keys(self,*keys)->tuple[jkey_t]: # 通过keys找到值 返回这个值的所有key
        cur = self.get(*keys)()
        if type(cur) == dict:
            return tuple(cur.keys())
        elif type(cur) == list:
            return tuple(range(len(cur)))
        else:
            return ()
    
    def is_sync(self)->bool: # cfg:dict == json 检查pth对应的json对象和cfg是否一致
        with open(self.pth, "r", encoding="utf-8") as f:
            fcfg = json.load(f)
        return fcfg == self.cfg

config=Config(cfg_path())

if __name__ == "__main__":
    # 单例检查
    # con=Config(file_path)
    # c2=Config(file_path)
    # print(con==c2 , con is c2 , len({con:1,c2:1}))
    
    t=config.get('presets','WHITE')
    print(config.is_sync())
    breakpoint()
