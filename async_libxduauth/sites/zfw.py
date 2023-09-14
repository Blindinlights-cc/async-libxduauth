import re

from bs4 import BeautifulSoup
from aiohttp import ClientSession


class ZFWSession(ClientSession):
    """
    校园网流量查询平台
    
    """
    BASE = 'https://zfw.xidian.edu.cn'

    async def login(self, username: str, password: str,):
        self.headers.update({
            'User-Agent': 'Mobile'
        })

        response = await self.get(self.BASE)
        text = await response.text()
        soup = BeautifulSoup(text, "lxml")
        vcv = soup.find('input', type='hidden').get('value')  # type: ignore

        response = await self.post(self.BASE + '/login', data={
            "LoginForm[username]": username,
            "LoginForm[password]": password,
            "_csrf": vcv,
            "login-button": ""
        })
        text = await response.text()

        error = re.findall(
            r'请修复以下错误<\/p><ul><li>(.*?)<',
            text
        )
        self.headers.pop('User-Agent')
        if len(error) > 0:
            raise ConnectionError(error[0])
