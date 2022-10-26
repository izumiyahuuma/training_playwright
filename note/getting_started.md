Getting Started の所のメモ書き
https://playwright.dev/python/docs/intro

# Writing Tests

テストで使う構文の種類として紹介されているのは3つ  
- Assertions
  - `expect` で記載する。期待する条件になるまで勝手に待ってくれるのが他との違い
- Locators
  - 要素のある場所を示しているオブジェクト?
- Selectors
  - Locators作成に利用されるもの。要素の場所を示す文字列

## Test Isolation
一つ一つのテストは分離されていて、別々のブラウザで動いているようなテストになるとか。

## Using Test Hooks
`fixtures`というアノテーションを使ってやることでテスト前後に処理を挟むことが可能。

# Test Generator(※割と重要)
以下のようにコマンドを実行するとブラウザが立ち上がって、操作した通りに自動的にテストケースを生成してくれる。  
```shell script
playwright codegen playwright.dev
```

# Trace Viewer
playwrightがどのような画面遷移をしたのかトレースしてくれるGUIツールもあるとか。
トレース例は以下の通り。 `trace.zip`として保存してくれる。

```python
browser = chromium.launch()
context = browser.new_context()

# Start tracing before creating / navigating a page.
context.tracing.start(screenshots=True, snapshots=True, sources=True)

page.goto("https://playwright.dev")

# Stop tracing and export it into a zip archive.
context.tracing.stop(path = "trace.zip")
```

トレースした結果を確認したいときはそれ用のコマンドを叩くとブラウザが立ち上がってGIUベースで見れる。
```shell script
playwright show-trace trace.zip
```