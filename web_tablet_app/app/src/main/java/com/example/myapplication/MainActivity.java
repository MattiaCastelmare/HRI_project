package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.GridLayout;
import android.widget.Button;
import android.view.View;

public class MainActivity extends AppCompatActivity {
    private WebSocketClient wsc;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.button);

        // Connect to Server in a separate thread
        new Thread(() -> {
            wsc = new WebSocketClient(Constants.SERVER_URL);
            // You can perform UI updates after the connection is established
            runOnUiThread(() -> {
                // Set up the Play button
                Button playButton = findViewById(R.id.playButton);
                playButton.setOnClickListener(view -> createPuzzleLayout());
            });
        }).start();
    }

    private void createPuzzleLayout() {
        wsc.sendMessage("Game started !");
        // Handle the button click and transition to the Puzzle layout
        setContentView(R.layout.activity_main);
        // Get the GridLayout from the new layout
        GridLayout gridLayout = findViewById(R.id.gridLayout);
        // Create dynamic class to modify it
        Puzzle puzzle = new Puzzle(gridLayout, this, wsc);
        // Send the puzzle to the Client
        wsc.initializePuzzle(puzzle);
    }
}



