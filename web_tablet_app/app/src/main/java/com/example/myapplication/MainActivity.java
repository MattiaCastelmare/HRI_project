package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.GridLayout;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity {
    private ImageView firstClickedImageView;
    private int firstClickedPosition = -1;
    private GridLayout gridLayout;
    private Puzzle puzzle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Create the static grid layout from files
        setContentView(R.layout.activity_main);
        gridLayout = findViewById(R.id.gridLayout);
        // Create dynamic class to modify it
        puzzle = new Puzzle(gridLayout, this);
    }
}


