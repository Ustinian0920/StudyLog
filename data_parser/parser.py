from abc import ABC, abstractmethod
import os 
from datetime import datetime
import re 
import math
import numpy as np
import json

#解析器抽象类包含read方法
class Parser(ABC):
    @abstractmethod
    def read(self):
        ...
    @abstractmethod
    def write(self,sw_tree):
        ...

#文件数据解析器类      
class FileDataParser(Parser):
    def __new__(cls,*args,**kwargs):
        new_object = super().__new__(cls)
        return new_object
    def __init__(self,file_path):
        self.file_path = file_path
        self.data = {}
        self.mapper_path = None
    
    def setFilePath(self,path):
        self.file_path = path
    
    def read(self):
        ...
    def write(self,sw_tree):
        ...


class Mapper(ABC):
    @abstractmethod
    def before_mapping(self):
        ...
    @abstractmethod
    def after_mapping(self):
        ...
    @abstractmethod
    def mapping(self,data):
        ...
    @abstractmethod
    def updateMapper(self,path):
        ...



