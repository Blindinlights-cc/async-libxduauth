from async_libxduauth import EhallSession
from dotenv import load_dotenv
import asyncio
import os
import sys
sys.path.append("..")
load_dotenv()
username = str(os.getenv('USERNAME'))
passwd = str(os.getenv('PASSWORD'))

print(username, passwd)


async def task():
    session = EhallSession()
    await session.login(username, passwd)
    res = await session.is_logged_in()
    print(res)
    await session.close()

asyncio.run(task())
