import json
import requests
from utils import get_data


def get_user_id(emp_no: str) -> str:
    data = get_data()
    url = data.get('EMP_ID_URL')

    payload = {
        "msname": "test",
        "pageNo": 1,
        "pageSize": 1,
        "queryConditionDTO": {
            "queryType": "Q0001",
            "queryVer": "v1",
            "queryKey": emp_no
        }

    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return json.loads(response.text)['bo']['rows'][0]['id']


def main():
    return get_user_id('XXX')


if __name__ == '__main__':
    res = main()
    print(res)
