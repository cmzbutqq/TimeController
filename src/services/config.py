"""_summary_
    TODO 配置文件交互
"""
import json
folder="config/"
name="user.json"

class Config:
    def __init__(self, cfg:dict):
        self.cfg:dict = cfg # cfg 是 Python dict 而 Config 是自定义类型
        
    
    
def get_config()->Config:
    with open(folder+name, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return Config(cfg)
def set_config(config:Config)->None:
    with open(folder+name, "w", encoding="utf-8") as f:
        json.dump(config.dict, f, indent=4, ensure_ascii=False)


    
    
set_config(get_config())