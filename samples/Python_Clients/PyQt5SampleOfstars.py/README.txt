Sample program: 'PyQt5SampleOfstars.py' can be used to test 'stars.py' from PyQt5.

    This program requires the PyQt5 and the python environment.

    [PyQt5SampleOfstars.py]
    This program uses PyQt5 and is able to exchange STARS message via STARS server.

    The sample program trys to connect to the starsserver(=localhost) as the nodename 'samplepyclient'.

    To change the starsserver host and stars nodename, please edit the lines 185-186.
        [sampledriver.py]
        starshost = 'localhost'
        starsnode1= 'samplepyclient';

    To connect to STARS Server, please setup the keyfiles to STARS Server.
        [keyfiles]
        samplepyclient.key


Tested:
    PyQt 5.8.0 and python 3.4.4 on Windows7 32bit

Execution examples:

    [PyQt5SampleOfstars.py]

        Before start, change directory to where the 'PyQt5SampleOfstars.py' has been placed.

        $ python PyQt5SampleOfstars.py

        *If failed to start GUI, please check the console messages.
        
        *If failed to connnect to STARS server, the 'Connection failure' message will be displayed on console.
        For example:
            ------ the messages -----
            Connection failure. (localhost:6057, <class 'ConnectionRefusedError'>)
            Bye.
            ------
