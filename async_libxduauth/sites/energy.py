from aiohttp import ClientSession


class EnergySession(ClientSession):
    """
    水表/电表查询平台
    """

    BASE = 'http://10.168.55.50:8088'

    async def login(self, username: str, password: str,):
        """
        
        `username`: 电费账号

        `password`: 密码
        """
        await self.get(self.BASE + "/searchWap/Login.aspx")
        await self.post(
            self.BASE + "/ajaxpro/SearchWap_Login,App_Web_fghipt60.ashx",
            json={
                "webName": username,
                "webPass": password
            }, headers={
                "AjaxPro-Method": "getLoginInput",
                'Origin': self.BASE
            }
        )
