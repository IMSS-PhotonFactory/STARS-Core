STARS�N���C�A���g�v���O�����uPF Ring���Q�ƃN���C�A���g�v�̎g����

���v���O�����ɂ���
��STARS���x�[�X�Ƃ����v���O�����ŁASTARS�R�}���h�̑���M��PF-Ring�̃r�[���v���t�@�C���l���Q�Ƃ��邱�Ƃ��ł��܂��B

--------------------------------------------------------------
���X�V����
2016.04.12	����Ń����[�X

--------------------------------------------------------------
���t�@�C�����X�g�iWindows�Łj
RingEPFStart.cmd	�R�}���h�t�@�C��
ringEPF.exe		���s�t�@�C��
cshosts.csv		�ݒ�t�@�C��
Ring.key		STARS�m�[�h���uRing�v�pKEY�t�@�C��
readme_ja.txt		�����t�@�C���i���{��j

--------------------------------------------------------------
���ғ���
�����v���O������
�EWindows�nOS�œ��삵�܂��B
�ELinux OS�ɂ��ẮA�v���O�����̃R���p�C�����K�v�ƂȂ�܂��B
����܂ŁAUbuntu/Cent OS/Scientific Linux�ł̓�����т�����܂��B
=>�z�z�p�b�P�[�W��Windows�ł݂̂ƂȂ��Ă���܂��̂ŁALinux�ł�����]�̕��͂��₢���킹���������B

�����v���O�����̓���ɂ́ASTARS�T�[�o���K�v�ł��B
=>STARS�T�[�o�̃C���X�g�[�����@��m�肽�����͂��₢���킹���������B

�����p�b�P�[�W���C���X�g�[������PC�ɁAKEK-LAN��IP�A�h���X������U���Ă���K�v������܂��B
=>���[�^��ʂ���KEK-LAN�ɐڑ����Ă���ꍇ�́A�ʃp�b�P�[�W��p�ӂ��܂��B���₢���킹���������B

�����p�b�P�[�W�̃C���X�g�[��PC�ŁA�l�b�g���[�N�J�[�h���Q���ȏ�g�p���Ă���ꍇ
�@KEK-LAN��IP�A�h���X������U���Ă���l�b�g���[�N�J�[�h�̎g�p�D�揇�ʂ��ŗD��ɂ���K�v������܂��B
���D�揇�ʂ́AWindows�̃l�b�g���[�N�A�_�v�^��TCP/IP(v4)�̐ݒ肩�炽�ǂ��ă��g���b�N�l����͂��邱�Ƃő���\�ł��B
�@���g���b�N�l�͒l�������������D�捂�ł��B

--------------------------------------------------------------
���C���X�g�[�����@�iWindows�Łj
�P�D���p�b�P�[�W�iZip�t�@�C���j���𓀂���B
�@�𓀃t�H���_�uRing�t�H���_�v���쐬����܂��B

�Q�D�𓀃t�H���_�̉���STARS�L�[�t�@�C���uRing.key�v������̂ŁASTARS Server�ɃR�s�[���܂��B

�R�D�i�I�v�V�����j�R�}���h�t�@�C���uRingEPFStart.cmd�v��ҏW���܂��B
�@STARS�T�[�o�����p�b�P�[�W�C���X�g�[��PC�Ɠ����ꍇ�́A�R�̓X�L�b�v���ďI���ł��B

�@STARS�T�[�o����PC�̏ꍇ�́A�t�@�C���uRingEPFStart.cmd�v���e�L�X�g�G�f�B�^�ŊJ���A
�@�s�u.\ringEPF.exe Ring localhost�v�́ulocalhost�v��STARS�T�[�o��IP�A�h���X�ɕύX���ĕۑ����܂��B

--------------------------------------------------------------
�����s���@
�P�D�t�@�C���uRingEPFStart.cmd�v���N���b�N�����s���܂��B
�@STARS Server�ɐڑ����AKEK-LAN��ɂ���PF Ring���T�[�o����Ring���̎�M���J�n���܂��B
=>���܂����삵�Ȃ��ꍇ�͂��A�����������B

--------------------------------------------------------------
��STARS�R�}���h�ɂ��l�擾���@

��Ring�v���t�@�C���m�[�h���iSTARS�m�[�h����Ring(�f�t�H���g�j�̏ꍇ�j
�r�[���d���imA�j	Ring.DCCT 
�r�[���G�l���M�[�iGeV�j	Ring.Energy
�r�[�������imin�j	Ring.Lifetime
���ϐ^��x�iPa�j	Ring.Vacuum
�^�]���[�h		Ring.Status (0:Shutdown,1:Linac,2:Injection,3:Storage,4:User,5:User(Top-UP))
���b�Z�[�W		Ring.Message

��L�̃m�[�h���ɑ΂��AGetValue�R�}���h�Œl���擾���܂��B
��jSTARS�m�[�h���uterm1�v�Ŏ��s����ꍇ
�r�[���d���imA�j�̏ꍇ�ł��ƁA
�i���M�jRing.DCCT GetValue
�i��M�jRing.DCCT>term1 @GetValue 449.982324

���邢�͏�L�̃m�[�h���ɑ΂��A�C�x���g_ChangedValue�Œl���擾���܂��B
��jSTARS�m�[�h���uterm1�v�Ŏ��s����ꍇ
�^�]���[�h�̏ꍇ�ł��ƁA
�i���M�jSystem flgon Ring.Status
�i��M�jRing.Status>term1 _ChangedValue 5
�i��M�jRing.Status>term1 _ChangedValue 2
--------------------------------------------------------------
�ȏ�ł��B