STARSクライアントプログラム「PF-AR Ring情報ビューワ」の使い方

■プログラムについて
○STARSをベースとしたPF-AR Ring情報表示用GUIプログラムで、Perl言語で記述されています。

--------------------------------------------------------------
■更新履歴
2016.04.12	初回版リリース 　　Ver 1.0

--------------------------------------------------------------
■ファイルリスト
pfarringdisplay		実行ファイル（Perl言語)
stars.pm		STARSライブラリファイル(Perl言語）
pfarringdisplay.key	STARSノード名「pfarringdisplay」用KEYファイル
readme_ja.txt		説明ファイル（日本語）

--------------------------------------------------------------
■稼動環境／条件
○当プログラムはLinux/Windows両OSに対応しています。

○当プログラムの動作には、STARSサーバが必要です。
=>STARSサーバのインストール方法を知りたい方はお問い合わせください。

○当プログラムの動作には、Perl（無料）が必要です。

○当プログラムは、PerlのTkモジュールを使用します。
=>Perl Tkモジュールのインストール方法がわからない場合はお問い合わせください。

○当プログラムは、STARSクライアントプログラム
・「PF-AR Ring情報参照クライアント」	（通称RingARプログラム）
あるいは
・「ID操作クライアント」		（通称idgatewayプログラム）
いずれかのプログラムから、PF-AR Ring情報を取得します。

--------------------------------------------------------------
■インストール方法
１．当パッケージ（tgzファイル/zipファイル）を解凍します。
　解凍フォルダ「pfarringdisplayフォルダ」が作成されます。

２．解凍フォルダの下にSTARSキーファイル「pfarringdisplay.key」があるので、STARS Serverにコピーします。

--------------------------------------------------------------
■実行方法
○起動コマンド

・「PF-AR Ring情報参照クライアント」	（通称RingARプログラム）から情報を取得する場合
 <perlの実行ファイル> pfarringdisplay -node pfarringdisplay -target RING -ring RingAR <STARSサーバのIPアドレスorホスト名>

・「ID操作クライアント」		（通称idgatewayプログラム）から情報を取得する場合
 <perlの実行ファイル> pfarringdisplay -node pfarringdisplay -target=IDGATEWAY <STARSサーバのIPアドレスorホスト名>


例）
【Windowsの場合】
コマンドプロンプトウィンドウを開いて以下のコマンドを実行します。
STARSサーバがlocalhostの場合
・「PF-AR Ring情報参照クライアント」	（通称RingAR）から情報を取得する場合
　perl.exe pfarringdisplay -node pfarringdisplay -target RING -ring RingAR localhost

・「ID操作クライアント」		（通称idgateway）から情報を取得する場合
  perl.exe pfarringdisplay -node pfarringdisplay -target=IDGATEWAY localhost

＊「perl.exe」に実行パスを通していない場合は、「perl.exe」をフルパスで指定してください。

【Linuxの場合】
ターミナルウィンドウから以下のコマンドを実行します。
STARSサーバがlocalhostの場合
・「PF-AR Ring情報参照クライアント」	（通称RingAR）から情報を取得する場合
   perl pfarringdisplay -node pfarringdisplay -target RING -ring RingAR localhost

・「ID操作クライアント」		（通称idgateway）から情報を取得する場合
   perl pfarringdisplay -node pfarringdisplay -target=IDGATEWAY localhost

=>うまく動作しない場合はご連絡ください。

--------------------------------------------------------------
以上です。
