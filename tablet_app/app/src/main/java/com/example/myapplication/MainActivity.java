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

    @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Print screen resolution
        int[] resolution = printResolution();

        // Remove stuff from the Tablet
        getSupportActionBar().hide(); // Remove TitleBar
        // Hide the status bar
        View decorView = getWindow().getDecorView();
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        // GREETINGS background
        setContentView(R.layout.greetings);

        // Connect to Server in a separate thread
        new Thread(() -> {
            wsc = new WebSocketClient(Constants.SERVER_URL);
            wsc.sendActivity((MainActivity context) context)
        }).start();
    }
    public void openWinLayout(){
            int imageId = puzzleLayout.getChosenImage();
            runOnUiThread(() -> {
                setContentView(R.layout.layout);
                ImageView imageView = findViewById(R.id.solved_puzzle);
                imageView.setImageResource(imageId);
            });
        }
    public void openLayoutQuestionaire(){
        runOnUiThread(() -> {
            setContentView(R.layout.questions);
            Button play = findViewById(R.id.playButton);
            play.setOnClickListener(view -> openLayoutDifficulty());
        });
        }).start();
    }
    public void openLayoutDifficulty(String difficulty){
        runOnUiThread(() -> {
            setContentView(R.layout.difficulty);
            text = "Pepper suggests " + difficulty;
            findViewById(textView).setText(text);
            Button easy = findViewById(R.id.easy);
            Button medium = findViewById(R.id.medium);
            Button hard = findViewById(R.id.hard);
            easy.setOnClickListener(view -> startGame(1));
            medium.setOnClickListener(view -> startGame(2));
            hard.setOnClickListener(view -> startGame(3));
        });
    }
    private void startGame(int difficulty) {
        wsc.sendMessage("Game started !");
        puzzleLayout = new Puzzle(difficulty, resolution, this);
        // Handle the button click and transition to the Puzzle layout
        setContentView(R.layout.activity_main);
        PuzzleGame puzzleGame = new PuzzleGame(puzzleLayout, this , wsc);
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



