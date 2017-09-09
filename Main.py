# *****************图片下载器--ZyCoder*****************

from urllib import request,parse
from Headers import GetHeader
from json import loads
from MkDir import MkDirDown
import random
import re

# 图片列表
def GetImgList(userid,albumid):
    req=request.Request('https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s'%(userid,albumid))
    req.add_header('user-agent', GetHeader())
    html = request.urlopen(req).read().decode('gbk')
    dict=loads(html)
    list=[]
    for i in dict['picList']:
        picUrl=i['picUrl']
        reg=r'290x10000'
        url= re.sub(reg,'620x10000',picUrl)  #大图地址
        list.append(url)
    return list

def GetAlbumList(userid):
    req=request.Request('https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%%20=%s'%(userid))
    req.add_header('user-agent', GetHeader())
    html=request.urlopen(req).read().decode('gbk')
    reg=r'class="mm-first" href="//(.*?)"'
    return re.findall(reg,html)[::2]

def GetUrlList():
    req=request.Request('https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
    req.add_header('user-agent',GetHeader())
    total=0
    for i in range(1,1450):   #遍历  1450页
        data = {
            'q': '',
            'viewFlag': 'A',
            'sortType': 'default',
            'searchStyle': '',
            'searchRegion': 'city:',
            'searchFansNum': '',
            'currentPage': i,   #页数
            'pageSize': 100
        }
        data=parse.urlencode(data).encode('gbk')
        html=request.urlopen(req,data=data).read().decode('gbk')
        dict=loads(html)
        for n in dict['data']['searchDOList']:
            print(n['realName'])
            mpath=n['realName']+'城市'+n['city']+'身高'+n['height']+'体重'+n['weight']
            #  *************创建目录**************
            MkDirDown(mpath)
            for i in GetAlbumList(n['userId']):  # i 相册url
                # print(i)   # 相册url
                reg=r'album_id=(.+?)&'
                albumid=re.findall(reg,i)[0] # 相册id
                list = GetImgList(n['userId'],albumid)
                path='E:\\MMPic'+'\\'+mpath
                # 'E:\\MMPic'
                for i in list:
                    print('正在下载>>>%s第%s张'%(n['realName'],total))
                    total+=1
                    request.urlretrieve('http:%s'%(i),path+'\\%s.jpg'%(random.randint(0,9999)))
                print(len(list))
GetUrlList()