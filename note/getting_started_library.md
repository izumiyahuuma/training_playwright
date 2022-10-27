https://playwright.dev/python/docs/library

# Usage
`asyncio` と呼ばれる機構がPython10から追加されたみたい。
javascriptのasync,awaitっぽく書けるので、公式ではそっちの書き方をおすすめしている。

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```


