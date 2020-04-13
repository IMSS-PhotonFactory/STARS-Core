Sample program: 'sampledriver.py' and 'sampledriver2.py' can be used to test 'stars.py'.

    [sampledriver.py]
    The sample program trys to connect to the starsserver(=localhost) as the nodename 'samplepyclient'.
    This program focuses on stars callback, error handling.

    To change the starsserver host and stars nodename, please edit the lines 13-14.
        [sampledriver.py]
        starshost = 'localhost'
        starsnode1= 'samplepyclient';

    To connect to STARS Server, please setup the keyfiles to STARS Server.
        [keyfiles]
        samplepyclient.key

    [sampledriver2.py]
    The sample program trys to connect to the starsserver(=localhost) as the nodename 'samplepyclient' and 'samplepyclientkeylist'.
    This program focuses especially on stars connect method using keyword list(no use of keyfile).

    To change the starsserver host and stars nodename, please edit the lines 14-16.
        [sampledriver2.py]
        starshost = 'localhost'
        starsnode1= 'samplepyclient';
        starsnode2= 'samplepyclientkeylist';

    To connect to STARS Server, please setup the keyfiles to STARS Server.
        [keyfiles]
        samplepyclient.key
        samplepyclientkeylist.key

Tested:
    python 3.4.4 on Windows7 32bit
    python 2.7.12 on Linux "Ubuntu 16.04.1 LTS"

Execution examples:

    [sampledriver.py]

        $ python sampledriver.py
        Send message to STARS server: System gettime
        Reply message arrived from STARS server: System>samplepyclient @gettime 2017-02-17 14:43:03.
        Callback started. Input quit to end.
        Try STARS command 'samplepyclient help' from the other stars client.
        Waiting message...
        quit

        <The STARS messages between STARS node 'term1' and 'samplepyclient'>
        samplepyclient hello
        samplepyclient>term1 @hello nice to meet you.
        samplepyclient help
        samplepyclient>term1 @help hello help

    [sampledriver2.py]

        $ python sampledriver2.py
        [Create stars instance]

        [Connect as samplepyclient using keyfile 'samplepyclient.key']
        samplepyclient connected.

        [Check Send and Receive test]
        Send message to STARS server: System hello
        Reply message arrived from STARS server: System>samplepyclient @hello Nice to meet you..

        [Disconnect]
        samplepyclient disconnected.

        [Connect as samplepyclientkeylist with keyword list(stars takashi kekpf hello)]
        samplepyclientkeylist connected.
        
        [Check Send and Receive test]
        Send message to STARS server: System help
        Reply message arrived from STARS server: System>samplepyclientkeylist @help flgon flgoff loadaliases listaliases loadpermission loadreconnectablepermission listnodes gettime hello getversion disconnect.

        STARS message: System>samplepyclientkeylist @help flgon flgoff loadaliases listaliases loadpermission loadreconnectablepermission listnodes gettime hello getversion disconnect
        Command of System: flgon
        Command of System: flgoff
        Command of System: loadaliases
        Command of System: listaliases
        Command of System: loadpermission
        Command of System: loadreconnectablepermission
        Command of System: listnodes
        Command of System: gettime
        Command of System: hello
        Command of System: getversion
        Command of System: disconnect
        Done.

        [Check receive timeout]
        Timeout detected.

        [Callback Start]
        Send event to myself.
        **Callback cb_handler(samplepyclientkeylist>samplepyclientkeylist _Event!!:1).**

        Send event to myself.
        **Callback cb_handler(samplepyclientkeylist>samplepyclientkeylist _Event!!:2).**

        Send event to myself.
        **Callback cb_handler(samplepyclientkeylist>samplepyclientkeylist _Event!!:3).**

        Send event to myself.
        **Callback cb_handler(samplepyclientkeylist>samplepyclientkeylist _Event!!:4).**

        Waiting message from the other stars client, press Enter to disconnect.

        [Disconnect]
        samplepyclient disconnected.
        **Callback cb_handler().**
        !!cb_handler() got Receive failure. (<class 'ConnectionAbortedError'>)

        [Check read error after disconnect]
        No socket.
        Bye.
