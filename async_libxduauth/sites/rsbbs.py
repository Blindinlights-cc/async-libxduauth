from aiohttp import ClientSession


from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from ..utils.vocde import _process_vcode


class RSBBSSession(ClientSession):

    """
    睿思BBS

    """

    HOST = 'rsbbs.xidian.edu.cn'

    async def login(self, username, password):
        login = await self.get(f'http://{self.HOST}/member.php', params={
            'mod': 'logging',
            'action': 'login',
            'mobile': '2'
        })
        soup = BeautifulSoup(await login.text(), 'lxml')

        img = soup.find('img', {'class': 'seccodeimg'}
                        ).get('src')  # type: ignore

        reponse = await self.get(f'http://{self.HOST}/{img}', headers={
            'Referer': login.url
        })
        content = await reponse.read()
        content = BytesIO(content)
        img = _process_vcode(Image.open(
            content
        ))
        img.show()
        vcode = input('验证码：')
        hidden_inputs = {
            item.get('name'): item.get('value', '')
            for item in soup.findAll('input', type='hidden')
        }

        page = await self.post(
            f'http://{self.HOST}/' +
            soup.find('form', id='loginform').get('action'), data=dict(  # type: ignore
                hidden_inputs, **{
                    'username': username,
                    'password': password,
                    'questionid': '0',
                    'answer': '',
                    'seccodeverify': vcode,
                }
            )
        )
        if '欢迎您回来' not in await page.text():
            return await self.login(username, password)
        return

    async def is_loggedin(self):
        return (await self.get(f'http://{self.HOST}/home.php', params={
            'mod': 'space', 'do': 'profile'
        }, allow_redirects=False)).status != 302
