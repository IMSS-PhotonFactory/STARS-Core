《注意事項》
  CW/CCWソフトウェアリミットスイッチとバックラッシュについて

【はじめに】
  １．pm16c04(pm16c02)には、あらかじめPMC本体のメモリに登録しておいたCWとCCWの限界
　　　値（以下CW/CCW ソフトウェアリミットスイッチ）を参照して、パルスモータ駆動時に
　　　ソフトウェアリミットスイッチの値に達すると自動停止する機能があります。

  ２．pm16c04(pm16c02)には、あらかじめPMC本体のメモリに登録しておいたバックラッシュ
　　　補正値を参照して、自動的にバックラッシュを補正する機能があります。
　
  PM4C-05-AのPMC本体は、上記１および２の機能はサポートしていません。
  しかしながらPM4C-05-AのSTARS I/O Clientでは、PM16C04との使用上の互換性を維持する
　ため、上記１および２の機能の一部をサポートしています。
　以下サポート情報について記述します。
　
【CW/CCWのソフトウェアリミットスイッチについて】
　　A)Stars GUI Client「npm4cconfig」からCW/CCWのソフトウェアリミットスイッチ値を登
　　　録します。CW/CCWの設定可能な値は-8388607～8388607です。
      PM16C04のCW/CCWのソフトウェアリミットスイッチ値の登録と同様のイメージです。

　　B)本プログラムの下記のモータコマンドは、CW/CCWの限界値を参照します。
      PM16C04の動作をエミュレートしています。
　　　＜モータコマンド＞
　　　SetValue、SetValueREL、JogCw、JocCcw、Preset

    C)本プログラムの下記のモータコマンドは、CW/CCWの限界値の値を参照しません。
      PM16C04と動作が異なりますのでご注意ください。
　　　＜モータコマンド＞
　　　ScanCw、ScanCcw、ScanCwConst、ScanCcwConst、ScanCwHome、ScanCcwHome
  
【バックラッシュについて】
　　A)Stars GUI Client「npm4cconfig」からバックラッシュ補正値を登録します。
      PM16C04のバックラッシュ補正値の登録と同様のイメージです。

　　B)本プログラムの下記のモータコマンドは、バックラッシュ補正機能をサポートします。
      PM16C04の動作をエミュレートしています。
　　　＜モータコマンド＞
　　　SetValue、SetValueREL、JogCw、JocCcw

    C)本プログラムの下記のモータコマンドは、バックラッシュ補正機能をサポートしません。
　　　＜モータコマンド＞
　　　ScanCw、ScanCcw、ScanCwConst、ScanCcwConst、ScanCwHome、ScanCcwHome　　　
  
以上
