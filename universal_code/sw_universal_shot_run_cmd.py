
from config import config 
from sw_viewer_tools import *
import sys
import time as tm
import cProfile

def get_shot_run():
 
    db = sys.argv[1]
    user = sys.argv[2]
 
    ids = {}

    imas_path_parser = IMASPathParser(user)
    ids_shot_list =[int(i) for i in imas_path_parser.get_shot(db)]
    ids_shot_list.sort()
    for shot in ids_shot_list:
        shot = str(shot)
        ids[shot] = []
        run_list = imas_path_parser.get_run_number_list(db,int(shot))
        ids[shot] = run_list
        if ids[shot] == []:
            ids.pop(shot)

    dic = ids

    return dic

if __name__=="__main__":
    dic = {"data":get_shot_run()}
    data_json_str = json.dumps(dic)
    print(data_json_str)