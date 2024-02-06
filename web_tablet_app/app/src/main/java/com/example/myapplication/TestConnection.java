package com.example.myapplication;

import java.io.IOException;

public class TestConnection {

    public WebSocketClient wsc;
    public TestConnection() {
    }

    public void Start() throws InterruptedException, IOException {

        wsc = new WebSocketClient();
        //wsc.callback = this;
        wsc.connect("ws://192.168.1.105:8888/websocket");
        Thread.sleep(1000);
        wsc.disconnect();
    }

    public static void main(String[] args) throws InterruptedException, IOException
    {
        TestConnection t = new TestConnection();
        t.Start();
        Thread.sleep(1000);
    }

}