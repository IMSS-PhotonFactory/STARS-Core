if __name__ == "__main__":

    import stars
    import sys
    import time

    """ 
    Sample usage of stars.py - focusing on stars connect method using keyword list.
        To connect to STARS Server, setup keyfiles below to STARS Server.
        [keyfiles]
             samplepyclient.key
             samplepyclientkeylist.key
    """
    starshost = 'localhost'
    starsnode1= 'samplepyclient';
    starsnode2= 'samplepyclientkeylist';

    #========================================
    sys.stdout.write('[Create stars instance]\n')
    #----------------------------------------
    st = stars.StarsInterface(starsnode1, starshost)

    #Enable debug print
    #st.setdebug(True)

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write("[Connect as %s using keyfile '%s']\n" %(starsnode1,starsnode1+'.key'))
    #----------------------------------------
    rt=st.connect()
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)
        
    sys.stdout.write('%s connected.\n' %(starsnode1))

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Check Send and Receive test]\n')
    #----------------------------------------
    sys.stdout.write('Send message to STARS server: System hello\n')
    st.send('System hello')
    rt = st.receive()
    if rt == '':
        rt = st.getlasterrortext()
        if(rt == 'Timeout'):
            sys.stdout.write('Timeout detected.\n')
        else:
            sys.stdout.write(st.getlasterrortext()+'\n')
            sys.stdout.write('Bye.\n')
            exit(1)
    else:
        sys.stdout.write('Reply message arrived from STARS server: %s.\n' %(rt))

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Disconnect]\n')
    #----------------------------------------

    st.disconnect()
    sys.stdout.write('%s disconnected.\n' %(starsnode1))

    #========================================
    sys.stdout.write('\n')
    st.nodename = starsnode2
    st.keywords = 'stars takashi kekpf hello'
    sys.stdout.write('[Connect as %s with keyword list(%s)]\n' %(st.nodename,st.keywords))
    #----------------------------------------
    rt=st.connect()
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)
        
    sys.stdout.write('%s connected.\n' %(starsnode2))
    
    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Check Send and Receive test]\n')
    #----------------------------------------
    sys.stdout.write('Send message to STARS server: System help\n')
    st.send('System help')
    rt = st.receive()
    if rt == '':
        rt = st.getlasterrortext()
        if(rt == 'Timeout'):
            sys.stdout.write('Timeout detected.\n')
        else:
            sys.stdout.write(st.getlasterrortext()+'\n')
            sys.stdout.write('Bye.\n')
            exit(1)
    else:
        sys.stdout.write('Reply message arrived from STARS server: %s.\n' %(rt))
        sys.stdout.write('\n')
        sys.stdout.write('STARS message: ' + rt.allmessage + '\n')
        for c in rt.parameters.split():
            sys.stdout.write('Command of System: ' + c + '\n')
        sys.stdout.write('Done.\n')

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Check receive timeout]\n')
    #----------------------------------------
    rt = st.receive(2)
    if rt == '':
        rt = st.getlasterrortext()
        if(rt == 'Timeout'):
            sys.stdout.write('Timeout detected.\n')
        else:
            sys.stdout.write(st.getlasterrortext()+'\n')
            sys.stdout.write('Bye.\n')
            exit(1)
    else:
        sys.stdout.write('Received %s.\n' %(rt))

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Callback Start]\n')
    #----------------------------------------
    def cb_handler(mess):
        global st
        try:
            sys.stdout.write('**Callback cb_handler(%s).**\n'%(mess))
            #!!Fatal error
            if mess == '':
                sys.stdout.write('!!cb_handler() got ' + st.getlasterrortext() + '\n')
                return
        except:
            return

        #Reply message
        if(mess.command.startswith('@')):
            return;

        #Event message
        if(mess.command.startswith('_')):
            return;

        #Command message
        sendstr=mess.nodeto+'>'+mess.nodefrom+' @'+mess.message
        sys.stdout.write(sendstr + '\n')
        st.send(sendstr)

    st.start_cb_handler(cb_handler)

    for i in range(1, 5):
        sys.stdout.write('Send event to myself.\n')
        st.send(st.nodename, '_Event!!:' + str(i))
        time.sleep(0.5)

    sys.stdout.write('Waiting message from the other stars client, press Enter to disconnect.\n')
    sys.stdin.readline().rstrip('\n')

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Disconnect]\n')
    #----------------------------------------
    st.disconnect()
    sys.stdout.write('%s disconnected.\n' %(starsnode1))

    #========================================
    sys.stdout.write('\n')
    sys.stdout.write('[Check read error after disconnect]\n')
    #----------------------------------------
    rt = st.receive(1)
    if rt == '':
        rt = st.getlasterrortext()
        if(rt == 'Timeout'):
            sys.stdout.write('Timeout detected.\n')
        else:
            sys.stdout.write(st.getlasterrortext()+'\n')
            sys.stdout.write('Bye.\n')
            exit(1)
    else:
        sys.stdout.write('Received %s.\n' %(rt))

    #========================================
    sys.stdout.write('Bye.\n')
