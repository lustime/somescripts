# -*- coding: utf-8 -*-
"""
cron: 0 9 * * *
new Env('我的考勤异常');
"""

import json
import requests
import datetime
import calendar
from notify_mtr import send
from my_util import get_user_id
from utils import get_data
from my_email_util import sendMail


class KQYC:

    def __init__(self, check_items):
        self.check_items = check_items

    def get_kq(self, url, emp_no):
        user_id = get_user_id(emp_no)
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        day = str(calendar.monthrange(year, month)[1])
        first_day = str(year) + '-' + str(month) + '-' + '1'
        last_day = str(year) + '-' + str(month) + '-' + day
        headers = {
            'x-emp-id': user_id,
            'x-emp-no': emp_no,
            'x-lang-id': 'zh_CN',
            'x-tenant-id': '10000',
            'Content-Type': 'application/json'
        }

        payload = {
            "command": "KQ-JG-002",
            "params": {
                "pageDTO": {
                    "pageSize": "100",
                    "pageNo": "1"
                },
                "startDate": first_day,
                "endDate": last_day,
                "displayType": "01",
                "empId": user_id
            }
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        abnormalAttendancTimes = str(json.loads(response.text)['bo']['abnormalAttendancTimes'])
        absenceTimes = str(json.loads(response.text)['bo']['abnormalAttendanceStatisticDTO']['absenceTimes'])
        lateOrLeaveEarlyTimes = str(json.loads(response.text)['bo']
                                    ['abnormalAttendanceStatisticDTO']
                                    ['lateOrLeaveEarlyTimes'])
        realInWorkTimes = str(json.loads(response.text)['bo']
                              ['abnormalAttendanceStatisticDTO']
                              ['realInWorkTimes'])
        return abnormalAttendancTimes, absenceTimes, lateOrLeaveEarlyTimes, realInWorkTimes

    def main(self):
        msg_all = ''
        has_abnormal = False
        url = self.check_items.get('url')
        for check_item in self.check_items.get('emp_info'):
            emp_no = check_item.get('emp_no')
            abnormalAttendancTimes, absenceTimes, lateOrLeaveEarlyTimes, realInWorkTimes = self.get_kq(url, emp_no)
            msg_all = "本月上班" + realInWorkTimes + "天," + "异常考勤:" + abnormalAttendancTimes + "次" + "\n"
            msg_all += "其中缺席:" + absenceTimes + "次" + "\n"
            msg_all += "迟到早退:" + lateOrLeaveEarlyTimes + "次" + "\n"
            has_abnormal = has_abnormal or int(abnormalAttendancTimes) > 0
        if has_abnormal:
            send("异常考勤提醒", msg_all)
            sendMail(msg_all, '考勤通知', '', '', '')
        else:
            print('无异常考勤，跳过通知')
        return msg_all


def start():
    data = get_data()
    _check_items = data.get('KQYC', [])
    res = KQYC(check_items=_check_items).main()
    print(res)


if __name__ == '__main__':
    start()
