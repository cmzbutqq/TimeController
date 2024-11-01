from typing import Any, Optional, Callable, Union

def singleton(cls): # 类装饰器，给类加上单例模式    ！！必须放在其他类装饰器之上（之外） 因为他会把类退化成函数
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

from textwrap import shorten
def dataclass(cls): # 类装饰器，给类加上__repr__,__str__,__eq__,__hash__方法
    def __str__(self)->str:
        ret:str = f"class:{self.__class__.__name__}\t"
        if hasattr(self,"__slots__"):
            for attr in self.__slots__:
                ret += f"\t{attr} = "+ shorten(f"{getattr(self,attr)}",50)
        elif hasattr(self,"__dict__"):
            for k,v in self.__dict__.items():
                ret += f"\t{k} : "+ shorten(f"{v}",50)
        return ret
    cls.__str__ = __str__
    def __repr__(self)->str: 
        ret:str = f"class:{self.__class__.__name__}\t"
        if hasattr(self,"__slots__"):
            for attr in self.__slots__:
                ret += f"\t{attr} = "+ shorten(f"{getattr(self,attr)}",200)
        elif hasattr(self,"__dict__"):
            for k,v in self.__dict__.items():
                ret += f"\t{k} : "+ shorten(f"{v}",200)
        return ret
    cls.__repr__ = __repr__
    def __eq__(self,other)->bool:
        if hasattr(self,"__slots__"):
            return all(getattr(self,attr)==getattr(other,attr) for attr in self.__slots__)
        elif hasattr(self,"__dict__"):
            return self.__dict__ == other.__dict__
    cls.__eq__ = __eq__
    def __hash__(self)->int:
        if hasattr(self,"__slots__"):
            return hash([(attr,getattr(self,attr)) for attr in self.__slots__])
        elif hasattr(self,"__dict__"):
            return hash(self.__dict__)
    __hash__ = __hash__
    return cls

def noexception(func): # 装饰器，给函数加上try-except
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print(f"ERROR:{e}")
    return wrapper


import time
class timeit: # 计时器 计算with timeit():后面的代码块运行时间
    def __enter__(self):
        self.start = time.time()
        print(f"time start:{self.start}")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            print(f"ERROR:{exc_type}\t{exc_val}\t{exc_tb}")
        print(f"time cost:{time.time()-self.start}")
        
def timeme(func:Callable)->Callable: # 函数装饰器，给函数加上计时器
    def wrapper(*args,**kwargs):
        start=time.time()   
        ret = func(*args,**kwargs)
        print(f"{func.__name__}\tcost time:{time.time()-start}")
        return ret
    return wrapper

def dprint(*args): # 带类型和详细信息的打印
    for arg in args:
        print(f"> id:\t{id(arg)}\n> type:\t{type(arg)}\n> str:\t{arg}\n> repr:\t{repr(arg)}")

if __name__ == "__main__":
    @singleton
    @dataclass
    class A:
        __slots__ = ["a","b"]
        a:int
        b:str
        def __init__(self,a,b):
            self.a = a
            self.b = b
    a = A(1,2)
    b = A(1,2)
    dprint(a , b)