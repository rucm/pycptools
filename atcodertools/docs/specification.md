# atcodertools 簡易仕様書

## 機能
* 問題サンプルのダウンロード
* サンプル検証
* 回答提出
* テンプレート出力（入力サポートは出来れば）
* 今回はＣ++のみの対応とする

## ファイル構成
|ファイル名|説明|
|:-|:-|
|`cli.py`|コマンドの定義を書き込むファイル。エントリーポイント|
|`service.py`|Atcoderにリクエストをしてデータを取得したり、認証とソースコードの提出を担う|
|`tester.py`|ダウンロードしたサンプルの検証とコードのコンパイル|
|`project.py`|コンテストの問題サンプルとソースコードをプロジェクトとして出力する|
|`problem.py`|データから問題を抽出する|

## コマンド一覧
|コマンド|説明|
|:-|:-|
|atcodertools create *[options] contest-id*|コンテストIDを指定してプロジェクトを作成する|
|atcodertools login *[options]*|認証情報を取得する|
|atcodertools test *[options] problem-id*|サンプルケースのテスト|
|atcodertools submit *[options] problem-id*|回答の提出|