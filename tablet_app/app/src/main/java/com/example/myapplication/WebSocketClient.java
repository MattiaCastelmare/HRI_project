package com.example.myapplication;

import android.util.Log;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class WebSocketClient extends WebSocketListener {
    private WebSocket webSocket;
    private PuzzleGame puzzleGame;
    private MainActivity activity;

    public WebSocketClient(String url) {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(url).build();
        webSocket = client.newWebSocket(request, this);
    }
    public void initializePuzzle(PuzzleGame puzzleGame) {
        this.puzzleGame = puzzleGame;
    }
    public void sendActivity(MainActivity  activity) {this.activity = activity; }

    @Override
    public void onOpen(WebSocket webSocket, Response response) {
        System.out.println("Connected to WebSocket server");
    }

    @Override
    public void onMessage(WebSocket webSocket, String text) {
        System.out.println("Received message from server: " + text);
        if (text.equals("User wants to play")){
            activity.openLayoutQuestionnaire();
        }
        if (text.equals("Go back waiting")){
            activity.openLayoutGreetings();
        }
        if (text.startsWith("The suggested difficulty is:")){
            // Extract the difficulty part from the message
            String difficulty =  text.substring("The suggested difficulty is:".length()).trim();
            activity.openLayoutDifficulty(difficulty);
        }
        if (text.equals("Play again")){
            activity.openLayoutDifficulty(null);
        }
        if (text.equals("Exit")){
            activity.openLayoutGreetings();
        }
        if (text.startsWith("PepperMove:")) {
            // Extract the indices part from the message
            String indicesPart = text.substring("PepperMove:".length()).trim();
            // Split the indices
            String[] indices = indicesPart.split(",");
            int index1 = Integer.parseInt(indices[0].trim());
            int index2 = Integer.parseInt(indices[1].trim());
            // Send indices to the Puzzle
            puzzleGame.PepperSwapsPuzzlePieces(index1, index2);
        }
    }

    @Override
    public void onClosed(WebSocket webSocket, int code, String reason) {
        System.out.println("Disconnected from WebSocket server: " + reason);
    }

    @Override
    public void onFailure(WebSocket webSocket, Throwable t, Response response) {
        t.printStackTrace();
    }

    public void sendMessage(String message) {
        webSocket.send(message);
        Log.d(Constants.TAG, "Sent to Server: " + message);
    }

}


