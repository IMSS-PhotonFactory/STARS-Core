# STARS over RS232C Bridge.

rs232brはRS232Cを使用してSTARSをブリッジするためのクライアントです。



名前変換
from, toの名前変換は以下のように行われます。

[telnetモード]
アプリケーション側
           stbr1        stbr2 ($::TelnetNode) シリアル部
term1>stbr1.dev1   =>   stbr2.term1>dev1
stbr1.dev1>term1   <=   dev1>stbr2.term1


[telnetモード以外]
           stbr1     シリアル部      stbr2
term1>stbr1.dev1 =>  term1>dev1   =>  stbr2.term1>dev1
stbr1.dev1>term1 <=  dev1>term1   <=  dev1>stbr2.term1

