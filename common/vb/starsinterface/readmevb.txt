-----------------------------------------------------------------------
Stars Interface ActiveX Control
2001-02-03  Takashi Kosuge
-----------------------------------------------------------------------

1. 概要
Stars Interface ActiveX ControlはStarsにWindowsアプリケーションプログラムを簡単に接続するために利用可能なActiveXコントロールです。

2. インストール及び利用
パッケージ内にあるcommon\vb\starsinterface\Package内のsetup.exeをダブルクリックしてインストールします。インストールの終了後はVisual Basic、Microsoft OfficeのVBA等から利用が可能です。
Visual Basicからの利用を例にとると以下のようになります。

*新規プロジェクトで「標準 EXE」を選ぶ。
*プロジェクト→コンポーネント、コントロールタブを選びます。
*StarsInterfaceをチェックし、OKを押します。
*ツールボックスにStarsInterfaceコントロールが表示されるのであとはFormに貼り付けると利用できます。

また、実際の動作手順は次の通りとなります。

自ノード名、サーバホスト名、ポート番号、Keyファイル名を指定してStars(TAKサーバ)へ接続する。(Connectメソッド)
↓
成功の場合はConnectedイベントが、失敗した場合はErrorイベントが発生。
↓
メッセージの送信、受信。(Sendメソッドにてメッセージ送信。CommandArrived、ReplyArrived、EventArrivedイベントはそれぞれコマンド、リプライ、イベントのメッセージ到着した時に発生。)
↓
切断(Disconectメソッド)

3. メソッド
3.1 Connectメッソッド
Usage:  object.Connect( Tname [, Rhost] [, Rport] [, Keyfile] )
Stars(TAKサーバ)との接続を開始します。

Tname   自ノード名(String)を指定します。
Rhosts  サーバのホスト名(String)を指定します。省略時は"localhost"が使用されます。
Rport   Starsの利用するポート番号をLongで指定します。省略時は"6057"が使用されます。
Keyfile ノード認証に使用するためのキーファイル名を指定します。省略すると"自ノード名+.key"というキーファイル名の使用が試みられます。

例: Rhost、Rport、Keyfileを省略した場合。それぞれ"localhost"、6057、"Dev1.key"が使用される。
Private Sub Command1_Click()
    If StarsControl1.IsConnected = False Then
        StarsControl1.Connect ("Dev1")
    Else
        StarsControl1.Disconnect
    End If
End Sub

例: 全ての引数を指定した場合。
Private Sub Command1_Click()
    If StarsControl1.IsConnected = False Then
        StarsControl1.Connect ("Dev1", "rhost.domain", 6058, "c:\AllDev.key")
    Else
        StarsControl1.Disconnect
    End If
End Sub

3.2 Disconnectメソッド
Usage:  object.Disconnect()
サーバとの接続を切ります。

3.3 Sendメソッド
Usage:  object.Send( Message [, TermTo] )
Starsにメッセージを送信します。TermToを指定すると送信先ノード名がメッセージの先頭に付加されます。自ノード名を設定する必要がある場合(bridge等として動作させるために送信元を"xxx.xxx"のような形式で示す場合)はTermToを設定せずにMessageの内用で「自ノード名」、「送信先ノード名」を指定します。

Message 送信するメッセージ
TermTo  相手先ノード名。指定するとMessageの先頭に相手先ノード名が付加されます。

例: TermToを指定した場合
Private Sub Command2_Click()
    StarsControl1.Send "Hello", "Term1"
End Sub

例: TermToを省略した場合
Private Sub Command2_Click()
    StarsControl1.Send "Term2>Term1 Hello"
End Sub

3.4 Sleepメソッド
Usage: object.Sleep(mileSeconds)
Starsの通信とは関係ありませんが、システムをmileSecondsだけロックすることができます。

mileSecond  停止する時間をミリ秒単位のLong値で設定します。

4. イベント
4.1 Connectedイベント
Usage: object_Connected(Message As String)
Starsの接続が完了するとConnectedイベントが発生します。また、Connectedメソッド以外にもIsConnectedプロパティーにより接続の完了を知ることができます。

Message  接続が完了したときのメッセージ(String)がセットされます。

例: 接続が完了した時TAKサーバが返してくるメッセージを表示。
Private Sub StarsControl1_Connected(Message As String)
    Command1.Enabled = False
    MsgBox Message
End Sub


4.2 Disconnectedイベント
Usage: object_Disconnected()
サーバから接続を切断された場合に発生します。

4.3 CommandArrivedイベント
Usage: object_CommandArrived(TermFrom As String, TermTo As String, Message As String)
コマンドを受け取ったときに発生します。

TermFrom  メッセージを送信してきたノード名がセットされます。
TermTo    メッセージのあて先がセットされます。
Message   コマンドメッセージがセットされます。

4.4 ReplyArrivedイベント
Usage: object_ReplyArrived(TermFrom As String, TermTo As String, Message As String)
リプライメッセージを受け取った場合に発生します。

TermFrom  メッセージを送信してきたノード名がセットされます。
TermTo    メッセージのあて先がセットされます。
Message   リプライメッセージがセットされます。先頭文字は"@"になっています。

4.5 EventArrivedイベント
Usage: object_EventArrived(TermFrom As String, TermTo As String, Message As String)
イベントメッセージを受け取った場合に発生します。

TermFrom  メッセージを送信してきたノード名がセットされます。
TermTo    メッセージのあて先がセットされます。
Message   イベントメッセージがセットされます。先頭文字は"_"になっています。

4.6 Errorイベント
Usage: object_Error(Message As String)
接続が失敗した場合に発生します。

Message   エラーメッセージがセットされます。

5. プロパティー
5.1 IsConnectedプロパティー
Usage: object.IsConneted
現在、Starsに接続中であるかどうかをBooleanで返します。接続中の場合はTrue、そうでない場合はFalseを返します。

例:

5.2 Portプロパティー
Usage: object.Port
接続に使用しているポート番号をLongで返します。
