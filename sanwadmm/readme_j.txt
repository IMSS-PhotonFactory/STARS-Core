#############################
sanwa �f�W�^���}���`���[�^ PC �V���[�Y STARS I/O Client
2011-02-15 Takashi Kosuge
#############################

.[�͂��߂�]
����STARS I/O Client�� RS232C�̃I�v�V�����𑕒����� sanwa �f�W�^���}���`���[�^(�ȉ�DMM) PC101����f�[�^��ǂݍ��ނ��߂̂��̂ł��B�Ȃ��ANPort�����g�p���Đڑ����鎖��O��Ƃ��Ă��܂��B

�{ I/O Client �� PC101(���\�Â�)�p�ɂȂ��Ă��܂����A�f�[�^��

DCV, 0.223E-1
DCV, 0.311E-1
     :
     :

�̂悤�Ȍ`�Ő��ꗬ���ő����Ă���̂Ȃ�΁A���̋@��ł����p�\���Ǝv���܂��B
�Ȃ��APC20����LCD�\���Z�O�����g�̏����o�C�i���[�f�[�^�ő��M���Ă���悤�ł��̂ŗ��p�s�ł��B
�@��Ǝ��@������ΑΉ��������Ǝv���Ă��܂��B

���ʏ�̓I�[�g�p���[�Z�[�u�������Ă��܂��܂��̂ŁA�����Ԃ̋L�^���s���ۂɂ�DMM�̍���� "��>�b" �{�^�����������܂ܓd�������āA3�b��Ƀ{�^��������悤�ɂ��ăI�[�g�p���[�Z�[�u���������Ďg���Ƃ悢�ł��B


.[�ݒ�]
�e��ݒ�� config.pl �t�@�C����ҏW���鎖�ɂ��s���܂��B
�ȉ��������̊��ɍ��킹�Đݒ肵�܂��B

#STARS�T�[�o�̃z�X�g��
$::Server = 'localhost';

## For NPORT interface
$::NPORT_HOST  = '192.168.11.166'; #NPort host name.
$::NPORT_PORT  = 4001;             #NPort port number.

�Ȃ��A������PC101��ڑ����邽�߂ɂ͂��ꂼ��I/O�N���C�A���g���̐ݒ�������K�v������܂��B

if(
$::NodeName eq 'sanwadmm'
){###############################################################################

  :
 1��ڂ̐ݒ�
  :

}elsif(
$::NodeName eq 'sanwadmm2'
){###############################################################################

  :
 2��ڂ̐ݒ�
  :

}else{
	die "Bad node name.";
}

�̂悤�ɂ��� config.pl ��2��ڈȍ~�̐ݒ��ǉ����Ă��������B


.[�N��]
STARS�T�[�o���N�����Ă���K�v������܂��̂ŁA�ڑ����PC���STARS�T�[�o���N�����Ă��邱�Ƃ�\�ߊm�F���Ă����Ă��������B
����

perl sanwadmm sanwadmm
              ~~~~~~~�m�[�h��(�ȗ����� �m�[�h���Ƃ��� "sanwadmm" ���g�p�����)

�̂悤�ɂ����I/O�N���C�A���g���N�����܂��B



.[hello, help, getversion�R�}���h]
��ʓI�� STARS Client ���l hello, help, getversion �R�}���h�����݂��܂��B


.[GetValue]
DMM���ǂݎ�����f�[�^���擾���܂��B


.[GetFunction]
DMM�̌��݂̃��[�h���擾���܂��B�Ȃ��APC101�̏ꍇ�͈ȉ��̒ʂ�ł��B

DCV: �����d��
OHM: ��R
BUZ: ���ʃ`�F�b�N(�u�U�[)
CAP: �R���f���T�e��
FRQ: ���g��
DmA: �����d��(mA�����W)
DCA: ���������W(A�����W)


.[GetAvrgValue]
���͂̕��ϒl���擾���܂��B�Ȃ��A�擾�O�ɂ͗\�� ClearAvrg�� ���s���A���ς��邽�߂̉񐔕��f�[�^��ǂݎ������Ƀf�[�^���擾����悤�ɂ��܂��B�����A�f�[�^�̓��͂����ς̂��߂̉񐔂ɒB���Ă��Ȃ��ꍇ�́A

sanwadmm>term1 @GetAvrgValue Er: Data is not ready

�̂悤�ȃG���[��Ԃ��܂��B


.[ClearAvrg]
���ϒl�p�̃f�[�^�����Z�b�g���܂��B


.[GetAvrgCount]
���ς��s���f�[�^�̐���Ԃ��܂��B


.[SetAvrgCount]
���ς��s���f�[�^�̐���ݒ肵�܂��B�f�t�H���g��20�ł��B


.[IsAvrgReady]
���ς��s�����߂ɏ\���ȃf�[�^�����擾�ł��Ă��邩��Ԃ��܂��B0 �͎擾���A1 �͎擾�����������܂��B


.[_ChangedAvrgReady]
System��flgon�����Ă������Ƃ� ClearAvrg �R�}���h�Ȃǂŕ��ϒl�p�̃f�[�^�����Z�b�g���ꂽ�ꍇ�ɂ́A

_ChangedAvrgReady 0

���A�f�[�^�̎擾�����������ۂɂ�

_ChangedAvrgReady 1

�C�x���g���󂯎�鎖���ł��܂��B


.[��: telnet���g�����ꍇ(�m�[�h��term1�Őڑ�)]
#help�R�}���h
sanwadmm help
sanwadmm>term1 @help help hello getversion GetValue GetFunction GetAvrgValue Cle
arAvrg GetAvrgCount SetAvrgCount IsAvrgReady

#�f�[�^�̎擾�A�ʏ�͂��ꂾ����OK.
sanwadmm GetValue
sanwadmm>term1 @GetValue  0.167E-1


#���σf�[�^�̎擾
#���ω񐔂̐ݒ�A�f�t�H���g��20
sanwadmm SetAvrgCount 30
sanwadmm>term1 @SetAvrgCount 30 Ok:

#�V�X�e����"flgon"�𑗂蕽�ς̏I�������m�ł���悤�ɂ���B
System flgon sanwadmm
System>term1 @flgon Node sanwadmm has been registered.

#���σf�[�^�̃N���A
sanwadmm ClearAvrg
sanwadmm>term1 _ChangedAvrgReady 0
sanwadmm>term1 @ClearAvrg Ok:

#�f�[�^�������ł���܂ő҂��A���̌�f�[�^���擾����B
sanwadmm>term1 _ChangedAvrgReady 1
sanwadmm GetAvrgValue
sanwadmm>term1 @GetAvrgValue 1.096E-002

