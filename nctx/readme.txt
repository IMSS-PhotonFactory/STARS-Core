--------------------------------------------------------------------------------------
��nct08�v���O�������Ή����Ă���J�E���^�̋@�햼
�c�W�d�q�� 8ch �J�E���^ NCT08-01�ANCT08-01B�ANCT08-02�ANCT08-01A�ACT(08|8|16|32|48|64)�V���[�Y
--------------------------------------------------------------------------------------
���}�j���A��
�c�W�d�q�� 8ch �J�E���^ NCT08-01�ANCT08-01B�ANCT08-02�ANCT08-01A�ACT(08|8|16|32|48|64)�V���[�Y
--------------------------------------------------------------------------------------
���X�V�����F
--------------------------------------------------------------------------------------
# 2016-04-18 Support Counter 8 -> 16,32 NCT08_PGM_VERSION:3
 Tsuji-Denshi CT�J�E���^�V���[�Y(8ch,16ch,32ch,48ch,64ch)�ɑΉ�
--------------------------------------------------------------------------------------
# 2019-11-07 Support Enable/Disable monitoring status.
 �v���O�������̃J�E���^�̌v�����^��~�X�e�[�^�X�Ď��@�\�̗L�����^������

* �L�����R�}���h
nct08 SetInternalMonitorEnable 1
nct08>term1 @SetInternalMonitorEnable 1 Ok:

* �L��/�����₢���킹:Get,Is�ǂ������
* �L���̏ꍇ
nct08 IsInternalMonitorEnable
nct08>term1 @IsInternalMonitorEnable 1
nct08 GetInternalMonitorEnable
nct08>term1 @GetInternalMonitorEnable 1

* �������R�}���h���s
nct08 SetInternalMonitorEnable 0
nct08>term1 @SetInternalMonitorEnable 0 Ok:

* �L��/�����₢���킹:Get,Is�ǂ������
#�����̏ꍇ
nct08 IsInternalMonitorEnable
nct08>term1 @IsInternalMonitorEnable 0
nct08 GetInternalMonitorEnable
nct08>term1 @GetInternalMonitorEnable 0
--------------------------------------------------------------------------------------
# 2020-02-12 The 'nct08' program merge with the 'nct08' program.
 �J�E���^�v���O����'nct08'�Ɠ�����
--------------------------------------------------------------------------------------
��nct08�v���O�����������̉ғ��m�F�̂��肢

 nct08�v���O�����𖳎��N���ł��܂�����
 GetDeviceType�R�}���h�����s���Ă��������B
nct08�v���O���������肵���J�E���^�̋@�햼���Ԃ���܂��B

 Stars�m�[�h����nct08�Ȃ�
=> nct08 GetDeviceType

�����A�@�햼��NCT08-01B�Ȃ�
=> nct08 @GetDeviceType NCT08-01B
�ƕԂ���܂��B

nct08�v���O�������Ԃ��J�E���^�̋@�햼�Ǝ��ۂɐڑ����Ă���
�J�E���^�@�햼�������Ă��邩�m�F���Ă��������B

������J�E���^�@�햼���قȂ��Ă���ꍇ�́Anct08�v���O������
�g�p����ߊJ���҂܂ł��A�����������B
