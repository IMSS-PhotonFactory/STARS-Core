# starsbridge.py
__starsbridge__ is a STARS client program.
It connects to two STARS servers and relays STARS messages between them.
 
## Requirements
* Python 3
* Two STARS Servers.

## Example Setup
  Assume `starsbridge.py` connects to STARS Server1 as `stbr` and Server2 as `stbr2`.
  The program runs on STARS Server1.
 
```md
   localhost                      192.168.1.100
   --------                        --------
  |STARS   |                      |STARS   |
  | Server1|                      | Server2|
   --------                        -------- 
       |                              |               
       +---stbr [starsbrige.py]       |
                     |                |
                     +-----stbr2------+
```

### 1\. Prepare the configuration file `config.cfg`

```Ini
[STARS]
StarsServerHost1=localhost
StarsNodeName1=stbr
StarsServerPort1=6057
StarsServerHost2=192.168.1.100
StarsNodeName2=stbr2
StarsServerPort2=6057
```

* Update `StarsServerHost[1,2]` with the correct hostnames or IP addresses.
* Set `StarsNodeName[1,2]` to match your desired node names.


### 2\. Install STARS keyfiles on STARS Servers
* Install `stbr.key`  on STARS Server1.
* Install `stbr2.key` on STARS Server2.

## Start the program
```Bash
python starsbrige.py --config config.cfg [--logenable --logdir <logoutpufolder> -d]
```

## Runtime example

```md
  --------                        --------    (I/O Client)   (motornames)
 |STARS   |                      |STARS   |------pm16c04---------th
 | Server1|                      | Server2|         |
  --------                        --------          +------------dth1
      |                              |               
      +--stbr [starsbrige.py]        |
      |             |                |
      |             +-----stbr2------+
      |                              
      +--term1                       
``` 
* `starsbridge.py` connects to STARS Server1 as `stbr` and Server2 as `stbr2`.
* A terminal client connects to Server1 as `term1`.
* A I/O client connects to Server2 as `pm16c04`.

### Example STARS Messages
`term1` on Server1 sends a message to `pm16c04` on Server2.
Then `term1` on Server1 recieves a reply from `pm16c04` on Server2.
```md
 stbr2.pm16c04 hello
 stbr2.pm16c04>term1 @hello nice to meet you.
 stbr2.pm16c04.th GetValue
 stbr2.pm16c04.th>term1 @GetValue 1234
```

## Notes
  This README covers the basic setup for the `starsbridge.py` program.
  Detailed documentation for additional configuration options in `config.cfg` is coming soon.
  
## Author
 Y. Nagatani @ KEK, Photon Factory