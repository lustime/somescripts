import json
import requests
from utils import get_data


def get_user_id(emp_no: str) -> str:
    data = get_data()
    url = data.get('EMP_ID_URL')

    payload = {
        "command": "TY-GR-002",
        "params": {
            "empShortId": emp_no
        }

    }

    headers = {
        'Content-Type': 'application/json',
        'x-emp-no': emp_no,
        'x-emp-id': '0',
        'x-lang-id': 'zh_CN',
        'x-tenant-id': '10000'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text).get('bo').get('empId')

def main():
    return get_user_id('XXX')


if __name__ == '__main__':
    res = main()
    print(res)
