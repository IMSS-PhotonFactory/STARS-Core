#############################
STARS ���[�����M�N���C�A���g
2010-06-08 Takashi Kosuge
#############################

����STARS�N���C�A���g�v���O�����̓R�}���h�ɂ�胁�[���𑗐M����N���C�A���g�v���O�����ł��B

[�ݒ�]
�e��ݒ�� config.pl �t�@�C����ҏW���鎖�ɂ��s���܂��B
�ȉ��������̊��ɍ��킹�Đݒ肵�܂��B

$::SMTPSERVER = 'smtpserver';
$::LOCALHOST  = 'myhostname';



[hello, help, getversion�R�}���h]
��ʓI�� STARS Client ���l hello, help, getversion �R�}���h�����݂��܂��B

[SendMail�R�}���h]
SendMail�R�}���h���󂯎��ƃ��[���̑��M���s���܂��B�K�� "From:, To:"�̎w��͕K�v�ƂȂ�A�ȉ��̂悤�ȃt�H�[�}�b�g�ɂȂ�܂��B

Usage:
SendMail From: mail_from\nTo: mail_to\nSubject: subject\n�{��

������"\n"�͉��s�ł͂Ȃ��P�� "\" �� "n" ��2�����ł��B

[�� stars.pm���g�����ꍇ]


#���[���̓��e��ǂݍ��݁A���s������"\n"�ɕύX���ăo�b�t�@�ɓo�^�B
my $buf = '';
while(<DATA>){
	chomp;s/\r//;
	$buf .= "$_\\n";
}

#���[���̑��M
$::tak->Send("mailer SendMail $buf");

#�ȉ��̓��[���̃f�[�^
__DATA__
From: takashi.kosuge@kek.jp
To: takashi.kosuge@kek.jp
Subject: Test
Hello, this is test.
Nice to meet you. I hope this program works well.
