package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.widget.GridLayout;
import android.widget.Button;
import android.view.View;
import android.widget.ImageView;
import android.view.Gravity;
import android.content.Context;

public class MainActivity extends AppCompatActivity {
    private WebSocketClient wsc;
    private Puzzle puzzleLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Print screen resolution
        int[] resolution = printResolution();
        // Create Puzzle Layout
        Context context = this;
        puzzleLayout = new Puzzle( 1, resolution, context, this);

        getSupportActionBar().hide(); // Remove TitleBar
        // Hide the status bar
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);
        /*
        setContentView(R.layout.button);
        // Connect to Server in a separate thread
        new Thread(() -> {
            wsc = new WebSocketClient(Constants.SERVER_URL);
            // You can perform UI updates after the connection is established
            runOnUiThread(() -> {
                // Set up the Play button
                Button playButton = findViewById(R.id.playButton);
                playButton.setOnClickListener(view -> startGame());
            });
        }).start();*/
    }

    private void startGame() {
        wsc.sendMessage("Game started !");
        // Handle the button click and transition to the Puzzle layout
        setContentView(R.layout.activity_main);
        // Get the GridLayout from the new layout
        //GridLayout gridLayout = findViewById(R.id.gridLayout);
        // Create dynamic class to modify it
        //PuzzleGame puzzleGame = new PuzzleGame(gridLayout, this, wsc);
        // Send the puzzle to the Client
        //wsc.initializePuzzle(puzzleGame);
    }
    public int[] printResolution() {
        DisplayMetrics displayMetrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        int screenWidth = displayMetrics.widthPixels;
        int screenHeight = displayMetrics.heightPixels;
        Log.d(Constants.TAG, "SCREEN Width: " + screenWidth + ", Height: " + screenHeight);
        return new int[]{screenHeight, screenWidth};
    }
}



