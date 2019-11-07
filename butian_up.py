import json
import urllib3
import time

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


butian_header_dic = {
    "Host": "www.butian.net",
    "Connection": "keep-alive",
    "Content-Length": "66",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://www.butian.net",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
    "Sec-Fetch-Mode": "cors",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.butian.net/WhiteHat/Center/loo",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": config.butian_cookie,
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def mark_url(url):
    index = url.index(".jpg")
    r = requests.get(url, verify=False)
    content = r.content
    filename = url[index - 32:index]
    return mark_req(filename, content)


# 调用联众打码平台，文字点选验证码识别
def mark_req(file_name, content):
    print("start upload captcha...")
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Connection': 'keep-alive',
        'Host': 'v1-http-api.jsdama.com',
        'Upgrade-Insecure-Requests': '1'
    }

    files = {
        'upload': (file_name, content, 'image/png')
    }

    data = {
        'user_name': config.LZ_USERNAME,
        'user_pw': config.LZ_PASSWORD,
        'yzmtype_mark': config.LZ_CAPTCHA_TYPE,
        'zztool_token': config.LZ_TOKEN
    }
    r = requests.post(config.LZ_API, headers=headers, data=data, files=files,
                      verify=False)
    result = r.text
    if r.status_code == 200:
        return json.loads(result)
    return {}


def req_butian_last():
    '''
    获取补天提交的最后一个厂商
    :return:
    '''
    url = "https://www.butian.net/WhiteHat/Center/loo"
    post_str = "level=&status=1&p=1&token=xxxxxxxxxx"
    with requests.post(url, headers=butian_header_dic, data=post_str, timeout=5, verify=False) as r:
        html = r.text
        item = json.loads(html)
        last_comp = item["data"]["list"][0]["company_name"]
        return last_comp
    return ""


