Sample program: 'sampledriver.py' can be used to test 'singlestars.py' featuring the callback method which runs on the single thread.

    [sampledriver.py]
    The sample program trys to connect to the starsserver(=localhost) as the nodename 'samplepyclient'.

    To change the starsserver host and stars nodename, please edit the lines 13-14.
        [sampledriver.py]
        starshost = 'localhost'
        starsnode1= 'samplepyclient';

    To connect to STARS Server, please setup the keyfiles to STARS Server.
        [keyfiles]
        samplepyclient.key

Tested:
    python 3.4.4 on Windows7 32bit
    python 2.7.12 on Linux "Ubuntu 16.04.1 LTS"

Execution examples:

    $ python sampledriver.py
        Send message to STARS server: System gettime
        Reply message arrived from STARS server: System>samplepyclient @gettime 2017-02-17 18:35:40.
        Start Callback method in the single thread.
        Waiting STARS message from the other stars client.
        Try STARS command 'samplepyclient help'
        Try STARS command 'samplepyclient terminate' to term this client.
        **Interval sb_interval() called at 2017-02-17 18:35:45.**
        Change intervaltime from 5 to 1 seconds.
        **Interval sb_interval() called at 2017-02-17 18:35:46.**
        Change intervaltime from 1 to 5 seconds.
        **Interval sb_interval() called at 2017-02-17 18:35:51.**
        Change intervaltime from 5 to 1 seconds.
        **Interval sb_interval() called at 2017-02-17 18:35:52.**
        Change intervaltime from 1 to 5 seconds.
        **Callback sb_handler(term1>samplepyclient hello).**
        Send:samplepyclient>term1 @hello nice to meet you.
        **Callback sb_handler(term1>samplepyclient help).**
        Send:samplepyclient>term1 @help hello help terminate
        **Interval sb_interval() called at 2017-02-17 18:35:57.**
        Change intervaltime from 5 to 1 seconds.
        **Callback sb_handler(term1>samplepyclient terminate).**
        Send:samplepyclient>term1 @terminate Ok:
        Bye.

    <The STARS messages between STARS node 'term1' and 'samplepyclient'>
        samplepyclient hello
        samplepyclient>term1 @hello nice to meet you.
        samplepyclient help
        samplepyclient>term1 @help hello help terminate
        samplepyclient terminate
        samplepyclient>term1 @terminate Ok:
