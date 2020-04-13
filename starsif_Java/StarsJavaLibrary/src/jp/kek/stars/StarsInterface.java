/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package jp.kek.stars;

/**
 *
 * @author kosuge
 */
import java.io.*;
import java.util.*;
import java.net.*;

public class StarsInterface implements Runnable{
    private final int DEFAULT_TIMEOUT = 5000;
    public String nodeName;
    public String svrHost;
    public int svrPort;
    public String keyFile;
    public String keyWords = "";     //if not "" this keyWords is used for keyword checking.
    private Socket sock;
    private DataInputStream sockInput;
    private DataOutputStream sockOutput;
    private Thread myThread;    //For implements runnable. This object is used for Callback function.
    
    //These variables are used for Read messages;
    private byte[] readBuffer;
    private int readCount;
    private int processedCount;
    private int processedLevel;  //shows progress of message processing
                                 //(Processed.. 0=Nothing, 1=From, 2=To, 3=Command, 4=Parameter)
    private List []  mesProcArray; //Buffer for message processing.

    private StarsCallback cbPoint;
    private boolean isCbStarted = false;

    
    public StarsInterface(String nodeName, String svrHost, String keyFile, int svrPort){
        this.nodeName = nodeName;
        this.svrHost = svrHost;
        this.keyFile = keyFile;
        this.svrPort = svrPort;

        sock = null;
        readBuffer = new byte[1024];
        readCount = 0;
        processedCount = 0;
        processedLevel = 0;
        mesProcArray = new List[4];
        int lp;
        for (lp = 0; lp <= 3; lp++) { mesProcArray[lp] = new ArrayList(); }
    }

    public StarsInterface(String nodeName, String svrHost, String keyFile) {
        this(nodeName, svrHost, keyFile, 6057);
    }

    public StarsInterface(String nodeName, String svrHost) {
        this(nodeName, svrHost, nodeName + ".key", 6057);
    }

    public void connect() throws StarsException{
        //Read keyworks
        List keyword;
        try{
            keyword = getKeywords();
        }catch(IOException e){
            StarsException eStars = new StarsException("Could not open keyword file.: " + e.getMessage());
            throw(eStars);
        }

        //Connect to stars server
        try{
            sock = new Socket();
            sock.connect(new InetSocketAddress(svrHost, svrPort));
        }catch(Exception e){
            StarsException eStars = new StarsException("Could not establish TCP/IP connection.: " + e.getMessage());
            throw(eStars);
        }

        try{
            sockInput = new DataInputStream(sock.getInputStream());
            sockOutput = new DataOutputStream(sock.getOutputStream());
        }catch(IOException e){
            StarsException eStars = new StarsException("Could not create DataInputStream.: " + e.getMessage());
            throw eStars;
        }

        //Get random number.
        StarsMessage rdBuf = receive();
        int rNum = Integer.parseInt(rdBuf.from);

        //Get keyword and send to STARS server;
        String bufKeyword = (String) keyword.get(rNum % keyword.size());

        try{
            tcpSendString(nodeName + " " + bufKeyword);
            rdBuf = receive();
        }catch(StarsException se){
            throw se;
        }

        if(!rdBuf.command.equals("Ok:")){
            StarsException eStars = new StarsException("Could not connect to server.: " + rdBuf.getMessage());
            throw eStars;
        }
    }

    public void disconnect() throws StarsException{
        try{
            sock.close();
        }catch(IOException e){
            StarsException eStars = new StarsException("Could not disconnect.: " + e.getMessage());
            throw eStars;
        }
    }
    
    public void send(String sndTo, String sndCommand) throws StarsException{
        String sndBuf = sndTo + " " + sndCommand;
        tcpSendString(sndBuf);
    }

    public void send(String sndCommand) throws StarsException{
        tcpSendString(sndCommand);
    }


