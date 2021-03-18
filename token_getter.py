# encoding:utf-8
import requests
import json

# client_id 为官网获取的AK， client_secret 为官网获取的SK
AppID = '23824451'
API_key = 'YlA81wKMkpuz9iOzorx41OBs'
Secret_key = '7MK9coeAt8VgemQu9oqRqGulF8QRNQ6k'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(API_key,Secret_key)

def get_token_info():
    response = requests.get(host)
    token_info = {}
    if response:
        # print(response.json())
        token_info = json.loads(response.text)
        # for key, value in token_info.items():
        #     print('{key}:{value}'.format(key=key, value=value))
        # if token_info['error'] != None:
        #     if token_info['error_description'] == 'unknown client id':
        #         print('API Key不正确')
        #     elif token_info['error_description'] == 'unknown client id':
        #         print('Secret Key不正确')
    return token_info


if __name__ == '__main__':
    print(get_token_info())