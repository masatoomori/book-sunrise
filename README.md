# book-sunrise

サンライズ瀬戸・出雲の予約を簡便にするためのスクリプト。
事前に[予約サイト](https://www.jr-odekake.net/goyoyaku/campaign/sunriseseto_izumo/form.html)の[利用登録](https://www.jr-odekake.net/cjw/about/)と支払い方法の設定をしておく必要がある。

Chrome ブラウザで動作確認。

## 使い方

下記のコマンドを実行。

```bash
python book.py -u [ユーザ名] -p [パスワード]
```

設備選択画面まで自動で進むので、そこから先は手動で進める必要がある。
ブラウザが自動で閉じるまでの時間は 30分なので、それまでに予約を完了させること。
人数を確定させるまで席の確保はできていないので注意。

```python
SEC_FOR_MANUAL_OPERATION = 1800     # 条件検索以降はマニュアルで操作する
```

## オプションとデフォルト値

```python
$ python book.py -h

--userid USERID, -u USERID               : ユーザ名
--password PASSWORD, -p PASSWORD         : パスワード
--origin ORIGIN, -o ORIGIN               : 出発駅（デフォルトは東京）
--destination DESTINATION, -d DESTINATION: 到着駅（デフォルトは出雲市）
--interval_month INTERVAL_MONTH          : スクリプト実行日から何ヶ月後の予約か（デフォルトは1ヶ月後）
--interval_day INTERVAL_DAY              : スクリプト実行日から何日後の予約か（デフォルトは0日後、上記パラメータに加算される）
--departure_hour DEPARTURE_HOUR          : 出発時刻（デフォルトは20時）
--departure_minute DEPARTURE_MINUTE      : 出発時刻（デフォルトは0分）
--train_name TRAIN_NAME                  : 列車名（デフォルトはサンライズ出雲）
--cabin_class {1,2,3,4,5,6}              : 設備クラス（デフォルトは3）
```

## 設備クラスの説明

```python
CABIN_CHOICES = [
    1, # 普通車　ノビノビ座席
    2, # 1人用　A寝台個室　シングルデラックス
    3, # 1人用　B寝台個室　シングルツイン。平日は5分で禁煙完売するが、少し経つとキャンセルが出る。喫煙は15分くらい残っている。金曜日、土曜日は禁煙即完売
    4, # 1人用　B寝台個室　シングル
    5, # 1人用　B寝台個室　ソロ
    6, # 2人用　B寝台個室　サンライズツイン。10時で即完売
]
```
