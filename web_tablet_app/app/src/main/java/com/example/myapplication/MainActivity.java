package com.example.myapplication;

import android.content.ClipData;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.LayerDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.DragEvent;
import android.view.View;
import android.widget.TextView;
import android.widget.GridLayout;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnDragListener {
    private static final String TAG = "MainActivity";
    private ImageView firstClickedImageView;
    private int firstClickedPosition = -1;
    private GridLayout gridLayout;
    private static final String SERVER_URL = "http://10.0.2.2:8081/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        gridLayout = findViewById(R.id.gridLayout);

        executeGetRequest(); // Execute the GET request to server

        // Delay before sending the POST request
        new Handler().postDelayed(() -> sendStringToServer("Hello server"), 2000);

        initializeGridView(); // Initialize the grid view with shuffled images
    }

    private void executeGetRequest() {
        new Thread(() -> {
            try {
                URL url = new URL(SERVER_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);

                JSONObject postData = new JSONObject();
                postData.put("message", "Hello, Server!");

                try (OutputStream os = conn.getOutputStream()) {
                    byte[] input = postData.toString().getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = conn.getResponseCode();
                Log.d(TAG, "Response Code: " + responseCode);

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // Handle successful response
                } else {
                    Log.d(TAG, "Failed to send message. Response Code: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.d(TAG, "Failed to connect to the web server");
            }
        }).start();
    }

    private void sendStringToServer(final String message) {
        new Thread(() -> {
            try {
                URL url = new URL(SERVER_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);

                JSONObject postData = new JSONObject();
                postData.put("message", message);

                try (OutputStream os = conn.getOutputStream()) {
                    byte[] input = postData.toString().getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = conn.getResponseCode();
                Log.d(TAG, "Response Code: " + responseCode);

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // Message sent successfully
                    BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder responseStringBuilder = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        responseStringBuilder.append(line).append('\n');
                    }
                    reader.close();

                    Log.d(TAG, "Server Response: " + responseStringBuilder.toString());

                    // Parse the JSON response
                    JSONObject responseData = new JSONObject(responseStringBuilder.toString());
                    int number1 = responseData.getInt("number1");
                    int number2 = responseData.getInt("number2");

                    // Swap the corresponding puzzle pieces
                    swapPuzzlePieces(number1, number2);
                } else {
                    Log.d(TAG, "Failed to send message. Response Code: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.d(TAG, "Failed to connect to the web server");
            }
        }).start();
    }

    private void initializeGridView() {
        int childCount = gridLayout.getChildCount();
        List<Integer> indices = new ArrayList<>();
        for (int i = 0; i < childCount; i++) {
            indices.add(i);
        }
        Collections.shuffle(indices);
        for (int i = 0; i < childCount; i++) {
            final ImageView child = (ImageView) gridLayout.getChildAt(i);
            final int currentPosition = i;
            int imageIndex = indices.get(i) + 1;
            int imageResourceId = getResources().getIdentifier("patch_" + imageIndex, "drawable", getPackageName());
            child.setImageResource(imageResourceId);
            Log.d(TAG, "ImageView " + (i + 1) + ": Set Image Resource to " + imageResourceId);

            child.setOnClickListener(view -> {
                if (firstClickedImageView == null) {
                    firstClickedImageView = child;
                    firstClickedPosition = currentPosition;
                } else {
                    swapImages(firstClickedImageView, child);
                    firstClickedImageView = null;
                    firstClickedPosition = -1;
                }
            });

            child.setOnDragListener(this);
            child.setOnLongClickListener(view -> {
                ClipData data = ClipData.newPlainText("", "");
                View.DragShadowBuilder shadowBuilder = new View.DragShadowBuilder(view);
                view.startDrag(data, shadowBuilder, view, 0);
                return true;
            });
        }
        Log.d(TAG, "Swapped indices: " + indices.toString());
    }

    @Override
    public boolean onDrag(View v, DragEvent event) {
        int action = event.getAction();
        switch (action) {
            case DragEvent.ACTION_DRAG_STARTED:
                if (v instanceof ImageView && isDraggedViewCorrect((ImageView) v, event)) {
                    highlightView((ImageView) v);
                }
                break;
            case DragEvent.ACTION_DRAG_ENTERED:
                highlightView((ImageView) v);
                break;
            case DragEvent.ACTION_DRAG_EXITED:
            case DragEvent.ACTION_DRAG_ENDED:
                unhighlightView((ImageView) v);
                break;
            case DragEvent.ACTION_DROP:
                View draggedView = (View) event.getLocalState();
                if (draggedView instanceof ImageView && v instanceof ImageView) {
                    swapImages((ImageView) draggedView, (ImageView) v);
                }
                break;
        }
        return true;
    }

    private boolean isDraggedViewCorrect(ImageView targetView, DragEvent event) {
        View draggedView = (View) event.getLocalState();
        return draggedView != null && draggedView.equals(targetView);
    }

    private void swapImages(final ImageView firstImageView, final ImageView secondImageView) {
        Drawable firstImage = firstImageView.getDrawable();
        Drawable secondImage = secondImageView.getDrawable();
        firstImageView.setImageDrawable(secondImage);
        secondImageView.setImageDrawable(firstImage);

        new Handler().postDelayed(() -> updateIndicesTextView(firstClickedPosition, gridLayout.indexOfChild(firstImageView), gridLayout.indexOfChild(secondImageView)), 500); // Delay in milliseconds (adjust as needed)
    }

    private void updateIndicesTextView(int firstIndex, int firstImageIndex, int secondImageIndex) {
        TextView indicesTextView = findViewById(R.id.indicesTextView);
        String indicesText = "Swapped: " + (firstIndex + 1) + " with " + (firstImageIndex + 1) + " and " + (secondImageIndex + 1);
        indicesTextView.setText(indicesText);
    }

    private void highlightView(ImageView imageView) {
        Drawable[] layers = new Drawable[2];
        layers[0] = imageView.getDrawable();
        layers[1] = getGreenBorderDrawable();
        LayerDrawable layerDrawable = new LayerDrawable(layers);
        imageView.setBackground(layerDrawable);
    }

    private void unhighlightView(ImageView imageView) {
        imageView.setBackground(null);
    }

    private Drawable getGreenBorderDrawable() {
        GradientDrawable borderDrawable = new GradientDrawable();
        borderDrawable.setStroke(5, 0xFF00FF00);
        return borderDrawable;
    }

    private void swapPuzzlePieces(final int position1, final int position2) {
        runOnUiThread(() -> {
            ImageView imageView1 = (ImageView) gridLayout.getChildAt(position1);
            ImageView imageView2 = (ImageView) gridLayout.getChildAt(position2);

            Drawable image1 = imageView1.getDrawable();
            Drawable image2 = imageView2.getDrawable();

            imageView1.setImageDrawable(image2);
            imageView2.setImageDrawable(image1);

            // Update the indices text view
            updateIndicesTextView(position1, position1, position2);
        });
    }
}
