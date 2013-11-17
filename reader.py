__author__ = 'zhaoyuli'
import urllib
import time
import Image
import shutil
from StringIO import StringIO
import requests


picDict = {'0': '0.png',
           '1': '1.png',
           '2': '2.png',
           '3': '3.png',
           '4': '4.png',
           '5': '5.png',
           '6': '6.png',
           '7': '7.png',
           '8': '8.png',
           '9': '9.png',
           'A': 'a.png',
           'B': 'b.png',
           'C': 'c.png',
           'D': 'd.png',
           'E': 'e.png',
           'F': 'f.png',
           'G': 'g.png',
           'H': 'h.png',
           'I': 'i.png',
           'J': 'j.png',
           'K': 'k.png',
           'L': 'l.png',
           'M': 'm.png',
           'N': 'n.png',
           'O': 'o.png',
           'P': 'p.png',
           'Q': 'q.png',
           'R': 'r.png',
           'S': 's.png',
           'T': 't.png',
           'U': 'u.png',
           'V': 'v.png',
           'W': 'w.png',
           'X': 'x.png',
           'Y': 'y.png',
           'Z': 'z.png'
}



def readPic(imageList):
    code = ''
    for image in imageList:
        theKey = ''
        currentMax = 0
        for key, picName in picDict.iteritems():
            path = './codepic/'+picName
            #print key
            temp = my_image_similarity(image, path)
            if temp > currentMax:
                currentMax = temp
                theKey = key
        print theKey
        code = code + theKey
    print code
    return code


def my_image_similarity(filepath1, filepath2):
    list1 = list(Image.open(filepath1).getdata())
    list2 = list(Image.open(filepath2).getdata())
    counter = 0;
    for i in range(100):
        if list1[i] == list2[i]:
            counter = counter + 1

    return counter


def getWeizhangInfo(dict):
    s = requests.Session()
    r = s.get("http://218.58.65.23/select/WZ.asp")
    yzr=s.get('http://218.58.65.23/select/checkcode.asp')
    im = Image.open(StringIO(yzr.content))

    payload = {'stateid':'B','hphm':'7f128', 'hpzl':'02', 'jzh':'0477', 'yam':'L3EM', 'image.x':'-583', 'image.y':'-374'}
    r = s.post("http://218.58.65.23/select/WZ.asp",data=payload)
    r.encoding='gb2312'
    print r.text


for i in range(1):
    time.sleep(1)
    time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    time_stamp_jpg = time_stamp + '.jpg'
    urllib.urlretrieve("http://218.58.65.23/select/checkcode.asp", time_stamp_jpg)
    shutil.copy(time_stamp_jpg, time_stamp + 'origin.png')

    #cvImg = cv2.imread(time_stamp_jpg)
    #grayCvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite(time_stamp_jpg, grayCvImg)



    img = Image.open(time_stamp_jpg)
    grayImg = img.convert('L').point(lambda i: i > 128 and 255)
    grayImg.save(time_stamp_jpg)
    #imgFilter(grayImg, 0)
    frame1 = grayImg.crop(((0, 0, 10, 10)))
    frame1.save(time_stamp + '_1.png')
    frame2 = grayImg.crop(((10, 0, 20, 10)))
    frame2.save(time_stamp + '_2.png')
    frame3 = grayImg.crop(((20, 0, 30, 10)))
    frame3.save(time_stamp + '_3.png')
    frame4 = grayImg.crop(((30, 0, 40, 10)))
    frame4.save(time_stamp + '_4.png')

    imageList = [time_stamp + '_1.png', time_stamp + '_2.png', time_stamp + '_3.png', time_stamp + '_4.png']

    readPic(imageList)