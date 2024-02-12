package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.StaggeredGridLayoutManager;
import android.annotation.TargetApi;
import android.os.Build;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.widget.Button;
import android.view.View;
import android.content.Context;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private WebSocketClient wsc;
    private Puzzle puzzleLayout;

    @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Print screen resolution
        int[] resolution = printResolution();

        // Create Puzzle Layout
        Context context = this;
        puzzleLayout = new Puzzle(1, resolution, context, this);

        // Remove stuff from the Tablet
        getSupportActionBar().hide(); // Remove TitleBar
        // Hide the status bar
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        // HOMEPAGE
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
        }).start();

    }

    private void startGame() {
        wsc.sendMessage("Game started !");
        // Handle the button click and transition to the Puzzle layout
        setContentView(R.layout.activity_main);
        // Layout and adapter and manager
        RecyclerView recyclerView = findViewById(R.id.grid);
        PieceAdapter adapter = puzzleLayout.adapter;
        StaggeredGridLayoutManager layoutManager = puzzleLayout.layoutManager;
        // Create dynamic class to modify it
        List<Integer> initialIndices =puzzleLayout.initial_indices;
        PuzzleGame puzzleGame = new PuzzleGame(initialIndices,recyclerView, this ,wsc,adapter);
        // Send the puzzle to the Client
        wsc.initializePuzzle(puzzleGame);
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



