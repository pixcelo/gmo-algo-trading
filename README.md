# gmo-algo-trading

このプログラムは、指定されたフォルダ構造内の複数のCSVファイルを読み込んで、機械学習モデルの学習データとして利用できる形式に整形します。
データはpandasデータフレームに格納され、pickle形式で保存されます。新しいデータが追加されるたびに、プログラムを実行してデータを更新できます。

## プログラムの機能
1. pickleファイルが存在する場合、データフレームを読み込みます。存在しない場合、新しいデータフレームを作成します。
2. 指定されたフォルダ構造からCSVファイルを読み込みます。過去のデータも含めて追加できるように対応しています。
3. 読み込んだデータをデータフレームに追加し、重複を削除し、日時でソートします。
4. データフレームをpickle形式で保存します。

## 使用方法
1. プログラムの parent_folder 変数に、データが格納されている親フォルダのパスを指定します。
2. プログラムを実行します。データが更新されるたびに、プログラムを再実行してデータフレームを更新できます。

## 出力
プログラムの実行結果として、以下の情報が表示されます。

- 追加前後のデータフレームの形状（行数と列数）
- 追加前後のデータフレームのカラム名
- データフレームの先頭部分（head）

データフレームはpickle形式で保存され、後で読み込んで利用できます。

## 設定ファイル構成 config.ini
[login]
username = xxxx
password = xxxx

[DISCORD]
WEBHOOK_URL = xxxx

## dataフォルダ
dataフォルダにはヒストリカルデータがあります。

ヒストリカルデータをすべて結合するには、`combine_and_sort_csv_files.py`を使用します。