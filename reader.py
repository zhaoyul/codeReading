 # -*- coding: utf-8 -*-
__author__ = 'zhaoyuli'
import requests
import web
import json

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
        # ret_str = str(get_weizhang_info(state_id, plate_id, license_id))
        url = "http://sixinone.qdznjt.com/sixinone/services/queryObjectOut"
        headers = {'content-type': "application/json",
                   "xtlb": "aiqingdao",
                   "jkid": "04C01",
                   "authCode": "53ea94bd0c68477685be10287f2c3867"}
        payload = {
            "hpzl": "02",
            "hphm": "鲁B789CA",
            "clsbdh": "6170",
            "sjhm": "18888888888",
            "startNum": 1,
            "endNum": 5
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        # ret_str = html_header + ret_str + html_ender
        if ret_str == 'None':
            ret_str = r'输入格式错误，请重新按照说明输入'
            return ret_str
        render = web.template.render('templates/', globals=template_globals, cache=False)
        return render.result(result_list)






if __name__ == '__main__':
    #getWeizhangInfo('B', '7f128', '0477')
    app.run()

