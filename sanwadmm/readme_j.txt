#############################
sanwa デジタルマルチメータ PC シリーズ STARS I/O Client
2011-02-15 Takashi Kosuge
#############################

.[はじめに]
このSTARS I/O Clientは RS232Cのオプションを装着した sanwa デジタルマルチメータ(以下DMM) PC101からデータを読み込むためのものです。なお、NPort等を使用して接続する事を前提としています。

本 I/O Client は PC101(結構古い)用になっていますが、データが

DCV, 0.223E-1
DCV, 0.311E-1
     :
     :

のような形で垂れ流しで送られてくるのならば、他の機種でも利用可能だと思います。
なお、PC20等はLCD表示セグメントの情報をバイナリーデータで送信してくるようですので利用不可です。
機会と実機があれば対応したいと思っています。

※通常はオートパワーセーブが働いてしまいますので、長時間の記録を行う際にはDMMの左上の "○>｜" ボタンを押したまま電源を入れて、3秒後にボタンを放すようにしてオートパワーセーブを解除して使うとよいです。


.[設定]
各種設定は config.pl ファイルを編集する事により行います。
以下を自分の環境に合わせて設定します。

#STARSサーバのホスト名
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.166'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

なお、複数のPC101を接続するためにはそれぞれI/Oクライアント毎の設定を書く必要があります。

if(
$::NodeName eq 'sanwadmm'
){###############################################################################

  :
 1台目の設定
  :

}elsif(
$::NodeName eq 'sanwadmm2'
){###############################################################################

  :
 2台目の設定
  :

}else{
	die "Bad node name.";
}

のようにして config.pl に2台目以降の設定を追加してください。


.[起動]
STARSサーバが起動している必要がありますので、接続先のPC上でSTARSサーバが起動していることを予め確認しておいてください。
次に

perl sanwadmm sanwadmm
              ~~~~~~~ノード名(省略時は ノード名として "sanwadmm" が使用される)

のようにするとI/Oクライアントが起動します。



.[hello, help, getversionコマンド]
一般的な STARS Client 同様 hello, help, getversion コマンドが存在します。


.[GetValue]
DMMが読み取ったデータを取得します。


.[GetFunction]
DMMの現在のモードを取得します。なお、PC101の場合は以下の通りです。

DCV: 直流電圧
OHM: 抵抗
BUZ: 導通チェック(ブザー)
CAP: コンデンサ容量
FRQ: 周波数
DmA: 直流電流(mAレンジ)
DCA: 直流レンジ(Aレンジ)


.[GetAvrgValue]
入力の平均値を取得します。なお、取得前には予め ClearAvrgを 実行し、平均するための回数分データを読み取った後にデータを取得するようにします。もし、データの入力が平均のための回数に達していない場合は、

sanwadmm>term1 @GetAvrgValue Er: Data is not ready

のようなエラーを返します。


.[ClearAvrg]
平均値用のデータをリセットします。


.[GetAvrgCount]
平均を行うデータの数を返します。


.[SetAvrgCount]
平均を行うデータの数を設定します。デフォルトは20です。


.[IsAvrgReady]
平均を行うために十分なデータ数が取得できているかを返します。0 は取得中、1 は取得完了を示します。


.[_ChangedAvrgReady]
Systemにflgonをしておくことで ClearAvrg コマンドなどで平均値用のデータがリセットされた場合には、

_ChangedAvrgReady 0

が、データの取得が完了した際には

_ChangedAvrgReady 1

イベントを受け取る事ができます。


.[例: telnetを使った場合(ノード名term1で接続)]
#helpコマンド
sanwadmm help
sanwadmm>term1 @help help hello getversion GetValue GetFunction GetAvrgValue Cle
arAvrg GetAvrgCount SetAvrgCount IsAvrgReady

#データの取得、通常はこれだけでOK.
sanwadmm GetValue
sanwadmm>term1 @GetValue  0.167E-1


#平均データの取得
#平均回数の設定、デフォルトは20
sanwadmm SetAvrgCount 30
sanwadmm>term1 @SetAvrgCount 30 Ok:

#システムに"flgon"を送り平均の終了を検知できるようにする。
System flgon sanwadmm
System>term1 @flgon Node sanwadmm has been registered.

#平均データのクリア
sanwadmm ClearAvrg
sanwadmm>term1 _ChangedAvrgReady 0
sanwadmm>term1 @ClearAvrg Ok:

#データが準備できるまで待ち、その後データを取得する。
sanwadmm>term1 _ChangedAvrgReady 1
sanwadmm GetAvrgValue
sanwadmm>term1 @GetAvrgValue 1.096E-002

