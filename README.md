# pythonkuma

Simple Python wrapper for Uptime Kuma

[![build](https://github.com/tr4nt0r/pythonkuma/workflows/Build/badge.svg)](https://github.com/tr4nt0r/pythonkuma/actions)
[![codecov](https://codecov.io/gh/tr4nt0r/pythonkuma/graph/badge.svg?token=YmUNsziQH0)](https://codecov.io/gh/tr4nt0r/pythonkuma)
[![PyPI version](https://badge.fury.io/py/pythonkuma.svg)](https://badge.fury.io/py/pythonkuma)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pythonkuma?style=flat&label=pypi%20downloads)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub-Sponsor-blue?logo=github)](https://github.com/sponsors/tr4nt0r)

---

## 📖 Documentation

- **Full Documentation**: [https://tr4nt0r.github.io/pythonkuma](https://tr4nt0r.github.io/pythonkuma)
- **Source Code**: [https://github.com/tr4nt0r/pythonkuma](https://github.com/tr4nt0r/pythonkuma)

---

## 📦 Installation

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

---

## 🛠 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request.

Make sure to follow the [contributing guidelines](CONTRIBUTING.md).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❤️ Support

If you find this project useful, consider [buying me a coffee ☕](https://www.buymeacoffee.com/tr4nt0r) or [sponsoring me on GitHub](https://github.com/sponsors/tr4nt0r)!

---

## Credit

This library is a fork of **pyuptimekuma** by [@jayakornk](https://github.com/jayakornk)
