package com.example.myapplication;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import javax.websocket.*;

@ClientEndpoint
public class WebSocketClient {

    private WebSocketContainer container;
    private Session userSession;

    public WebSocketClient() {
        container = ContainerProvider.getWebSocketContainer();
    }

    public void connect(String serverUrl) {
        try {
            userSession = container.connectToServer(this, new URI(serverUrl));
        } catch (DeploymentException | URISyntaxException | IOException e) {
            e.printStackTrace();
        }
    }

    public void sendMessage(String message) throws IOException {
        userSession.getBasicRemote().sendText(message);
    }

    @OnOpen
    public void onOpen(Session session) {
        System.out.println("Connected to WebSocket server");
    }

    @OnClose
    public void onClose(Session session, CloseReason closeReason) {
        System.out.println("Disconnected from WebSocket server: " + closeReason);
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println("Received message from server: " + message);
        // Process the received message
    }

    public void disconnect() throws IOException {
        userSession.close();
    }
}

