Ⅰ．breakerプログラムをアップグレードする時の注意
　breakerで使用しているstars.pmはDoEvents対応のものです。
　stars.pmの置き換え時にはご注意ください。

Ⅱ．breakerの実行イメージ

１．breakerの準備

=>'term2'からbreakerを設定する

＜実行するコマンド＞
breaker setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken
breaker listcmd

＜実行結果 from syslogger＞
=>'term2'がdisconnetしたときに実行されるコマンドを設定する
=>コマンドが複数ある場合の区切り文字は'\t'文字か本当のtabを使う
term2>breaker setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken
System>breaker @flgon Node term2 has been registered.
breaker>term2 @setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken Ok:

=>'term2'がdisconnetしたときに実行されるコマンドを確認する。
term2>breaker listcmd
=>コマンドが複数ある場合の区切り文字は本当のtabを使っている
breaker>term2 @listcmd pm16c04.th Stop	pm16c04.dth1 Stop	term1 _term2 broken

=>ついでに'term1'からもterm2が設定したbreakerコマンドの内容を確認してみる
breaker listcmd term2
breaker>term1 @listcmd term2 pm16c04.th Stop	pm16c04.dth1 Stop	term1 _term2 broken

２．pm16c04を操作（スクリプトコマンドの実行を想定）

=>'term2'からpm16c04を操作する
System flgon pm16c04.th
System flgon pm16c04.dth1
pm16c04.th SetValue 1000000
pm16c04.dth1 SetValue 1000000

＜実行結果 from syslogger＞
System>term2 @flgon Node pm16c04.th has been registered.
System>term2 @flgon Node pm16c04.dth1 has been registered.
term2>pm16c04.th SetValue 1000000
term2>pm16c04.dth1 SetValue 1000000
pm16c04.th>term2 _ChangedIsBusy 1
pm16c04.th>term2 @SetValue 1000000 Ok:
pm16c04.dth1>term2 _ChangedIsBusy 1
pm16c04.dth1>term2 @SetValue 1000000 Ok:
pm16c04.th>term2 _ChangedValue 30572
pm16c04.dth1>term2 _ChangedValue 12606
．．．

Ⅲ．'term2'を切断する。breakerが発動する。

＜実行結果 from syslogger＞
term2>breaker _Disconnected
=>breakerに設定したコマンドを実行して最後にflgoffする
breaker>pm16c04.th Stop
pm16c04.th>breaker @Stop Ok:
breaker>pm16c04.dth1 Stop
pm16c04.dth1>breaker @Stop Ok:
breaker>term1 _term2 broken
System>breaker @flgoff Node term2 has been removed.
=>目検でpm16c04のthとdth1が停止したのを確認した。
=>term1でのイベントメッセージの受信を確認した。

Ⅳ．breakerの実行結果を確認する。

＜実行結果 from syslogger＞
=>'term1'からbreakerの実行結果をみる。
term1>breaker listlog term2
breaker>term1 @listlog term2 pm16c04.th Stop	pm16c04.th>breaker @Stop Ok:	pm16c04.dth1 Stop	pm16c04.dth1>breaker @Stop Ok:	term1 _term2 broken
=>ちなみに'term2'のbreakerへの設定内容は既にクリアされている。
term1>breaker listcmd term2
breaker>term1 @listcmd term2 Er: No list.

以上です。