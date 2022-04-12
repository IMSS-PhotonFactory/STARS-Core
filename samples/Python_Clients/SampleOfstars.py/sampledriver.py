if __name__ == "__main__":

    import stars
    import sys
    import time

    """ 
    Sample usage of stars.py - focusing on stars callback, error handling.
        To connect to STARS Server, setup keyfiles below to STARS Server.
        [keyfiles]
             samplepyclient.key
    """
    starshost = 'localhost'
    starsnode1= 'samplepyclient';

    # Create stars instance
    st = stars.StarsInterface(starsnode1, starshost)

    #Enable debug print
    #st.setdebug(True)

    # Connect to STARS server
    rt=st.connect()
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)

    # Send and receicve test
    sys.stdout.write('Send message to STARS server: System gettime\n')
    st.send('System gettime')
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

    #************************************************************
    # Callback function
    #************************************************************
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
        sendstr=''
        if(mess.nodeto == st.nodename):
            if mess.message == 'hello':
                sendstr="@hello nice to meet you."
            elif mess.message == 'help':
                sendstr="@help hello help"
            else:
                sendstr='@' + mess.message + " Er: Bad command or parameter."
            st.send(mess.nodefrom,sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')
        else:
            to=mess.nodeto.replace(st.nodename+'.','')
            sendstr='@' + mess.message + " Er: %s is down."%(to)
            st.send(st.nodename, mess.nodefrom, sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')


    # Start receive waiting thread
    # Callback function 'cb_handler' called when receive detected.
    st.start_cb_handler(cb_handler)

    sys.stdout.write('Callback started. Input quit to end.\n')
    sys.stdout.write("Try STARS command '"+starsnode1+" help' from the other stars client.\n")
    sys.stdout.write('Waiting message...\n')
    # Wait 0.5 seconds to make return value of iscallbackrunning() True
    time.sleep(0.5)
    while True:
        if(st.iscallbackrunning() == False):
            sys.stdout.write('!!Callback stopped!!\n')
            break
        sbuf=sys.stdin.readline().rstrip('\n')
        if sbuf == 'quit':
            break
        elif sbuf == 'test':
            st.send(st.nodename, '_Test!!')
    st.disconnect()
    sys.stdout.write('Bye.\n')
