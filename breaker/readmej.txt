�T�Dbreaker�v���O�������A�b�v�O���[�h���鎞�̒���
�@breaker�Ŏg�p���Ă���stars.pm��DoEvents�Ή��̂��̂ł��B
�@stars.pm�̒u���������ɂ͂����ӂ��������B

�U�Dbreaker�̎��s�C���[�W

�P�Dbreaker�̏���

=>'term2'����breaker��ݒ肷��

�����s����R�}���h��
breaker setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken
breaker listcmd

�����s���� from syslogger��
=>'term2'��disconnet�����Ƃ��Ɏ��s�����R�}���h��ݒ肷��
=>�R�}���h����������ꍇ�̋�؂蕶����'\t'�������{����tab���g��
term2>breaker setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken
System>breaker @flgon Node term2 has been registered.
breaker>term2 @setcmd pm16c04.th Stop\tpm16c04.dth1 Stop\tterm1 _term2 broken Ok:

=>'term2'��disconnet�����Ƃ��Ɏ��s�����R�}���h���m�F����B
term2>breaker listcmd
=>�R�}���h����������ꍇ�̋�؂蕶���͖{����tab���g���Ă���
breaker>term2 @listcmd pm16c04.th Stop	pm16c04.dth1 Stop	term1 _term2 broken

=>���ł�'term1'�����term2���ݒ肵��breaker�R�}���h�̓��e���m�F���Ă݂�
breaker listcmd term2
breaker>term1 @listcmd term2 pm16c04.th Stop	pm16c04.dth1 Stop	term1 _term2 broken

�Q�Dpm16c04�𑀍�i�X�N���v�g�R�}���h�̎��s��z��j

=>'term2'����pm16c04�𑀍삷��
System flgon pm16c04.th
System flgon pm16c04.dth1
pm16c04.th SetValue 1000000
pm16c04.dth1 SetValue 1000000

�����s���� from syslogger��
System>term2 @flgon Node pm16c04.th has been registered.
System>term2 @flgon Node pm16c04.dth1 has been registered.
term2>pm16c04.th SetValue 1000000
term2>pm16c04.dth1 SetValue 1000000
pm16c04.th>term2 _ChangedIsBusy 1
pm16c04.th>term2 @SetValue 1000000 Ok:
pm16c04.dth1>term2 _ChangedIsBusy 1
pm16c04.dth1>term2 @SetValue 1000000 Ok:
pm16c04.th>term2 _ChangedValue 30572
pm16c04.dth1>term2 _ChangedValue 12606
�D�D�D

�V�D'term2'��ؒf����Bbreaker����������B

�����s���� from syslogger��
term2>breaker _Disconnected
=>breaker�ɐݒ肵���R�}���h�����s���čŌ��flgoff����
breaker>pm16c04.th Stop
pm16c04.th>breaker @Stop Ok:
breaker>pm16c04.dth1 Stop
pm16c04.dth1>breaker @Stop Ok:
breaker>term1 _term2 broken
System>breaker @flgoff Node term2 has been removed.
=>�ڌ���pm16c04��th��dth1����~�����̂��m�F�����B
=>term1�ł̃C�x���g���b�Z�[�W�̎�M���m�F�����B

�W�Dbreaker�̎��s���ʂ��m�F����B

�����s���� from syslogger��
=>'term1'����breaker�̎��s���ʂ��݂�B
term1>breaker listlog term2
breaker>term1 @listlog term2 pm16c04.th Stop	pm16c04.th>breaker @Stop Ok:	pm16c04.dth1 Stop	pm16c04.dth1>breaker @Stop Ok:	term1 _term2 broken
=>���Ȃ݂�'term2'��breaker�ւ̐ݒ���e�͊��ɃN���A����Ă���B
term1>breaker listcmd term2
breaker>term1 @listcmd term2 Er: No list.

�ȏ�ł��B