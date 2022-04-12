#############################
STARS メール送信クライアント
2010-06-08 Takashi Kosuge
#############################

このSTARSクライアントプログラムはコマンドによりメールを送信するクライアントプログラムです。

[設定]
各種設定は config.pl ファイルを編集する事により行います。
以下を自分の環境に合わせて設定します。

$::SMTPSERVER = 'smtpserver';
$::LOCALHOST  = 'myhostname';



[hello, help, getversionコマンド]
一般的な STARS Client 同様 hello, help, getversion コマンドが存在します。

[SendMailコマンド]
SendMailコマンドを受け取るとメールの送信を行います。必ず "From:, To:"の指定は必要となり、以下のようなフォーマットになります。

Usage:
SendMail From: mail_from\nTo: mail_to\nSubject: subject\n本文

ここで"\n"は改行ではなく単に "\" と "n" の2文字です。

[例 stars.pmを使った場合]


#メールの内容を読み込み、改行文字を"\n"に変更してバッファに登録。
my $buf = '';
while(<DATA>){
	chomp;s/\r//;
	$buf .= "$_\\n";
}

#メールの送信
$::tak->Send("mailer SendMail $buf");

#以下はメールのデータ
__DATA__
From: takashi.kosuge@kek.jp
To: takashi.kosuge@kek.jp
Subject: Test
Hello, this is test.
Nice to meet you. I hope this program works well.
