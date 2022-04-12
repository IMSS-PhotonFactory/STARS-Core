if __name__ == "__main__":

    from singlestars import StarsInterface
    import sys
    import time

    """ 
    Sample usage of singlestars.py - focusing on stars callback which runs in the single thread.
        To connect to STARS Server, setup keyfiles below to STARS Server.
        [keyfiles]
             samplepyclient.key
    """
    starshost = 'localhost'
    starsnode1= 'samplepyclient';

    # Create stars instance
    st = StarsInterface(starsnode1, starshost)
    
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
    rt = st.act('System gettime')
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
    def sb_handler(mess, sock):
        global st
        try:
            sys.stdout.write('**Callback sb_handler(%s).**\n'%(mess))
            #!!Fatal error
            if mess == '':
                sys.stdout.write('!!sb_handler() got ' + st.getlasterrortext() + '\n')
                st.terminateMainloop()
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
                sendstr="@help hello help terminate"
            elif mess.message == 'terminate':
                st.terminateMainloop()
                sendstr="@terminate Ok:"
            else:
                sendstr='@' + mess.message + " Er: Bad command or parameter."
            st.send(mess.nodefrom,sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')
        else:
            to=mess.nodeto.replace(st.nodename+'.','')
            sendstr='@' + mess.message + " Er: %s is down."%(to)
            st.send(st.nodename, mess.nodefrom, sendstr)
            sys.stdout.write('Send:' + st.nodename + '>' + mess.nodefrom + ' ' + sendstr+'\n')

    #************************************************************
    # Interval function
    #************************************************************
    def sb_interval():
        global st
        ct=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        sys.stdout.write('**Interval sb_interval() called at '+ct+'.**\n')
        t = st.getintervaltime()
        if(t>=5):
            sys.stdout.write('Change intervaltime from %s to 1 seconds.\n' %(str(t)))
            st.setintervaltime(1)
        else:
            sys.stdout.write('Change intervaltime from %s to 5 seconds.\n' %(str(t)))
            st.setintervaltime(5)

    #Add callback handler
    rt = st.addcallback(sb_handler)
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)

    # Callback function 'sb_handler' called when receive detected.
    sys.stdout.write('Start Callback method in the single thread.\nWaiting STARS message from the other stars client.\n')
    sys.stdout.write("Try STARS command '"+starsnode1+" help'\n")
    sys.stdout.write("Try STARS command '"+starsnode1+" terminate' to term this client.\n")
    rt = st.Mainloop(sb_interval, 5)
    if(rt == False):
        sys.stdout.write(st.getlasterrortext()+'\n')
        sys.stdout.write('Bye.\n')
        exit(1)

    # Disconnect from STARS server
    st.removecallback()
    st.disconnect()
    sys.stdout.write('Bye.\n')
