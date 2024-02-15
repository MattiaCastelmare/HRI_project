package com.example.myapplication;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class WebSocketClient extends WebSocketListener {
    private WebSocket webSocket;
    private PuzzleGame puzzleGame;

    public WebSocketClient(String url) {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(url).build();
        webSocket = client.newWebSocket(request, this);
    }
    public void initializePuzzle(PuzzleGame puzzleGame) {
        this.puzzleGame = puzzleGame;
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
            puzzleGame.PepperSwapsPuzzlePieces(index1, index2);
            System.out.println("Pepper is making a move, swapping: " + index1 + ", " + index2);
        }
        else if (text.startsWith("2_PepperMove:")) {
            // Remove the prefix '2_PepperMove:'
            String indicesPart = text.substring("2_PepperMove:".length()).trim();

            // Divide the string in two parts --> the two move indices
            String[] moves = indicesPart.split(";");

            // First Move
            String[] firstMoveIndices = moves[0].split(",");
            int index1_firstMove = Integer.parseInt(firstMoveIndices[0].trim());
            int index2_firstMove = Integer.parseInt(firstMoveIndices[1].trim());

            // Second move
            String[] secondMoveIndices = moves[1].split(",");
            int index1_secondMove = Integer.parseInt(secondMoveIndices[0].trim());
            int index2_secondMove = Integer.parseInt(secondMoveIndices[1].trim());

            // Send indices to the Puzzle
            puzzleGame.PepperSwapsPuzzlePieces(index1_firstMove, index2_firstMove);
            puzzleGame.PepperSwapsPuzzlePieces(index1_secondMove, index2_secondMove);
            System.out.println("Pepper is making two move, swapping: " + index1_firstMove + ", " + index2_firstMove + "and " + index1_secondMove + ", " + index2_secondMove);
        }
    }

    // Credo vada CANCELLATA visto che lo abbiamo già definito sopra
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

    public void sendMessage(String message) {
        webSocket.send(message);
    }

    public void disconnect() {
        webSocket.close(1000, "Disconnecting");
    }
}


