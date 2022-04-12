-----------------------------------------------------------------------
Stars Interface ActiveX Control
2001-02-03  Takashi Kosuge
-----------------------------------------------------------------------

1. �T�v
Stars Interface ActiveX Control��Stars��Windows�A�v���P�[�V�����v���O�������ȒP�ɐڑ����邽�߂ɗ��p�\��ActiveX�R���g���[���ł��B

2. �C���X�g�[���y�ї��p
�p�b�P�[�W���ɂ���common\vb\starsinterface\Package����setup.exe���_�u���N���b�N���ăC���X�g�[�����܂��B�C���X�g�[���̏I�����Visual Basic�AMicrosoft Office��VBA�����痘�p���\�ł��B
Visual Basic����̗��p���ɂƂ�ƈȉ��̂悤�ɂȂ�܂��B

*�V�K�v���W�F�N�g�Łu�W�� EXE�v��I�ԁB
*�v���W�F�N�g���R���|�[�l���g�A�R���g���[���^�u��I�т܂��B
*StarsInterface���`�F�b�N���AOK�������܂��B
*�c�[���{�b�N�X��StarsInterface�R���g���[�����\�������̂ł��Ƃ�Form�ɓ\��t����Ɨ��p�ł��܂��B

�܂��A���ۂ̓���菇�͎��̒ʂ�ƂȂ�܂��B

���m�[�h���A�T�[�o�z�X�g���A�|�[�g�ԍ��AKey�t�@�C�������w�肵��Stars(TAK�T�[�o)�֐ڑ�����B(Connect���\�b�h)
��
�����̏ꍇ��Connected�C�x���g���A���s�����ꍇ��Error�C�x���g�������B
��
���b�Z�[�W�̑��M�A��M�B(Send���\�b�h�ɂă��b�Z�[�W���M�BCommandArrived�AReplyArrived�AEventArrived�C�x���g�͂��ꂼ��R�}���h�A���v���C�A�C�x���g�̃��b�Z�[�W�����������ɔ����B)
��
�ؒf(Disconect���\�b�h)

3. ���\�b�h
3.1 Connect���b�\�b�h
Usage:  object.Connect( Tname [, Rhost] [, Rport] [, Keyfile] )
Stars(TAK�T�[�o)�Ƃ̐ڑ����J�n���܂��B

Tname   ���m�[�h��(String)���w�肵�܂��B
Rhosts  �T�[�o�̃z�X�g��(String)���w�肵�܂��B�ȗ�����"localhost"���g�p����܂��B
Rport   Stars�̗��p����|�[�g�ԍ���Long�Ŏw�肵�܂��B�ȗ�����"6057"���g�p����܂��B
Keyfile �m�[�h�F�؂Ɏg�p���邽�߂̃L�[�t�@�C�������w�肵�܂��B�ȗ������"���m�[�h��+.key"�Ƃ����L�[�t�@�C�����̎g�p�����݂��܂��B

��: Rhost�ARport�AKeyfile���ȗ������ꍇ�B���ꂼ��"localhost"�A6057�A"Dev1.key"���g�p�����B
Private Sub Command1_Click()
    If StarsControl1.IsConnected = False Then
        StarsControl1.Connect ("Dev1")
    Else
        StarsControl1.Disconnect
    End If
End Sub

��: �S�Ă̈������w�肵���ꍇ�B
Private Sub Command1_Click()
    If StarsControl1.IsConnected = False Then
        StarsControl1.Connect ("Dev1", "rhost.domain", 6058, "c:\AllDev.key")
    Else
        StarsControl1.Disconnect
    End If
End Sub

3.2 Disconnect���\�b�h
Usage:  object.Disconnect()
�T�[�o�Ƃ̐ڑ���؂�܂��B

3.3 Send���\�b�h
Usage:  object.Send( Message [, TermTo] )
Stars�Ƀ��b�Z�[�W�𑗐M���܂��BTermTo���w�肷��Ƒ��M��m�[�h�������b�Z�[�W�̐擪�ɕt������܂��B���m�[�h����ݒ肷��K�v������ꍇ(bridge���Ƃ��ē��삳���邽�߂ɑ��M����"xxx.xxx"�̂悤�Ȍ`���Ŏ����ꍇ)��TermTo��ݒ肹����Message�̓��p�Łu���m�[�h���v�A�u���M��m�[�h���v���w�肵�܂��B

Message ���M���郁�b�Z�[�W
TermTo  �����m�[�h���B�w�肷���Message�̐擪�ɑ����m�[�h�����t������܂��B

��: TermTo���w�肵���ꍇ
Private Sub Command2_Click()
    StarsControl1.Send "Hello", "Term1"
End Sub

��: TermTo���ȗ������ꍇ
Private Sub Command2_Click()
    StarsControl1.Send "Term2>Term1 Hello"
End Sub

3.4 Sleep���\�b�h
Usage: object.Sleep(mileSeconds)
Stars�̒ʐM�Ƃ͊֌W����܂��񂪁A�V�X�e����mileSeconds�������b�N���邱�Ƃ��ł��܂��B

mileSecond  ��~���鎞�Ԃ��~���b�P�ʂ�Long�l�Őݒ肵�܂��B

4. �C�x���g
4.1 Connected�C�x���g
Usage: object_Connected(Message As String)
Stars�̐ڑ������������Connected�C�x���g���������܂��B�܂��AConnected���\�b�h�ȊO�ɂ�IsConnected�v���p�e�B�[�ɂ��ڑ��̊�����m�邱�Ƃ��ł��܂��B

Message  �ڑ������������Ƃ��̃��b�Z�[�W(String)���Z�b�g����܂��B

��: �ڑ�������������TAK�T�[�o���Ԃ��Ă��郁�b�Z�[�W��\���B
Private Sub StarsControl1_Connected(Message As String)
    Command1.Enabled = False
    MsgBox Message
End Sub


4.2 Disconnected�C�x���g
Usage: object_Disconnected()
�T�[�o����ڑ���ؒf���ꂽ�ꍇ�ɔ������܂��B

4.3 CommandArrived�C�x���g
Usage: object_CommandArrived(TermFrom As String, TermTo As String, Message As String)
�R�}���h���󂯎�����Ƃ��ɔ������܂��B

TermFrom  ���b�Z�[�W�𑗐M���Ă����m�[�h�����Z�b�g����܂��B
TermTo    ���b�Z�[�W�̂��Đ悪�Z�b�g����܂��B
Message   �R�}���h���b�Z�[�W���Z�b�g����܂��B

4.4 ReplyArrived�C�x���g
Usage: object_ReplyArrived(TermFrom As String, TermTo As String, Message As String)
���v���C���b�Z�[�W���󂯎�����ꍇ�ɔ������܂��B

TermFrom  ���b�Z�[�W�𑗐M���Ă����m�[�h�����Z�b�g����܂��B
TermTo    ���b�Z�[�W�̂��Đ悪�Z�b�g����܂��B
Message   ���v���C���b�Z�[�W���Z�b�g����܂��B�擪������"@"�ɂȂ��Ă��܂��B

4.5 EventArrived�C�x���g
Usage: object_EventArrived(TermFrom As String, TermTo As String, Message As String)
�C�x���g���b�Z�[�W���󂯎�����ꍇ�ɔ������܂��B

TermFrom  ���b�Z�[�W�𑗐M���Ă����m�[�h�����Z�b�g����܂��B
TermTo    ���b�Z�[�W�̂��Đ悪�Z�b�g����܂��B
Message   �C�x���g���b�Z�[�W���Z�b�g����܂��B�擪������"_"�ɂȂ��Ă��܂��B

4.6 Error�C�x���g
Usage: object_Error(Message As String)
�ڑ������s�����ꍇ�ɔ������܂��B

Message   �G���[���b�Z�[�W���Z�b�g����܂��B

5. �v���p�e�B�[
5.1 IsConnected�v���p�e�B�[
Usage: object.IsConneted
���݁AStars�ɐڑ����ł��邩�ǂ�����Boolean�ŕԂ��܂��B�ڑ����̏ꍇ��True�A�����łȂ��ꍇ��False��Ԃ��܂��B

��:

5.2 Port�v���p�e�B�[
Usage: object.Port
�ڑ��Ɏg�p���Ă���|�[�g�ԍ���Long�ŕԂ��܂��B
