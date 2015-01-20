 # -*- coding: utf-8 -*-
__author__ = 'zhaoyuli'
import Image
from StringIO import StringIO
import requests
from bs4 import BeautifulSoup
import web

"""
测试方式：http://127.0.0.1:8080/wzAPI?stateid=B&plateNo=7f128&license=0477
"""

urls = (
    '/', 'index',
    '/(wzAPI)', 'Hello'
)

template_globals = {
    "cookies": web.cookies,
}

class index:
    def GET(self):
        print web.cookies().get('state_id')
        render = web.template.render('templates/', globals=template_globals, cache=False)
        return render.query()

app = web.application(urls, globals())


class Hello:
    def __init__(self):
        pass

    def GET(self, name):
        result_list = []

        def get_weizhang_info(state_id, plate_no, license_no):
            s = requests.Session()
            r = s.get("http://218.58.65.23/select/WZ.asp")
            yzr=s.get('http://218.58.65.23/select/checkcode.asp')
            im = Image.open(StringIO(yzr.content))
            # debug only
            #im.show()

            image_list = cut_pictures(im)
            code_text = read_pics(image_list)

            payload = {'stateid':state_id,'hphm':plate_no, 'hpzl':'02', 'jzh':license_no, 'yam':code_text, 'image.x':'-583', 'image.y':'-374'}
            r = s.post("http://218.58.65.23/select/WZ.asp",data=payload)
            r.encoding='gb2312'
            #print r.text
            parsed_html = BeautifulSoup(r.text)
            html = parsed_html.prettify().encode('utf-8')
            if r'请输入正确的验证码' in html:
                return get_weizhang_info(state_id, plate_no, license_no)
            # Find the specific table, rather than the whole one.
            data_table = parsed_html.find_all("table",  {"width":"100%", "align":"center", "border":"0", "cellspacing":"0", "cellpadding":0  })

            if len(data_table) < 2:
                return None
            rows = data_table[2].findAll('tr')
            for tr in rows:
                cols = tr.findAll('td', {"class": "css"})
                result_list.append([c.text for c in cols])


            weizhang_tables = parsed_html.find_all("table",  {"width":5, "align":"center", "border":"0", "cellspacing":"0", "cellpadding":0  })
            for weizhang_table in weizhang_tables:
                for weizhang_row in weizhang_table.find_all('tr'):
                    cols = weizhang_row.findAll('td')
                    if len(cols) == 7:
                        result_list.append([c.text for c in cols])


            return 'successful'


        web.header('Content-Type', 'text/html; charset=utf-8')
        ret_str=''
        user_data = web.input()
        # print user_data
        state_id = ''
        plate_id = ''
        license_id = ''
        try:
            state_id = user_data.stateid
            plate_id = user_data.plateNo
            license_id = user_data.license
            web.setcookie('state_id', state_id, 3600000)
            web.setcookie('plate_id', plate_id, 3600000)
            web.setcookie('license_id', license_id, 3600000)
        except:
            ret_str = r"""输入格式错误，请重按照说明新输入"""
        ret_str = str(get_weizhang_info(state_id, plate_id, license_id))
        # ret_str = html_header + ret_str + html_ender
        if ret_str == 'None':
            ret_str = r'输入格式错误，请重新按照说明输入'
            return ret_str
        render = web.template.render('templates/', globals=template_globals, cache=False)
        return render.result(result_list)


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

def read_pics(image_list):
    """
    read characters from the 4 input images
    """

    code = ''
    for image in image_list:
        the_key = ''
        current_max = 0
        for key, picName in picDict.iteritems():
            #print key
            temp = my_image_similarity(image, picName)
            if temp > current_max:
                current_max = temp
                the_key = key
        code = code + the_key
    print r'验证码:' + code
    return code


def my_image_similarity(image, character_image):
    list1 = list(image.getdata())
    list2 = list(character_image.getdata())
    counter = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            counter += 1
    return counter

def cut_pictures(img):
    gray_img = img.convert('L').point(lambda i: i > 128 and 255)
    frame1 = gray_img.crop(((0, 0, 10, 10)))
    frame2 = gray_img.crop(((10, 0, 20, 10)))
    frame3 = gray_img.crop(((20, 0, 30, 10)))
    frame4 = gray_img.crop(((30, 0, 40, 10)))
    image_list = [frame1, frame2, frame3, frame4]
    return image_list


if __name__ == '__main__':
    #getWeizhangInfo('B', '7f128', '0477')
    app.run()

