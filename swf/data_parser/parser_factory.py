
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# parser_factory.py
# 解析器工厂



import os
import re

base_dir = os.path.dirname( os.path.realpath(__file__))
# 动态引入parser
parsers = []
exec_str  = ""
for f in os.listdir(base_dir):
    m = re.match(r"(\w+Parser)\.py", f)
    if m:
        p_name = m.group(1)
        parsers.append(p_name)
        exec_str += f"from .{p_name} import {p_name}\n"
exec(exec_str)

class ParserFactory():
    @staticmethod
    def getParser(name,file_path):
        c_name  = name.capitalize()
        p_name = f"{c_name}Parser"
        if p_name in parsers:
            return  eval(f"{c_name}Parser('{file_path}')")
        raise  KeyError("解析器配置错误")
