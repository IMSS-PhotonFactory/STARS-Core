# STARS over RS232C Bridge.

rs232br��RS232C���g�p����STARS���u���b�W���邽�߂̃N���C�A���g�ł��B



���O�ϊ�
from, to�̖��O�ϊ��͈ȉ��̂悤�ɍs���܂��B

[telnet���[�h]
�A�v���P�[�V������
           stbr1        stbr2 ($::TelnetNode) �V���A����
term1>stbr1.dev1   =>   stbr2.term1>dev1
stbr1.dev1>term1   <=   dev1>stbr2.term1


[telnet���[�h�ȊO]
           stbr1     �V���A����      stbr2
term1>stbr1.dev1 =>  term1>dev1   =>  stbr2.term1>dev1
stbr1.dev1>term1 <=  dev1>term1   <=  dev1>stbr2.term1

