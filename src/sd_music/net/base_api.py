import requests


class BaseApi:
    def __init__(self,timeout=30):
        self.session = requests.session()
        self.timeout = timeout

    def common_get_request(self,url,header):
        r=requests.get(url,headers=header,timeout=self.timeout)
        result=r.json()
        if result['code'] != 200:
            print('Error return{} when try to use get function{}'.format(result,url))
        else:
            return result

    def common_post_request(self,url,header,params):
        r=requests.post(url,headers=header,data=params,timeout=self.timeout)
        result=r.json()
        if result['code'] != 200:
            print('Error return {} when try to post=> {}'.format(result,params,url))
        else:
            return result


    def sample_get_request(self, url, header):
        r = requests.get(url,headers=header)
        try:
            result = r.json()
            return result
        except UnicodeDecodeError:
            print("字符转码错误"+r.text)