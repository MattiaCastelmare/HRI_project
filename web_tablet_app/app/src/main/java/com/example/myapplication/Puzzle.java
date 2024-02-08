package com.example.myapplication;

import android.app.Activity;
import android.content.ClipData;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.LayerDrawable;
import android.util.Log;
import android.view.DragEvent;
import android.view.View;
import android.widget.GridLayout;
import android.widget.ImageView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Puzzle implements View.OnDragListener{
        private ImageView firstClickedImageView;
        private int firstClickedPosition = -1;
        private List<Integer> indices = new ArrayList<>();
        private GridLayout gridLayout;
        private Context context;
        private WebSocketClient webSocketClient;

        // Constructor
        public Puzzle(GridLayout gridLayout, Context context,WebSocketClient webSocketClient) {
                this.gridLayout = gridLayout;
                this.context = context;
                this.webSocketClient = webSocketClient;
                initializeGridView();
        }
        private void initializeGridView() {
                int childCount = gridLayout.getChildCount();
                for (int i = 0; i < childCount; i++) {
                        indices.add(i);
                }
                Collections.shuffle(indices);
                for (int i = 0; i < childCount; i++) {
                        final ImageView child = (ImageView) gridLayout.getChildAt(i);
                        final int currentPosition = i;
                        int imageIndex = indices.get(i);
                        int imageResourceId = context.getResources().getIdentifier("patch_" + imageIndex, "drawable", context.getPackageName());
                        child.setImageResource(imageResourceId);
                        // Set the tag to store the position of the ImageView
                        child.setTag(currentPosition);
                        Log.d(Constants.TAG, "ImageView " + i + ", Tag: " + child.getTag());
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

                // Send initial random indices to the Server
                String initial_message = "Initial random indices: " + indices.toString();
                webSocketClient.sendMessage(initial_message);
                Log.d(Constants.TAG, "Initial random indices: " + indices.toString());
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
        private int getImageViewIndex(ImageView imageView) {
                // Retrieve the index from the tag
                Object tag = imageView.getTag();
                return tag instanceof Integer ? (Integer) tag : -1;
        }
        private ImageView findImageViewByIndex(int index) {
                // Iterate through child views of the GridLayout to find the ImageView with the specified index
                int childCount = gridLayout.getChildCount();
                for (int i = 0; i < childCount; i++) {
                        View child = gridLayout.getChildAt(i);
                        if (child instanceof ImageView) {
                                ImageView imageView = (ImageView) child;
                                int imageViewIndex = getImageViewIndex(imageView);
                                if (imageViewIndex == index) {
                                        return imageView;
                                }
                        }
                }
                return null; // Return null if ImageView with the specified index is not found
        }
        // Next classes are relative al on Drag event
        private boolean isDraggedViewCorrect(ImageView targetView, DragEvent event) {
                View draggedView = (View) event.getLocalState();
                return draggedView != null && draggedView.equals(targetView);
        }
        private void highlightView(ImageView imageView) {
                Drawable[] layers = new Drawable[2];
                layers[0] = imageView.getDrawable();
                layers[1] = getGreenBorderDrawable();
                LayerDrawable layerDrawable = new LayerDrawable(layers);
                imageView.setBackgroundDrawable(layerDrawable);
        }

        private void unhighlightView(ImageView imageView) {
                imageView.setBackgroundDrawable(null);
        }

        private Drawable getGreenBorderDrawable() {
                GradientDrawable borderDrawable = new GradientDrawable();
                borderDrawable.setStroke(5, 0xFF00FF00);
                return borderDrawable;
        }

        private void swapImages(final ImageView firstImageView, final ImageView secondImageView) {
                // Get the indices from the ImageViews
                int firstIndex = getImageViewIndex(firstImageView);
                int secondIndex = getImageViewIndex(secondImageView);
                // Swap the Image Views
                Drawable firstImage = firstImageView.getDrawable();
                Drawable secondImage = secondImageView.getDrawable();
                firstImageView.setImageDrawable(secondImage);
                secondImageView.setImageDrawable(firstImage);
                // Update the indices in the list
                Collections.swap(indices, firstIndex, secondIndex);
                Log.d(Constants.TAG, "New indices after swap: " + indices.toString());
                // Send indices to Server
                String swap_message = "SWAP: position " + firstIndex + " , with " + secondIndex;
                String indices_message = "New indices: " + indices.toString();
                webSocketClient.sendMessage(swap_message);
                webSocketClient.sendMessage(indices_message);
        }
        public void PepperSwapsPuzzlePieces(int index1, int index2) {
                // Ensure UI updates are done on the main thread
                ((Activity) context).runOnUiThread(() -> {
                        // Locate the corresponding ImageViews in the GridLayout
                        ImageView firstImageView = findImageViewByIndex(index1);
                        ImageView secondImageView = findImageViewByIndex(index2);
                        // Swap the Image Views
                        Drawable firstImage = firstImageView.getDrawable();
                        Drawable secondImage = secondImageView.getDrawable();
                        firstImageView.setImageDrawable(secondImage);
                        secondImageView.setImageDrawable(firstImage);
                        // Update the indices in the list
                        Collections.swap(indices, index1, index2);
                        System.out.println("Pepper is making a move, swapping: " + index1 + ", " + index2);
                        // SEND THEM BACK TO PEPPER MAYBE?
                });
        }
}