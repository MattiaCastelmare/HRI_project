package com.example.myapplication;


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
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Puzzle implements View.OnDragListener{
        private ImageView firstClickedImageView;
        private int firstClickedPosition = -1;
        List<Integer> indices = new ArrayList<>();
        private GridLayout gridLayout;
        private Context context;
        // Constructor
        public Puzzle(GridLayout gridLayout, Context context) {
                this.gridLayout = gridLayout;
                this.context = context;
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
                        int imageIndex = indices.get(i) + 1;
                        int imageResourceId = context.getResources().getIdentifier("patch_" + imageIndex, "drawable", context.getPackageName());
                        child.setImageResource(imageResourceId);
                        Log.d(Constants.TAG, "ImageView " + (i + 1) + ": Set Image Resource to " + imageResourceId);

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
                Log.d(Constants.TAG, "Swapped indices: " + indices.toString());
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

        // Queste sono relative al on Drag event
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
                Drawable firstImage = firstImageView.getDrawable();
                Drawable secondImage = secondImageView.getDrawable();
                firstImageView.setImageDrawable(secondImage);
                secondImageView.setImageDrawable(firstImage);
        }
}