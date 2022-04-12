#############################################
Syslogger
STARS システム Logger Client
2005-06-30 Takashi Kosuge
#############################################

概要:
 本クライアントはSTARSサーバに接続した後、STARSサーバから送られてくる文字をログファイルに書き込んでゆくだけのSTARS Clientです。
将来 STARS Serverの改良後にはsysloggerという名前で接続するようになる予定ですが、現在の段階では "Debugger" というクライアント名を使用してSTARS Serverと接続します。そのためキーファイルとしてはDebugger.keyを使うこととなります。

本クライアントが起動すると、STARS Serverが他のクライアントに送るメッセージすべてをログに残す事ができます。

実際の起動は以下のようになります。

perl syslogger localhost
#localhost上のSTARSサーバへ接続

また、デバッグツールとしても有効で、-e オプションを付けて起動するとSTARS Server からのメッセージがスクリーンへ出力されます。この時 -nolog オプションを付加すれば、ログファイルへの出力を抑制しますので、単純なデバッグツールとして使用可能です。

例, perl syslogger -e -nolog localhost

さらに、UNIX系のシステムならばgrepなどを併用するのもgoodでしょう。
その他簡単な使い方については
perl syslogger -h
としてください。


なお、使用の際には"Time::HiRes"モジュールがあらかじめインストールされている必要があります。
