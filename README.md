# pythonkuma
Simple Python wrapper for Uptime Kuma

## Installation

```shell
pip install pythonkuma
```

## Example

```python
import asyncio

import aiohttp

from pythonkuma import UptimeKuma

URL = ""
USERNAME = ""
PASSWORD = ""


async def main():

    async with aiohttp.ClientSession() as session:
        uptime_kuma = UptimeKuma(session, URL, USERNAME, PASSWORD)
        response = await uptime_kuma.async_get_monitors()
        print(response.data)


asyncio.run(main())

```

## Credit

This library is a fork of **pyuptimekuma** by [@jayakornk](https://github.com/jayakornk)
