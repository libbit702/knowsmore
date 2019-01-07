import datetime
import os
import re
import json
from scrapy.utils.project import get_project_settings

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

settings = get_project_settings()

project_proxy_file = settings.get('PROXY_LIST')

def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs