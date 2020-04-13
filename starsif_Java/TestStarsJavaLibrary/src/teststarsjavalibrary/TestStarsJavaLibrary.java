/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package teststarsjavalibrary;

import jp.kek.stars.*;

/**
 *
 * @author kosuge
 */
public class TestStarsJavaLibrary {
    static StarsInterface stars;
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        // Create STARS object and connect to STARS server.
        stars = new StarsInterface("Mytest", "localhost");

        //If keyWords is set, these keywords which seperated with blank is used for keyword checking.
        //stars.keyWords = "stars hello 123";
        
        try{
            stars.connect();
        }catch(StarsException se){
            System.out.println(se.getMessage());
        }
        System.out.println("Ok:");

        //"receive" method etc. hundles "StarsMessage".
        StarsMessage rdBuf = new StarsMessage();
      
        //Send message and receive message. They throws "StarsException".
        try{
            stars.send("System gettime");
            rdBuf = stars.receive();
        }catch(StarsException se){
            System.out.println(se.getMessage());
        }
        
        //"getAllMessage" returns druft message.
        System.out.println("all message: " + rdBuf.getAllMessage());

        //"getMessge returns" command and parameters.
        System.out.println("message:     " + rdBuf.getMessage());

        //These are example for handling each parameter.
        System.out.println("from:        " + rdBuf.from);
        System.out.println("to:          " + rdBuf.to);
        System.out.println("command:     " + rdBuf.command);
        System.out.println("parameters:  " + rdBuf.parameters);
        System.out.println();

        //Prepare call back function.
        StarsCallback Cbh = new StarsMessageHandler();
        stars.startCallbackHandler(Cbh);
        
        int i;
        System.out.println("Press \"Enter\" to terminate.");
        try{i = System.in.read();}catch(Exception e){}

        //Close stars connection and stop thread for call back.
        //With callback function, "disconnect" method must be executed before termination.
        try{stars.disconnect();}catch(StarsException es){}
        System.out.println("Terminated.");
    }
    
    
    //Class for callback. This class must have "starsCallbackHandler" method.
    static class StarsMessageHandler implements StarsCallback{

        //This method is called automatically from stars object.
        @Override
        public void starsCallbackHandler(StarsMessage st){
            System.out.println(st.getAllMessage());
            try{
                if(st.command.equals("hello")){
                    stars.send(st.from, "@hello nice to meet you.");
                }else if(st.command.equals("help")){
                    stars.send(st.from, "@help hello");
                }else if(st.command.charAt(0) == '@'){
                    System.out.println("Reply: " + st.getMessage());
                }else if(st.command.indexOf(0) == '_'){
                    System.out.println("Event: " + st.getMessage());                   
                }else{
                    stars.send(st.from, "@" + st.command + " Er: Bad command or parameter.");
                }
            }catch(Exception e){}
        }
    }
}
