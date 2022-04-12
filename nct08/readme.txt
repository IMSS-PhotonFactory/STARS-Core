--------------------------------------------------------------------------------------
■nct08プログラムが対応しているカウンタの機種名
ツジ電子製 8ch カウンタ NCT08-01、NCT08-01B、NCT08-02、NCT08-01A、CT(08|8|16|32|48|64)シリーズ
--------------------------------------------------------------------------------------
■マニュアル
ツジ電子製 8ch カウンタ NCT08-01、NCT08-01B、NCT08-02、NCT08-01A、CT(08|8|16|32|48|64)シリーズ
--------------------------------------------------------------------------------------
■更新履歴：
--------------------------------------------------------------------------------------
# 2016-04-18 Support Counter 8 -> 16,32 NCT08_PGM_VERSION:3
 Tsuji-Denshi CTカウンタシリーズ(8ch,16ch,32ch,48ch,64ch)に対応
--------------------------------------------------------------------------------------
# 2019-11-07 Support Enable/Disable monitoring status.
 プログラム内のカウンタの計測中／停止ステータス監視機能の有効化／無効化

* 有効化コマンド
nct08 SetInternalMonitorEnable 1
nct08>term1 @SetInternalMonitorEnable 1 Ok:

* 有効/無効問い合わせ:Get,Isどちらも可
* 有効の場合
nct08 IsInternalMonitorEnable
nct08>term1 @IsInternalMonitorEnable 1
nct08 GetInternalMonitorEnable
nct08>term1 @GetInternalMonitorEnable 1

* 無効化コマンド実行
nct08 SetInternalMonitorEnable 0
nct08>term1 @SetInternalMonitorEnable 0 Ok:

* 有効/無効問い合わせ:Get,Isどちらも可
#無効の場合
nct08 IsInternalMonitorEnable
nct08>term1 @IsInternalMonitorEnable 0
nct08 GetInternalMonitorEnable
nct08>term1 @GetInternalMonitorEnable 0
--------------------------------------------------------------------------------------
# 2020-02-12 The 'nct08' program merge with the 'nct08' program.
 カウンタプログラム'nct08'と統合化
--------------------------------------------------------------------------------------
■nct08プログラム導入時の稼働確認のお願い

 nct08プログラムを無事起動できましたら
 GetDeviceTypeコマンドを実行してください。
nct08プログラムが判定したカウンタの機種名が返されます。

 Starsノード名がnct08なら
=> nct08 GetDeviceType

もし、機種名がNCT08-01Bなら
=> nct08 @GetDeviceType NCT08-01B
と返されます。

nct08プログラムが返すカウンタの機種名と実際に接続している
カウンタ機器名があっているか確認してください。

万が一カウンタ機種名が異なっている場合は、nct08プログラムの
使用をやめ開発者までご連絡ください。
