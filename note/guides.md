適当なページクローリングして出てきた要素から見ていくので順不同

# Browsers
https://playwright.dev/python/docs/browsers

## Managing browser binaries
`playwright install`するとデフォルトの位置にブラウザがダウンロードされるけど、  
環境変数を指定してやればその場所を変更することが可能。  
実行する時もその場所を指定しないといけないのでexportとかで環境変数に直で設定してあげるほうが楽かな。  
```shell
# ブラウザのinstall
pip install playwright
PLAYWRIGHT_BROWSERS_PATH=$HOME/pw-browsers python -m playwright install

# 実行
PLAYWRIGHT_BROWSERS_PATH=$HOME/pw-browsers python playwright_script.py
```

# Pages