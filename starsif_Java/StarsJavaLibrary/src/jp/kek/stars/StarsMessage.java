/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package jp.kek.stars;

/**
 *
 * @author kosuge
 */
public class StarsMessage {

    public String from;
    public String to;
    public String command;
    public String parameters;

    public StarsMessage(String from, String to, String command, String parameters) {
        this.from = from;
        this.to = to;
        this.command = command;
        this.parameters = parameters;
    }

    public StarsMessage() {
        this.clear();
    }

    public void clear() {
        this.from = "";
        this.to = "";
        this.command = "";
        this.parameters = "";
    }

    public String getAllMessage(){
        if(parameters.length() == 0){
            return(from + ">" + to + " " + command);
        }else{
            return(from + ">" + to + " " + command + " " + parameters);
        }
    }

    public String getMessage(){
        if(parameters.length() == 0){
            return(command);
        }else{
            return(command + " " + parameters);
        }
    }

}
