from .ids import IDSSession
from typing import List, Any, Optional, Dict

LOGIN_URL = 'http://ehall.xidian.edu.cn/login?service=http://ehall.xidian.edu.cn/new/index.html'
APP_LIST_URL = 'http://ehall.xidian.edu.cn/jsonp/serviceSearchCustom.json'
USE_APP_URL = 'http://ehall.xidian.edu.cn/appShow'
FAVORITE_URL = 'http://ehall.xidian.edu.cn/jsonp/userFavoriteApps.json'


class EhallSession(IDSSession):
    """
    一站式服务平台
    
    """
    async def login(self, username: str, password: str,) -> None:
        """
        登录到一站式服务平台

        `username`: 统一认证平台用户名
        
        `password`: 统一认证平台密码

        """
        await super(EhallSession, self).login(LOGIN_URL, username, password, )

    async def use_app(self, app_id: int) -> None:

        """

        使用一个应用

        """
        await self.get(APP_LIST_URL, params={
            'appId': app_id
        }, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/webp,image/apng,*/*;q=0.8",
        })

    async def get_app_list(self, search_key: str = '') -> List[Dict[str, Any]]:
        """
        获取应用列表

        `search_key`: 搜索关键字，默认为''
        """
        app_list = await self.get(APP_LIST_URL, params={
            'searchKey': search_key,
            'pageNumber': 1,
            'pageSize': 150,
            'sortKey': 'recentUseCount',
            'orderKey': 'desc'
        })
        app_list = await app_list.json()
        assert app_list['hasLogin']
        return app_list['data']

    async def get_app_id(self, search_key:str) -> Optional[str]:
        """
        获取应用的ID
        """
        search_result = await self.get_app_list(search_key)
        if len(search_result) == 0:
            return None
        if len(search_result) > 1:
            pass
        return search_result[0]['appId']

    async def is_logged_in(self) -> bool:
        async with self.get(FAVORITE_URL) as response:
            data = await response.json()
            return data['hasLogin']
