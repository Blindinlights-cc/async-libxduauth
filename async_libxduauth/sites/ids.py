from bs4 import BeautifulSoup
from aiohttp import ClientSession
from ..utils.aes import aec_cbc_encrypt
LOGIN_URL = 'http://ids.xidian.edu.cn/authserver/login'
CHECK_CAPTCHA_URL = 'https://ids.xidian.edu.cn/authserver/checkNeedCaptcha.htl'
GET_CAPTCHA_URL = 'http://ids.xidian.edu.cn/authserver/getCaptcha.htl'


class IDSSession(ClientSession):
    """
    用于登录到 统一身份认证，继承自 `aiohttp.ClientSession`

    """
    async def login(self,
                    target_url: str,
                    username: str,
                    password: str,):
        """
        登录到 IDS

        `target_url`: 登录后跳转的地址，即要登录的服务

        `username`: 统一认证平台用户名
        
        `password`: 统一认证平台密码
        """
        response = await self.get(
            LOGIN_URL,
            params={
                'service': target_url,
                'type': 'userNameLogin'
            }
        )
        text = await response.text()
        vcode = None
        page = BeautifulSoup(text, 'lxml')
        form = page.findChild(attrs={'id': 'pwdFromId'})
        params = {
            item.get('name'): item.get('value', '')
            for item in form.findAll('input', type='hidden')  # type: ignore
        }
        salt = form.find('input', id='pwdEncryptSalt').get(  # type: ignore
            'value')
        await self.post(
            LOGIN_URL,
            params={'service': target_url},
            data=dict(params, **{
                'username': username,
                'password': aec_cbc_encrypt(password, str(salt)),
                'captcha': vcode,
                'rememberMe': 'true'
            })
        )