    private void tcpSendString(String sndBuf) throws StarsException{
        sndBuf = sndBuf + "\n";
        try{
            sockOutput.writeBytes(sndBuf);
        }catch(IOException e){
            StarsException eStars = new StarsException("Write error.: " + e.getMessage());
            throw eStars;
        }
    }

    public StarsMessage receive(int timeout) throws StarsException{
        StarsMessage rdMes;
        rdMes = receiveCommon(timeout);
        return(rdMes);
    }

    public StarsMessage receive() throws StarsException{
        StarsMessage rdMes;
        rdMes = receiveCommon(DEFAULT_TIMEOUT);
        return(rdMes);
    }

    private StarsMessage receiveCommon(int timeout) throws StarsException{
        StarsMessage rdMes = new StarsMessage();

        boolean isProcessed;
        while (true){
            isProcessed = processMessage(rdMes);
            if(isProcessed){break;}
            try{
                sock.setSoTimeout(timeout);
            }
            catch(Exception e){
                StarsException eStars = new StarsException("Could not set timeout.: " + e.getMessage());
                throw eStars;
            }

            try{
                readCount = sockInput.read(readBuffer);
                processedCount = 0;
            }
            catch (Exception e){
                //Clear buffers with error.
                readCount = 0;
                processedCount = 0;
                for (int lp = 0; lp < 4; lp++) { mesProcArray[lp].clear(); }
                processedLevel = 0;

                StarsException eStars = new StarsException("Receive error.: " + e.getMessage());
                throw eStars;
            }
            if (readCount < 1){
                StarsException eStars = new StarsException("Could not read.: " + String.valueOf(readCount));
                throw eStars;
            }
        }
        return rdMes;
    }

    public void startCallbackHandler(StarsCallback sCb){
        if(isCbStarted == true){return;}
        myThread = new Thread(this);
        cbPoint = sCb;
        isCbStarted = true;
        myThread.start();
    }
    
    @Override
    public void run(){
        StarsMessage rMess;
        while(isCbStarted){
            try{
                rMess = receiveCommon(0);
            }catch(StarsException e){
                rMess = null;
                isCbStarted = false;
                return;
            }
            cbPoint.starsCallbackHandler(rMess);
        }
    }
    
    
    private boolean processMessage(StarsMessage rdMess){
        byte [] delimiter = {0x3e, 0x20, 0x20, 0x0a};
        rdMess.clear();
        byte nret = 0;
        int lp;
        while (processedCount < readCount){
            nret = readBuffer[processedCount];
            processedCount++;
            if (nret == 0x0d) { continue; }
            if (nret == 0x0a){
                rdMess.from = array2String(mesProcArray[0]);
                rdMess.to = array2String(mesProcArray[1]);
                rdMess.command = array2String(mesProcArray[2]);
                rdMess.parameters = array2String(mesProcArray[3]);
                for (lp = 0; lp < 4; lp++) { mesProcArray[lp].clear(); }
                processedLevel = 0;
                return true;
            }
            if (nret == delimiter[processedLevel]) { processedLevel++; continue; }
            mesProcArray[processedLevel].add(nret);
        }
        processedCount = 0;
        readCount = 0;
        return false;
    }


    private String array2String(List al){
        int alSize = al.size();
        byte[] bBuf = new byte[alSize];
        for (int i= 0; i< alSize; i++){
            bBuf[i] = (Byte) al.get(i);
        }
        return(new String(bBuf, 0, alSize));
    }


    private List getKeywords() throws IOException{
        List<String> keyword = new ArrayList<String>();

        if(! keyWords.equals("")){
            String [] dkeys = keyWords.split(" ");
            keyword.addAll(Arrays.asList(dkeys));
        }else{
            try{
                FileReader reader = new FileReader(keyFile);
                BufferedReader br = new BufferedReader(reader);
                String line;
                while((line = br.readLine()) != null){
                    keyword.add(line);
                }
                br.close();
                reader.close();
            }catch(IOException e){
                throw(e);
            }
        }
        return(keyword);
    }
   
}
