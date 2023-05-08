from .parser import FileDataParser,Mapper
import os 
from datetime import datetime
import re 
import math
# import numpy as np
import json
from .swtree import SWTree,SWNode
import logging
import numpy as np


#GFile 解析器         
class GfileParser(FileDataParser):

    def __init__(self, file_path):
        super().__init__(file_path)

    def _toENumStr(self,num):
        return "%2.9e"%num

    def write(self,sw_tree):
        data = sw_tree.toDict()
        shot = data['shot']
        time_slice = data['time_slice']
        if time_slice < 1:
            time_slice = int(time_slice*1000)

        time_str = datetime.now().strftime('%m/%d/%Y')
        nw = data['nw']
        nh = data['nh']
        nw = int(nw)
        nh = int(nh)
        line_str = ""
        line_str += f"EFITD         {time_str} # {shot} {time_slice}ms       3 {nw} {nh}\n"
        keys_keys = [
            ['rdim','zdim','rcentr','rleft','zmid'],
            ['rmaxis','zmaxis','simag','sibry','bcentr'],
            ['current','simag','xdum','rmaxis','xdum'],
            ['zmaxis','xdum','sibry','xdum','xdum'],
        ]
        for keys in keys_keys:
            l_s = ""
            for key in keys:
                d = 0
                if key in data.keys():
                    d = data[key]
                s = self._toENumStr(d)
                if d >= 0:
                    s = " " + s
                l_s += s
            l_s += "\n"
            line_str += l_s
         
        f_data = [0.0]*nw
        if 'fpol' in data.keys():
            f_data = data['fpol']
            if len(f_data) > nw:
                f_data = f_data[:nw]

        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"

        f_data = data['pres']
        if len(f_data) > nw:
            f_data = f_data[:nw]
        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"
        f_data = data['ffprime']
        if len(f_data) > nw:
            f_data = f_data[:nw]
        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"
        f_data = data['pprime']
        if len(f_data) > nw:
            f_data = f_data[:nw]
        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"
        
        f_data = [0.0]*nw*nh 
        if 'psirz' in data.keys():
            f_data = np.array(data['psirz']).reshape((nh,nw)).flatten().tolist()
        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"

        f_data = np.array(data['qpsi']).flatten().tolist()
        for i,d in enumerate(f_data):
            s = self._toENumStr(d)
            if d >= 0:
                s = " "+s 
            line_str += s
            if (i+1) % 5 == 0:
                line_str += "\n"
        if line_str[-1] != "\n":
            line_str += "\n"
        
        
        
        
        if 'nbbbs' in data.keys():
            nbbbs = data['nbbbs']
        else:
            nbbbs = len(data['rbbbs'])
            
        if 'limitr' in data.keys():
            limitr = data['limitr']
        else:
            limitr = len(data['rlim'])
            
      
        
        line_str += f'  {nbbbs}   {limitr}\n'
        index = 1
        for i in range(nbbbs):
            d1 = data['rbbbs'][i]
            s1 = self._toENumStr(d1)
            if d1 >=0 :
                s1 = " "+s1
            line_str += s1 
            if index % 5 == 0:
                line_str += "\n"
            index=index+1

            d2 = data['zbbbs'][i]
            s2 = self._toENumStr(d2)
            if d2 >= 0:
                s2 = " "+s2
            line_str += s2 
            if index % 5 == 0:
                line_str += "\n"
            index=index+1

        if line_str[-1] != "\n":
            line_str += "\n" 
            
        index = 1   
        for i in range(limitr):
            d1 = data['rlim'][i]
            s1 = self._toENumStr(d1)
            if d1 >=0 :
                s1 = " "+s1
            line_str += s1 
            if index % 5 == 0:
                line_str += "\n"
            index=index+1

            d2 = data['zlim'][i]
            s2 = self._toENumStr(d2)
            if d2 >= 0:
                s2 = " "+s2
            line_str += s2 
            if index % 5 == 0:
                line_str += "\n"
            index=index+1

        if line_str[-1] != "\n":
            line_str += "\n" 
        line_str += "            MSE"
        with open(self.file_path,'w') as f:
            f.write(line_str)


    def read(self):
        _,file = os.path.split(self.file_path)
        fmt_file = r'^g(\d+)\.(\d+)'
        fm = re.match(fmt_file, file)
        shot = 0
        if fm:
            shot = fm.group(1)
            time = fm.group(2)
            self.data['shot'] = int(shot)
            self.data['time'] = int(time)
        
        if not os.path.exists(self.file_path):
            return None
        lines = []
        try:
            lines = open(self.file_path).readlines()
        except Exception as e:
            print(e)
        #2000 format (6a8,3i4)  
        #\s*(.*)\s+\d+\s+ =   EFITD 08/27/2020    # 36000   300ms  
        fmt2000 = r'\s*(.*)\s+\d+\s+(\d+)\s+(\d+)\s*'
        # fmt2020 = r'^\s*([ \-]\d\.\d+[Ee][\+\-]\d\d)([ \-]\d\.\d+[Ee][\+\-]\d\d)([ \-]\d\.\d+[Ee][\+\-]\d\d)([ \-]\d\.\d+[Ee][\+\-]\d\d)([ \-]\d\.\d+[Ee][\+\-]\d\d)\s*$'
        fmt2020 = r'^\s*' + 5*r'([\s\-]\d+\.\d+[Ee][\+\-]\d\d)' 
        fmt_e =   r'^\s*[\s\-]\d\.\d+[Ee][\+\-]\d\d'
        fmt2022 = r'^\s*(\d+)\s+(\d+)'
        #解析 read (neqdsk,2000) (case(i),i=1,6),idum,nw,nh
        counter = 0
        line0 = lines[counter]
        m = re.search(fmt2000, line0)
        if m:
            self.data['case'] = m.group(1) #  
            self.data['nw'] = int(m.group(2)) # "Number of horizontal R grid points"
            self.data['nh'] = int(m.group(3))  #"Number of vertical Z grid points"
            counter += 1
        
         #解析 read (neqdsk,2020) rdim,zdim,rcentr,rleft,zmid
        keys_keys = [
            ['rdim','zdim','rcentr','rleft','zmid'],
            ['rmaxis','zmaxis','simag','sibry','bcentr'],
            ['current','simag','xdum','rmaxis','xdum'],
            ['zmaxis','xdum','sibry','xdum','xdum'],
        ]


        for keys in keys_keys:
            line = lines[counter]
            m = re.search(fmt2020, line)
            if m:
                for index ,key in enumerate(keys):
                    self.data[key] = eval(m.group(index+1))
                counter += 1
        
        #读数据到特殊行停止
        data = []
        while True:
            line = lines[counter]
            m1 = re.match(fmt_e, line)
            if not m1:
                break
            data += eval('[' + re.sub(r'(\d)([ \-]\d\.)', '\\1,\\2', line) + ']')
            counter += 1

        nw = self.data['nw']
        nh = self.data['nh']
        #read (neqdsk,2020) (fpol(i),i=1,nw)
        #read (neqdsk,2020) (pres(i),i=1,nw)
        self.data['fpol'] = data[0:nw]
        self.data['pres'] = data[nw:2*nw]
        self.data['ffprime'] = data[2*nw:3*nw]
        self.data['pprime'] = data[3*nw:4*nw]

        #read (neqdsk,2020) ((psirz(i,j),i=1,nw),j=1,nh)
        self.data['psirz'] = np.reshape( data[4*nw:4*nw+nw*nh], (nh, nw) )
        #read (neqdsk,2020) (qpsi(i),i=1,nw)
        self.data['qpsi']  =  np.array(data[4*nw+nw*nh:5*nw+nw*nh]).tolist()  

      
        
        line = lines[counter]
        #特殊行
        m2 = re.search(fmt2022, line)
        nbbbs = int(m2.group(1))
        limitr = int(m2.group(2))
        self.data['nbbbs'] = nbbbs
        self.data['limitr'] = limitr
        # 281   35
        counter += 1

        data = []
        while True:
            line = lines[counter]
            m = re.search(fmt_e, line)
            counter += 1
            if not m: break
            data += eval('[' + re.sub(r'(\d)([ \-]\d\.)', '\\1,\\2', line) + ']')
        
        self.data['rbbbs'] = np.zeros( (nbbbs,), np.float64 ).tolist()# "R of boundary points in meter"
        self.data['zbbbs'] = np.zeros( (nbbbs,), np.float64 ).tolist()# "Z of boundary points in meter"
        #read (neqdsk,2020) (rbbbs(i),zbbbs(i),i=1,nbbbs)
        for i in range(nbbbs):
            self.data['rbbbs'][i] = data[2*i]
            self.data['zbbbs'][i] = data[2*i + 1]
        
        self.data['rlim'] = np.zeros( (limitr,), np.float64 ).tolist()
        self.data['zlim'] = np.zeros( (limitr,), np.float64 ).tolist()
        #read (neqdsk,2020) (rlim(i),zlim(i),i=1,limitr)
        for i in range(limitr):
            self.data['rlim'][i] = data[2*nbbbs + 2*i]
            self.data['zlim'][i] = data[2*nbbbs + 2*i + 1]



        #--------------1st end of gfile with out currents------------------------
        data = data[2*nbbbs+2*limitr:]
        if len(data)>nw:
            shift = 0
            #read (neqdsk,2024,err=30900,end=30900) kvtor,rvtor,nmass
            kvtor = data[0]
            rvtor = data[1]
            nmass = data[2]
            if kvtor > 0:
                # read (neqdsk,2020) (presw(i),i=1,mw)
                self.data['presw'] = np.zeros( (nw,), np.float64 ).tolist()
                for i in range(nw):
                    self.data['presw'][i] = data[3+i]
                # read (neqdsk,2020) (preswp(i),i=1,mw)
                self.data['preswp'] = np.zeros( (nw,), np.float64 ).tolist()
                for i in range(nw):
                    self.data['preswp'][i] = data[3+nw+i]
                shift += nw*2
            if nmass > 0:
                # read (neqdsk,2020) (dmion(i),i=1,nw)
                self.data['preswp'] = np.zeros( (nw,), np.float64 ).tolist()
                for i in range(nw):
                    self.data['preswp'][i] = data[3+shift+i]
                shift += nw
            # read (neqdsk,2020) (rhovn(i),i=1,nw)
            self.data['rhovn'] = np.zeros( (nw,), np.float64 ).tolist()
            for i in range(nw):
                self.data['rhovn'][i] = data[3+shift+i]



            line = lines[counter]
            #特殊行
            m2 = re.search(fmt2022, line)
            keecur = int(m2.group(1))
            self.data['keecur'] = keecur
            # 2
            counter += 1

            if keecur > 0:
                data = []
                while True:
                    line = lines[counter]
                    m = re.search(fmt_e, line)
                    counter += 1
                    if not m: break
                    data += eval('[' + re.sub(r'(\d)([ \-]\d\.)', '\\1,\\2', line) + ']')
                self.data['workk'] = np.zeros( (nw,), np.float64 ).tolist()
                for i in range(nw):
                    self.data['workk'][i] = data[i]

            #---------------2nd end of gfile without currents-----------------






        #数据比较多
        # self.data['time'] = self.data['time']/1000
        tree = SWTree(name=f"gfile")
        # tree.time_slice = self.data['time']
        # tree.shot = self.data['shot']
        tree.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for key ,value in self.data.items():
             if isinstance(value, np.ndarray):
                node = SWNode(name=key,data=value.tolist())
             else:
                node = SWNode(name=key,data=value)
             tree.addNode(node)
        return tree
    

