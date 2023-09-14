import hashlib
from datetime import datetime
from aiohttp import ClientSession
from typing import Dict, Any
from ..utils.rsa import rsa_encrypt_by_pkcs1
import importlib.resources as res


class SportsSession(ClientSession):

    """
        体适能平台

    """

    BASE_URL = 'http://xd.5itsn.com//app/'

    __RSA_PUBLIC_KEY = res.files('async_libxduauth').joinpath(
        'sites/pub.pem').read_text()

    __COMMON_HEADERS = {
        'channel': 'H5',
        'version': '99999',
        'type': '0'
    }
    __COMMON_SIGN_PARAMS = {
        'appId': '3685bc028aaf4e64ad6b5d2349d24ba8',
        'appSecret': 'e8167ef026cbc5e456ab837d9d6d9254'
    }

    user_id: str = ''

    def __get_sign(self, params: Dict[str, Any]) -> str:
        sorted_params = sorted(params.items())
        concated_params = '&'.join(
            ['{}={}'.format(entry[0], entry[1]) for entry in sorted_params])
        return hashlib.md5(concated_params.encode('utf-8')).hexdigest()

    def __append_payload_sign(self, payload: Dict[str, Any]):
        timestamp = int(datetime.now().timestamp() * 1000)
        payload['timestamp'] = timestamp
        sign_params = payload.copy()
        sign_params.update(self.__COMMON_SIGN_PARAMS)
        payload['sign'] = self.__get_sign(sign_params)

    async def post(self, url: str, data: Dict[str, Any]):

        payload = data.copy()
        self.__append_payload_sign(payload)

        return await super().post(url, data=payload, headers=self.__COMMON_HEADERS)

    async def login(self, username: str, password: str,) -> None:

        """

        `username`: 体适能平台用户名

        `password`: 体适能平台密码

        """

        login_response = await self.post(
            self.BASE_URL + 'h5/login', data={
                'uname': username,
                'pwd': rsa_encrypt_by_pkcs1(self.__RSA_PUBLIC_KEY, password)
            })
        login_response = await login_response.json()
        if login_response['returnCode'] != '200':
            raise ConnectionError('登录失败: ' + login_response['returnMsg'])

        self.user_id = login_response['data']['id']
        self.headers.update({
            'token': login_response['data']['token']
        })
