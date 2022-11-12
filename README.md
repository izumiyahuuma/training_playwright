# training_playwright

playwright勉強用のリポジトリ

## install

```shell
pipenv install
pipenv run playwright install webkit
```

## run

```shell
pipenv shell
# 阿部寛のサイトクローリング
cd my_src/abehiroshi
python abehiroshi.py

# 秋田県庁の入札サイトクローリング(/tmp/crawl配下に公告ファイルがダウンロードされる)
cd my_src/akita
python akita.py

```