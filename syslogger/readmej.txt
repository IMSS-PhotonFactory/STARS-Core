#############################################
Syslogger
STARS �V�X�e�� Logger Client
2005-06-30 Takashi Kosuge
#############################################

�T�v:
 �{�N���C�A���g��STARS�T�[�o�ɐڑ�������ASTARS�T�[�o���瑗���Ă��镶�������O�t�@�C���ɏ�������ł䂭������STARS Client�ł��B
���� STARS Server�̉��ǌ�ɂ�syslogger�Ƃ������O�Őڑ�����悤�ɂȂ�\��ł����A���݂̒i�K�ł� "Debugger" �Ƃ����N���C�A���g�����g�p����STARS Server�Ɛڑ����܂��B���̂��߃L�[�t�@�C���Ƃ��Ă�Debugger.key���g�����ƂƂȂ�܂��B

�{�N���C�A���g���N������ƁASTARS Server�����̃N���C�A���g�ɑ��郁�b�Z�[�W���ׂĂ����O�Ɏc�������ł��܂��B

���ۂ̋N���͈ȉ��̂悤�ɂȂ�܂��B

perl syslogger localhost
#localhost���STARS�T�[�o�֐ڑ�

�܂��A�f�o�b�O�c�[���Ƃ��Ă��L���ŁA-e �I�v�V������t���ċN�������STARS Server ����̃��b�Z�[�W���X�N���[���֏o�͂���܂��B���̎� -nolog �I�v�V������t������΁A���O�t�@�C���ւ̏o�͂�}�����܂��̂ŁA�P���ȃf�o�b�O�c�[���Ƃ��Ďg�p�\�ł��B

��, perl syslogger -e -nolog localhost

����ɁAUNIX�n�̃V�X�e���Ȃ��grep�Ȃǂ𕹗p����̂�good�ł��傤�B
���̑��ȒP�Ȏg�����ɂ��Ă�
perl syslogger -h
�Ƃ��Ă��������B


�Ȃ��A�g�p�̍ۂɂ�"Time::HiRes"���W���[�������炩���߃C���X�g�[������Ă���K�v������܂��B
