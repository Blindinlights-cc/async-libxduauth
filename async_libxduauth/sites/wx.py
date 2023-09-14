import hashlib
import json
import random
import time

from aiohttp import ClientSession as Session
from typing import Any, Dict, Optional
Param = Dict[str, Any]


def _generate_uuid() -> str:
    a = [str(random.random())[2:10] for _ in range(2)]
    a = [a[i] + str(int(time.time() * 1000))[-10:] for i in range(2)]
    a = [hex(int(a[i]))[2:10] for i in range(2)]
    return "web" + a[0] + a[1]


class WXSession(Session):
    BASE = 'http://202.117.121.7:8080/'

    def _dump_sign(self, data: Param) -> str:
        key_list = list(data.keys())
        key_list.sort()
        s = ''
        for i in key_list:
            s += i + '=' + str(data[i]) + '&'
        s = s[:-1]
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    async def options(self, url: str):
        return await super().options(url, headers={
            'Access-Control-Request-Headers': 'content-type,token',
            'Access-Control-Request-Method': 'POST'
        })

    async def post(self, url: str,
                   data: Optional[Param] = None,
                   json: Optional[Param] = None,
                   headers: Optional[Param] = None,
                   param: Optional[Param] = None):
        await self.options(url)
        if param is not None:
            json = {
                'appKey': "GiITvn",
                'param': param,
                'secure': 0
            }
        if json is not None:
            json['time'] = int(time.time() * 1000)  # 先后顺序
            json['sign'] = self._dump_sign(json)  # 数据签名在生成时间戳之后
            if headers is None:
                headers = {}
            headers = dict(headers, **{
                'Content-Type': 'application/json;charset=UTF-8'
            })
        return await super().post(url, json=json, data=data, headers=headers)

    async def login(self, username: str, password: str):
        data = {
            'appKey': "GiITvn",
            'param': json.dumps({
                'userName': username,
                'password': password,
                'schoolId': 190,
                'uuId': _generate_uuid()
            }),
            'secure': 0
        }
        result = await self.post(
            self.BASE + 'baseCampus/login/login.do', json=data)
        result = await result.json()
        if result['isConfirm'] != 1:
            raise ConnectionError('登录失败')
        self.headers.update({
            'token': result['token'][0] + '_' + result['token'][1]
        })
