STARSクライアントプログラム「PF-AR Ring情報参照クライアント」の使い方

■プログラムについて
○STARSをベースとしたプログラムで、STARSコマンドの送受信でPF-AR Ringのビームプロファイル値を参照することができます。

--------------------------------------------------------------
■更新履歴
2016.04.12	初回版リリース

--------------------------------------------------------------
■ファイルリスト（Windows版）
RingEPFARStart.cmd	コマンドファイル
ringEPFAR.exe		実行ファイル
cshosts.csv		設定ファイル
RingAR.key		STARSノード名「RingAR」用KEYファイル
readme_ja.txt		説明ファイル（日本語）

--------------------------------------------------------------
■稼動環境
○当プログラムは
・Windows系OSで動作します。
・Linux OSについては、プログラムのコンパイルが必要となります。
これまで、Ubuntu/Cent OS/Scientific Linuxでの動作実績があります。
=>配布パッケージはWindows版のみとなっておりますので、Linux版をご希望の方はお問い合わせください。

○当プログラムの動作には、STARSサーバが必要です。
=>STARSサーバのインストール方法を知りたい方はお問い合わせください。

○当パッケージをインストールするPCに、KEK-LANのIPアドレスが割り振られている必要があります。
=>ルータを通してKEK-LANに接続している場合は、別パッケージを用意します。お問い合わせください。

○当パッケージのインストールPCで、ネットワークカードを２枚以上使用している場合
　KEK-LANのIPアドレスを割り振ってあるネットワークカードの使用優先順位を最優先にする必要があります。
＊優先順位は、WindowsのネットワークアダプタのTCP/IP(v4)の設定からたどってメトリック値を入力することで操作可能です。
　メトリック値は値が小さい方が優先高です。

--------------------------------------------------------------
■インストール方法（Windows版）
１．当パッケージ（Zipファイル）を解凍する。
　解凍フォルダ「RingARフォルダ」が作成されます。

２．解凍フォルダの下にSTARSキーファイル「RingAR.key」があるので、STARS Serverにコピーします。

３．（オプション）コマンドファイル「RingEPFARStart.cmd」を編集します。
　STARSサーバが当パッケージインストールPCと同じ場合は、３はスキップして終わりです。

　STARSサーバが別PCの場合は、ファイル「RingEPFARStart.cmd」をテキストエディタで開き、
　行「.\ringEPFAR.exe RingAR localhost」の「localhost」をSTARSサーバのIPアドレスに変更して保存します。

--------------------------------------------------------------
■実行方法
１．ファイル「RingEPFARStart.cmd」をクリックし実行する。
　STARS Serverに接続し、KEK-LAN上にあるPF-AR Ring情報サーバからRing情報の受信を開始します。
=>うまく動作しない場合はご連絡ください。

--------------------------------------------------------------
■STARSコマンドによる値取得方法

○Ringプロファイルノード名（STARSノード名がRingAR(デフォルト）の場合）
ビーム電流（mA）	RingAR.DCCT 
ビームエネルギー（GeV）	RingAR.Energy
ビーム寿命（min）	RingAR.Lifetime
平均真空度（Pa）	RingAR.Vacuum
運転モード		RingAR.Status (0:Shutdown,1:Storage,2:Injection,3:Accelerate/Decelarate,4:User)
メッセージ		RingAR.Message

上記のノード名に対し、GetValueコマンドで値を取得します。
例）STARSノード名「term1」で実行する場合
ビーム電流（mA）の場合ですと、
（送信）RingAR.DCCT GetValue
（受信）RingAR.DCCT>term1 @GetValue 49.982324

あるいは上記のノード名に対し、イベント_ChangedValueで値を取得します。
例）STARSノード名「term1」で実行する場合
運転モードの場合ですと、
（送信）System flgon RingAR.Status
（受信）RingAR.Status>term1 _ChangedValue 4
（受信）RingAR.Status>term1 _ChangedValue 1
--------------------------------------------------------------
以上です。