class Butian(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.butian.net/")
        self.driver.add_cookie({
            "domain": "www.butian.net",
            "name": config.btlc_name,
            "value": config.btlc_value,
            "path": '/',
            "expires": None
        })
        self.is_quit = 0

        self.driver.add_cookie({
            "domain": "www.butian.net",
            "name": "PHPSESSID",
            "value": config.phpsessid,
            "path": '/',
            "expires": None
        })

    # 判断提交是否成功
    def _up_success(self, comp_name):
        last_comp_name = req_butian_last()
        print(last_comp_name, comp_name)
        if last_comp_name == comp_name:
            return True
        return False

    def submit(self, comp_name, host, poc_type, poc_url, poc_desc, poc_detail, poc_img):
        print("test:", comp_name)
        try:
            self.driver.get("https://www.butian.net/Loo/submit")
            time.sleep(2)
            self.driver.find_element_by_id("inputCompy").send_keys(comp_name)

            self.driver.find_element_by_name("host").send_keys(host)

            time.sleep(1)
            Select(self.driver.find_element_by_id("selCate")).select_by_index(1)

            poc_title = comp_name+"网站某处存在"+poc_type
            self.driver.find_element_by_id("title").send_keys(poc_title)
            self.driver.find_element_by_name("url[]").send_keys(poc_url)

            time.sleep(1)

            Select(self.driver.find_element_by_name("attribute")).select_by_index(0)

            loc = self.driver.find_element_by_id("lootypesel2").location
            ActionChains(self.driver).move_by_offset(loc['x'], loc['y']).click().perform()

            Select(self.driver.find_element_by_id("lootypesel2")).select_by_index(12)

            Select(self.driver.find_element_by_name("level")).select_by_index(0)

            poc_profile = config.PRE_FLAG + poc_title
            self.driver.find_element_by_id("description").send_keys(poc_profile)

            # 插入python代码， 因为url格式千奇百怪，防止插入的时候出错，直接插到python的代码区域
            self.driver.find_element_by_id("edui93").click()
            time.sleep(1)
            # ActionChains(self.driver).move_to_element_with_offset(
            #     self.driver.find_element_by_id("edui90_body"), 0, 5).double_click().perform()
            self.driver.find_element_by_id("edui113").click()
            time.sleep(1)
            self.driver.find_element_by_id("edui113").click()
            time.sleep(1)

            # 将焦点放在iframe中
            self.driver.switch_to.frame("ueditor_0")
            self.driver.find_element_by_tag_name('body').send_keys(poc_desc)
            time.sleep(1)
            self.driver.find_element_by_css_selector("body > p").click()
            time.sleep(1)
            self.driver.find_element_by_css_selector("body").send_keys(poc_detail)
            self.driver.switch_to.default_content()

            self.driver.find_element_by_id("edui92_body").click()

            self.driver.switch_to.frame("edui88_iframe")
            self.driver.find_elements_by_css_selector('div#tabhead > span')[0].click()
            self.driver.find_element_by_id('url').send_keys(poc_img)

            # 将焦点从iframe中切出来
            self.driver.switch_to.default_content()
            time.sleep(1)

            self.driver.find_element_by_id('edui90_body').click()

            # 选择使用SQL的修复建议
            self.driver.find_element_by_id("repair_suggest").send_keys(config.REPAIR["SQL"])

            # 行业这里默认填互联网行业
            Select(self.driver.find_element_by_name("industryLoo1")).select_by_index(16)
            time.sleep(2)
            self.driver.find_element_by_id("21").click()
            time.sleep(1)

            # 地区这里默认填北京
            Select(self.driver.find_element_by_id("selec1")).select_by_value("北京市")
            time.sleep(1)
            Select(self.driver.find_element_by_id("selec2")).select_by_value("市辖区")
            time.sleep(1)
            Select(self.driver.find_element_by_id("selec3")).select_by_value("东城区")

            self.driver.find_element_by_name("anonymous").click()

            time.sleep(1)
            self.driver.find_element_by_id("tijiao").click()

            time.sleep(5)
            img_url = self.driver.find_element_by_class_name("geetest_item_img").get_attribute("src")
            # TODO 要判断直接提交成功以及验证码是滑块的情况
            '''
                不判断了，懒得搞，这两种情况很少见
            '''

            captcha_result = mark_url(img_url)

            val = captcha_result["data"]["val"]
            locs = val.split("|")

            for item in locs:
                ActionChains(self.driver).move_to_element_with_offset(self.driver.find_element_by_class_name("geetest_table_box"), 0, 0).perform()
                tmp_loc_x = int(item.split(",")[0])
                tmp_loc_y = int(item.split(",")[1])-10
                ActionChains(self.driver).move_by_offset(tmp_loc_x, tmp_loc_y).click().perform()
                time.sleep(0.3)

            self.driver.find_element_by_class_name("geetest_commit_tip").click()
            time.sleep(6)
            return self._up_success(comp_name)
        except Exception as e:
            print(e)
            # time.sleep(50)
            self.quit()
            return False

    def quit(self):
        self.driver.close()
        self.driver.quit()
        self.is_quit = 1


if __name__ == '__main__':

    comp_name = "王老菊未来科技有限公司"
    host = "wanglaoju.com"
    poc_type = "SQL注入"
    poc_url = "http://www.baidu.com"
    poc_desc = "漏洞描述"
    poc_detail = "漏洞详情"
    poc_img = "https://shs3.b.qianxin.com/butian_public/f932191add9a69347f59c42894a316905920be20ef9a5.png"

    # comp_name = "厂商名称"
    # host = "域名"
    # poc_type = "漏洞类型"
    # poc_url = "漏洞url"
    # poc_desc = "漏洞描述"
    # poc_detail = "漏洞详情"
    # poc_img = "漏洞的图片地址"
    butian = Butian()
    flag = butian.submit(comp_name, host, poc_type, poc_url, poc_desc, poc_detail, poc_img)

    if butian.is_quit == 0:
        butian.quit()