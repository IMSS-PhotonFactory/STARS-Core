read me
※正式なマニュアルは別途作ります。申し訳ありません。
TPG361対応STARSクライアントプログラム
【準備】
デバイスとの接続はUSB Bインターフェイスを利用して行う。
linuxPCを利用する場合はsdevport、windowsPCならpcportにてTPC/IPソケットを利用したデバイスとの通信環境を整える。

##対応コマンド
STARS共通コマンド
-hello
-getversion
-listnodes
TPG361専用コマンド
-GetValue
-SetSwFunc(1|2|3|4)
-GetSwFunc(1|2|3|4)
-SAV
-UNI (mbar|Torr|Pa|Micron|hPa|Volt)
-UNI
-SPS

->GetValue
[Send message]
nodename GetValue
	-センサー1の真空値を出力
nodename.1 GetValue
	-センサー1の真空値を出力
nodename.2 GetValue
	-センサー2の真空値を出力
出力例)
tnodename>term1 @GetValue 5.6900E+02

*Error message
-Underrange
-Overrange
-Sensor error
-Sensor off
-No Sensor
-identification error

->SetSwFunc
nodename SetSwFunc1 任意の真空値
	-セットポイント1を任意の真空値へ変更
nodename SetSwFunc2 任意の真空値
	-セットポイント2を任意の真空値へ変更
nodename SetSwFunc3 任意の真空値
	-セットポイント3を任意の真空値へ変更
nodename SetSwFunc4 任意の真空値
	-セットポイント4を任意の真空値へ変更

->GetSwFunc
[Send message]
nodename GetSwFunc1
	-セットポイント1の設定値を出力
nodename GetSwFunc2
	-セットポイント2の設定値を出力
nodename GetSwFunc3
	-セットポイント3の設定値を出力
nodename GetSwFunc4
	-セットポイント4の設定値を出力

[receive message]
Turnedoff 設定値
Ternon 設定値
Measurment channel 1設定値
Measurment channel 2設定値

->SAV
[Send message]
nodename SAV
	-設定値等を保存する

->UNI
[Send message]
nodename UNI
	-現在のデータの単位を出力
nodename UNI mbar
	-データ単位をmbarに変更
nodename UNI Torr
	-データ単位をTorrに変更
nodename UNI Pa
	-データ単位をPaに変更
nodename UNI Micron
	-データ単位をMicronに変更
nodename UNI Volt
	-データ単位をVoltに変更

->SPS
[Send message]
nodename SPS
	-セットポイントが設定されているかどうかの状態を表示
1:設定あり
0:設定なし