import json

import requests
from requests_toolbelt import MultipartEncoder


butian_headers_str='''Host: www.butian.net
Sec-Fetch-Mode: cors
Origin: https://www.butian.net
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36
Accept: */*
Sec-Fetch-Site: same-origin
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryx1m9sWUsRMvfpPo2
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Pragma: no-cache
Cache-Control: no-cache
Connection: keep-alive'''


# 补天上传图片
def up_butian_img(imgName, path):
    up_img_url = "https://www.butian.net/Public/ueditor/php/controller.php?action=uploadimage"
    header_dic = dict([line.split(": ", 1) for line in butian_headers_str.split("\n")])
    file_headers_1 = {
        'upfile': (imgName+".png", open(path, 'rb'), 'image/png'),
        'type': (None, 'ajax')
    }
    m = MultipartEncoder(
        fields=file_headers_1,
        boundary='----WebKitFormBoundaryx1m9sWUsRMvfpPo2')
    with requests.post(up_img_url, data=m, headers=header_dic, verify=False) as r:
        if r.status_code == 200:
            return json.loads(r.text)['url']
        return ""
    return ""


if __name__ == '__main__':
    img_url = up_butian_img('1', '1.png')
    print(img_url)