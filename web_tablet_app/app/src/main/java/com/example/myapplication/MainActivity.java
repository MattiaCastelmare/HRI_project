package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.GridLayout;
import android.widget.Button;
import android.view.View;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.button);
        // Set up the Play button
        Button playButton = findViewById(R.id.playButton);
        playButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                createPuzzleLayout();
            }
        });
    }

    private void createPuzzleLayout() {
        // Handle the button click and transition to the Puzzle layout
        setContentView(R.layout.activity_main);
        // Get the GridLayout from the new layout
        GridLayout gridLayout = findViewById(R.id.gridLayout);
        // Create dynamic class to modify it
        Puzzle puzzle = new Puzzle(gridLayout, this);
    }
}



