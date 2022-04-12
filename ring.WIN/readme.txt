■インストール環境について

１．インストールPCから"ping spinet-m51.kek.jp"
 が通るかどうか確認してください。

２．インストールPCのネットワークアドレス
　PCがPF-KEK用のアドレスをお持ちの場合はそのままお進みください。
　おもちでない場合はルータの設定が必要になる場合がありますので
　制御Gまでご連絡ください。

３．インストールPCのFireWallの設定
　Firewallを導入されている場合、例外プログラムとして
 "ring-ar.exe"を許可するようにしてください。

４．インストールPCのネットワークが２枚ざしの場合
　PF-KEKのネットワークのメトリックを優先するよう設定して
　ください。

５．ring-arフォルダをインストールPCにコピーします。

■プログラム起動コマンド
　cd ring-arプログラムディレクトリ
　ring-ar.exe -myaddr:<起動PCの"PF-KEK用のアドレス">
(例）
 cd c:\stars\ring
 ring-ar.exe -myaddr:130.87.182.24

■Stars Command
Stars nodenameが"RingAR"の場合

対象		Stars Command
---------------------------------------
Ring Current:   RingAR.DCCT GetValue
Ring Lifetime:  RingAR.Lifetime GetValue
