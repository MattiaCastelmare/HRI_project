package com.example.myapplication;

import android.util.Log;
import java.net.ConnectException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;
import java.util.Timer;
import java.util.TimerTask;

public class WebSocketClient extends WebSocketListener {
    private WebSocket webSocket;
    private Puzzle puzzle;
    private String url_;

    public WebSocketClient(String url) {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(url).build();
        webSocket = client.newWebSocket(request, this);

        this.url_ = url;
        //Schedule the periodic function
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run(){
                PeriodicFunction();
            }
        },0 , 3000);
    }
    public void initializePuzzle(Puzzle puzzle) {
        this.puzzle = puzzle;
    }

    @Override
    public void onOpen(WebSocket webSocket, Response response) {
        System.out.println("Connected to WebSocket server");
    }

    @Override
    public void onMessage(WebSocket webSocket, String text) {
        System.out.println("Received message from server: " + text);
        if (text.startsWith("PepperMove:")) {
            // Extract the indices part from the message
            String indicesPart = text.substring("PepperMove:".length()).trim();
            // Split the indices
            String[] indices = indicesPart.split(",");
            int index1 = Integer.parseInt(indices[0].trim());
            int index2 = Integer.parseInt(indices[1].trim());
            // Send indices to the Puzzle
            puzzle.PepperSwapsPuzzlePieces(index1, index2);
            System.out.println("Pepper is making a move, swapping: " + index1 + ", " + index2);
        }
    }
    @Override
    public void onMessage(WebSocket webSocket, ByteString bytes) {
        // Handle binary messages if needed
    }

    @Override
    public void onClosed(WebSocket webSocket, int code, String reason) {
        System.out.println("Disconnected from WebSocket server: " + reason);
    }

    @Override
    public void onFailure(WebSocket webSocket, Throwable t, Response response) {
        t.printStackTrace();
    }

    public void sendMessage(String message)
    {
        webSocket.send(message);
    }

    public void disconnect() {
        webSocket.close(1000, "Disconnecting");
    }

    public boolean isConnected(){
        return webSocket != null && webSocket.send("ping"); // In this way it sends a ping to check connection
    }

    public void PeriodicFunction() {
        if (!isConnected()) {
            Log.d(Constants.TAG, "Tablet not connected, trying to reconnect...");
            OkHttpClient client = new OkHttpClient();
            Request request = new Request.Builder().url(url_).build();
            webSocket = client.newWebSocket(request, this);

            // Check if the connection is open after attempting to establish it
            if (!webSocket.send("ping")) {
                Log.e(Constants.TAG, "Failed to connect to server: Connection not open");
                // You can handle the connection failure here, such as showing a message to the user
                // or attempting to reconnect after a delay
            }
        } else {
            Log.d(Constants.TAG, "Tablet connected");
        }
    }



}


