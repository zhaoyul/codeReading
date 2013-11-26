 # -*- coding: utf-8 -*-
__author__ = 'zhaoyuli'
import Image
from StringIO import StringIO
import requests
from bs4 import BeautifulSoup
import codecs
import web
import re

urls = (
    '/(wzAPI)', 'Hello'
)

app = web.application(urls, globals())


class Hello:
    def GET(self, name):
        web.header('Content-Type', ' text/html; charset=utf-8')
        ret_str=''
        user_data = web.input()
        state_id = ''
        plate_id = ''
        license_id = ''
        try:
            state_id = user_data.stateid
            plate_id = user_data.plateNo
            license_id = user_data.license
        except:
            ret_str = r'输入格式为:http://127.0.0.1:8080/wzAPI?stateid=B&plateNo=7f128&license=0477'
        ret_str = str(getWeizhangInfo(state_id, plate_id, license_id))
        if ret_str == 'None':
            ret_str = r'输入信息不正确,http://127.0.0.1:8080/wzAPI?stateid=B&plateNo=7f128&license=0477'
        return ret_str


picDict = {'0': Image.open('./codepic/0.png'),
           '1': Image.open('./codepic/1.png'),
           '2': Image.open('./codepic/2.png'),
           '3': Image.open('./codepic/3.png'),
           '4': Image.open('./codepic/4.png'),
           '5': Image.open('./codepic/5.png'),
           '6': Image.open('./codepic/6.png'),
           '7': Image.open('./codepic/7.png'),
           '8': Image.open('./codepic/8.png'),
           '9': Image.open('./codepic/9.png'),
           'A': Image.open('./codepic/a.png'),
           'B': Image.open('./codepic/b.png'),
           'C': Image.open('./codepic/c.png'),
           'D': Image.open('./codepic/d.png'),
           'E': Image.open('./codepic/e.png'),
           'F': Image.open('./codepic/f.png'),
           'G': Image.open('./codepic/g.png'),
           'H': Image.open('./codepic/h.png'),
           'I': Image.open('./codepic/i.png'),
           'J': Image.open('./codepic/j.png'),
           'K': Image.open('./codepic/k.png'),
           'L': Image.open('./codepic/l.png'),
           'M': Image.open('./codepic/m.png'),
           'N': Image.open('./codepic/n.png'),
           'O': Image.open('./codepic/o.png'),
           'P': Image.open('./codepic/p.png'),
           'Q': Image.open('./codepic/q.png'),
           'R': Image.open('./codepic/r.png'),
           'S': Image.open('./codepic/s.png'),
           'T': Image.open('./codepic/t.png'),
           'U': Image.open('./codepic/u.png'),
           'V': Image.open('./codepic/v.png'),
           'W': Image.open('./codepic/w.png'),
           'X': Image.open('./codepic/x.png'),
           'Y': Image.open('./codepic/y.png'),
           'Z': Image.open('./codepic/z.png')
}


def read_pics(imageList):
    """
    read characters from the 4 input images
    """

    code = ''
    for image in imageList:
        theKey = ''
        currentMax = 0
        for key, picName in picDict.iteritems():
            #print key
            temp = my_image_similarity(image, picName)
            if temp > currentMax:
                currentMax = temp
                theKey = key
        #print theKey
        code = code + theKey
    print code
    return code


def my_image_similarity(image, characterImage):
    list1 = list(image.getdata())
    list2 = list(characterImage.getdata())
    counter = 0;
    for i in range(100):
        if list1[i] == list2[i]:
            counter = counter + 1

    return counter


def getWeizhangInfo(stateid, plateNo, license):
    s = requests.Session()
    r = s.get("http://218.58.65.23/select/WZ.asp")
    yzr=s.get('http://218.58.65.23/select/checkcode.asp')
    im = Image.open(StringIO(yzr.content))
    # debug only
    #im.show()

    imageList = cutPictures(im)
    cdoeText = read_pics(imageList)


    payload = {'stateid':stateid,'hphm':plateNo, 'hpzl':'02', 'jzh':license, 'yam':cdoeText, 'image.x':'-583', 'image.y':'-374'}
    r = s.post("http://218.58.65.23/select/WZ.asp",data=payload)
    r.encoding='gb2312'
    #print r.text
    parsed_html = BeautifulSoup(r.text)
    html = parsed_html.prettify().encode('utf-8')
    if r'请输入正确的验证码' in html:
        return getWeizhangInfo(stateid, plateNo, license)

    #width="100%" align="center"  border="0" cellspacing="0" cellpadding="0"
    tabulka = parsed_html.find("table",  {"width":"100%", "align":"center", "border":"0", "cellspacing":"0", "cellpadding":0  })
    #tabulka = parsed_html.findNext()

    rawTable = str(tabulka);
    #replace images
    processedTable, n = re.subn(r'<td.+?images.+?<\/td>','', rawTable)
    #replace info
    processedTable = re.sub(r'<br>.+</br>','',processedTable)
    processedTable = re.sub(r'<center>.+</center>','',processedTable)


    print rawTable
    print '------------------------------'
    print processedTable

    return BeautifulSoup(processedTable)

    records = [] # store all of the records in this list
    #for row in tabulka.findAll('tr'):
    #    col = row.findAll('td')
    #    prvy = col[0].string.strip()
    #    #druhy = col[1].string.strip()
    #    record = '%s' % (prvy) # store the record with a ';' between prvy and druhy
    #    records.append(record)
    #    print records

    fl = codecs.open('output.txt', 'wb', 'utf8')
    line = ';'.join(records)
    fl.write(line + u'\r\n')
    fl.close()


def cutPictures(img):
    grayImg = img.convert('L').point(lambda i: i > 128 and 255)
    frame1 = grayImg.crop(((0, 0, 10, 10)))
    frame2 = grayImg.crop(((10, 0, 20, 10)))
    frame3 = grayImg.crop(((20, 0, 30, 10)))
    frame4 = grayImg.crop(((30, 0, 40, 10)))
    imageList = [frame1, frame2, frame3, frame4]
    return imageList


#for i in range(1):
#    time.sleep(1)
#    time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
#    time_stamp_jpg = time_stamp + '.jpg'
#    urllib.urlretrieve("http://218.58.65.23/select/checkcode.asp", time_stamp_jpg)
#    shutil.copy(time_stamp_jpg, time_stamp + 'origin.png')
#
#    img = Image.open(time_stamp_jpg)

if (__name__ == '__main__'):
    render = web.template.render('templates/')
    #getWeizhangInfo('B', '7f128', '0477')
    app.run()

