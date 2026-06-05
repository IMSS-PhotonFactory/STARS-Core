Python版 STARS RS232 bridge 2026-06-04 T. Kosuge
================================================
rs232brpy はRS232C等を使用して2つのSTARS ServerをブリッジするためのPython版のクライアントです。
なお、Perl版の rs232br とも互換性があります。


接続の概要
----------
[STARS Server1]<-->[rs232brpy]<=>[Converter]<=Serial=>[Converter]<=>[rs232brpy]<-->[STARS Server2]

# <-->: TCP/IP接続
# <=>: ケーブル接続(USB,Ethernet)
# Serial: RS232、RS422、RS485等
# Comverter: USB/Serial変換やNPort(MOXA製)等

また、Perl版の rs232br とも互換性があるので、以下のような接続も可能です。

[STARS Server1]<-->[rs232br(python)]<=>[NPort]<=Serial=>[Converter]<=>[rs232brpy]<-->[STARS Server2]


セットアップと実行
------------------
実行にはPython3が必要です。それぞれのSTARS Serverが走るPCにこのディレクトリごとコピーしてください。
Python3 rs232brpy.py
とする事で実行されます。


Configファイルの内容
--------------------
rs232brpy.cfg が設定用のファイルとなります。適宜書き変えてください。


[main]
starsserver = localhost
mynodename  = rs232brpy
starsport   = 6057
keyfile     = rs232brpy.key
use_nport   = no             #yesとすると NPort(nportserv.py)が、noとするとシリアルポート(pfipyserial.py)が選択されます。

[serial]                     #シリアルポートを使用する場合の設定を記述します。
Device      = COM3
Speed       = 230400
Data        = 8
Parity      = No
Stop        = 1
XonXoff     = No
RtsCts      = No
DsrDtr      = No

[nport]                      #Nportを使用する場合の設定を記述します。
host        = 192.168.127.254
port        = 4001


更新履歴
--------
2026-06-02 (Tue) Version 1.0 作成。
