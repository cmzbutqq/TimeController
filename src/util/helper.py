import time
def dataclass(cls): # 装饰器，给类加上__repr__,__str__,__eq__,__hash__方法
    def __str__(self)->str:
        return f"type:{self.__class__.__name__}"
    cls.__str__ = __str__
    def __repr__(self)->str:
        return f"type:{self.__class__.__name__}\tattrs:{self.__dict__}"
    cls.__repr__ = __repr__
    def __eq__(self,other)->bool:
        return self.__dict__ == other.__dict__
    cls.__eq__ = __eq__
    def __hash__(self)->int:
        return hash(self.__dict__)
    __hash__ = __hash__
    return cls

class timeit: # 计时器 计算with timeit():后面的代码块运行时间
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"E:{exc_type}\t{exc_val}\t{exc_tb}")
        print(f"T:{time.time()-self.start}")

