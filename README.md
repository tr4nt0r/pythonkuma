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

URL = "https://uptime.exampe.com"
API_KEY = "api_key"


async def main():

    async with aiohttp.ClientSession() as session:
        uptime_kuma = UptimeKuma(session, URL, API_KEY)
        response = await uptime_kuma.metrics()
        print(response)


asyncio.run(main())

```

## Credit

This library is a fork of **pyuptimekuma** by [@jayakornk](https://github.com/jayakornk)
