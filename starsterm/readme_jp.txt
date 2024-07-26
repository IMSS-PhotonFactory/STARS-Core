###################################
STARS ターミナル Client (starsterm)
###################################

STARSのClient開発時など、簡単にSTARSサーバに接続するにはTelnetなどが大変便利ですが、Windowsではデフォルトで機能が有効になっていません。また、Linuxでもインストールされていない場合があります。
「STARS ターミナル Client (starsterm)」を使うと、telnetが無くてもSTARSサーバに接続してテキストメッセージの送受を行えるようになります。


[インストール]
starstermのディレクトリごと、適当なところにコピーしてください。


[実行]
python3 starsterm.py (環境によっては python starsterm.py)
とするとプログラムが実行されます。

ノード名とキーワードを聞いてきますので、入力します。
--------------------------
STARS terminal client Ver. 1.0
Nodename: term1
Keyword: stars
Connected.
Enter STARS messge. (Eenter ">h" if you need help.)
--------------------------

このあと、文字列を入力し<Enter>を押せばその文字列がSTARSサーバに送信されます。
あらかじめstarsterm.keyのようなキーワードファイルを用意しておけば(STARS Serverのtakaserv-lib配下にコピーする事を忘れずに)、以下のように入力する事でも実行が可能です。

--------------------------
$ python3 starsterm.py starsterm
STARS terminal client Ver. 1.0
Connected.
Enter STARS messge. (Eenter ">h" if you need help.)
--------------------------


[終了]
quit
と入力してください。STARS Serverとの接続が切れます。その後Enterを押してください。

--------------------------
quit

!!cb_handler() got Lost connection.
Press enter.

quit
!!Callback stopped!!
Bye.
--------------------------

[helpの表示]
python3 starsterm.py -h
あるいは
python3 starsterm.py --help
としてください。簡単なhelpが表示されます。


[ショートカット]
">"から始まる文字列を入力するとショートカットが呼び出されます。
また、">h"と入力するとショートカット一覧が表示されます。

--------------------------
>h
* The message will be sent to STARS server.
* Previous message will be sent if press just <Enter> key.
* ">string [param(s)_$1..$9]" calls shortcut.
== Short cuts ==
>l          System listnodes
>fon        System flgon $1
>foff       System flgoff $1
>g          $1 GetValue
--------------------------

例えば ">l" と入力すると "System listnodes" がSTARS Serverに送られます。
なお、">文字列 パラメータ1 パラメータ2 .... のように入力すると、各パラメータはリスト中の "$番号" ($1～$9が利用可)と置き換えられます。

>fon testdev
と入力すると
System flgon testdev
に変換されてSTARSサーバに送信されます。

ショートカットの追加等は、設定ファイルstarsterm.cfgの[commands]の下を書き換えることで可能です。


[同じ文字列の再送信]
文字列を入力せず、単にEnterキーを押すと、前回STARS Serverに送った文字列が再送されます。
(">h"を入力しhelpを見ると、前に送った内容はクリアされます)


[サーバ及びポートの指定]
サーバ名およびポート番号のデフォルトは starsterm.cfg 内に
starsserver = localhost
starsport   = 6057
のように記述されていますので変更の際はここを書き変えます。なお、プログラム起動時に "-s SERVER" や "-p PORT" とオプションを付ける事で一時的に変更する事が可能です。

