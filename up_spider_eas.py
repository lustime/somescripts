# -*- coding: utf-8 -*-
"""
cron: 0 9 * * *
new Env('璐宝宝考勤异常');
"""

import datetime
import json
import time
import warnings

import requests
# from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from notify_mtr import send
from utils import get_data
from my_email_util import sendMail
import platform

warnings.filterwarnings("ignore", category=Warning)


class SpiderAirport:

    def __init__(self, check_items):
        self.check_items = check_items

    def login(self):
        username = self.check_items.get('username')
        password = self.check_items.get('password')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920x1080')
        # options.binary_location = binary_location
        e = platform.system()
        #c = webdriver.Chrome(ChromeDriverManager(path="./").install(),
        #                         chrome_options=options)
        if e == 'Windows':
            # pip install webdriver-manager
            c = webdriver.Chrome(ChromeDriverManager(path="./").install(),
                                 chrome_options=options)
        else:
            c = webdriver.Chrome(chrome_options=options)
        c.implicitly_wait(10)
        url = self.check_items.get('url') + 'portal/main.jsp'
        c.get(url)
        c.find_element(By.ID, 'username').send_keys(username)
        c.find_element(By.ID, 'password').send_keys(password)
        c.find_element(By.ID, 'loginSubmit').click()
        time.sleep(2)
        ck = c.get_cookies()
        cookies_dic = dict()
        for cookie in ck:
            cookies_dic[cookie['name']] = cookie['value']
        session = requests.session()
        requests.utils.add_dict_to_cookiejar(session.cookies, cookies_dic)
        return session, c

    def getUserInfo(self):
        print("begin to login for cookie...")
        session, c = self.login()
        print("login success, get cookie success.")
        time.sleep(2)
        try:
            c.find_element(By.ID, 'btnKick').click()
        except BaseException:
            print("...")

        referer = self.check_items.get('Referer')
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
                "Referer": referer,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        param = self.check_items.get('param')
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        begin_date = str(year) + '-' + str(month) + '-01'
        end_date = str(year) + '-' + str(month) + '-' + str(day)
        # param += "filterItems1=result.FAttenceDate+>=+'" + begin_date + "'+"
        param += '&beginDate=' + begin_date + '&endDate=' + end_date
        rel_url = self.check_items.get('url') + 'shr/dynamic.do'
        print("begin to query kq info..")
        response = session.get(url=rel_url, params=param, verify=False)
        print("get kq info success.")
        data = json.loads(response.text)['rows']
        self.quit(c)
        person_number = self.check_items.get('personNumber')
        yl = ''
        for d in data:
            if d['personNumber'] == person_number:
                yl = d
                break
        msg_text = "姓名：" + str(yl['personName']) + "\n"
        msg_text += "缺卡次数：" + str(yl['S38']) + ",矿工次数：" + str(yl['S22']) + ",迟到次数：" + str(yl['S18']) + ",早退次数： " + str(
            yl['S20']) + "\n"
        msg_text += "补卡次数：" + str(yl['S24']) + ",请假次数：" + str(yl['S26'])
        if yl['S38'] or yl['S22'] or yl['S18'] or yl['S20'] > 0:
            send("璐宝宝异常考勤提醒", msg_text)
            mail_to_address = self.check_items.get('mail_to_address')
            if self.check_items.get('send_mail'):
                sendMail(msg_text, '璐宝宝考勤异常提醒', mail_to_address)
        else:
            print('无考勤异常，跳过通知。')
        return msg_text

    @staticmethod
    def quit(c):
        time.sleep(10)
        move = c.find_element(By.ID, 'userLogo')
        ActionChains(c).move_to_element(move).perform()
        time.sleep(2)
        c.find_element(By.XPATH, '//div[@class="portal-header-logout"]').click()
        time.sleep(2)
        # c.switch_to_default_content()
        quite = c.find_element(By.XPATH, "//*[@role='button']/span[contains(text(), '安全退出')]")
        # q = quite.find_element(By.XPATH, "./..")
        quite.click()
        time.sleep(5)
        c.close()
        c.quit()


def start():
    data = get_data();
    _check_items = data.get('EAS', [])
    res = SpiderAirport(check_items=_check_items).getUserInfo()
    print(res)


if __name__ == '__main__':
    start()
