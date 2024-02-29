package com.example.myapplication;


import android.app.Activity;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.view.DragEvent;
import android.view.View;
import android.widget.ImageView;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.StaggeredGridLayoutManager;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Timer;
import java.util.TimerTask;

public class PuzzleGame {
        private final Context context;
        private final MainActivity mainActivity;
        private final PieceAdapter adapter;
        private final RecyclerView recyclerView;
        private final WebSocketClient webSocketClient;
        private int lastClickedPosition = 0;
        private final Timer timer = new Timer();
        private int imageId;
        private final List<Integer> indices;

        // Constructor
        public PuzzleGame(Puzzle puzzleLayout, Context context, WebSocketClient webSocketClient) {
                this.context = context;
                this.mainActivity = (MainActivity) context;
                this.recyclerView = mainActivity.findViewById(R.id.grid);
                // Create dynamic class to modify it
                this.indices = puzzleLayout.initial_indices;;
                this.webSocketClient = webSocketClient;
                this.adapter= puzzleLayout.adapter;
                this.imageId = puzzleLayout.random_id;
                initializeGridView();
                timer.schedule(new CheckIndicesTask(), 1000, 100); // period (in milliseconds)
        }
        private class CheckIndicesTask extends TimerTask {
                @Override
                public void run() {
                        if (areIndicesInOrder()) {
                                mainActivity.openWinLayout();
                                ImageView imageView = mainActivity.findViewById(R.id.solved_puzzle);
                                imageView.setImageResource(imageId);
                                timer.cancel();
                                timer.purge();
                        }
                }
        }
        private void initializeGridView() {
                // Attach the adapter and layout manager to the RecyclerView
                StaggeredGridLayoutManager layoutManager = new StaggeredGridLayoutManager(Constants.cols, StaggeredGridLayoutManager.HORIZONTAL);
                recyclerView.setLayoutManager(layoutManager);
                recyclerView.setAdapter(adapter);
                recyclerView.addItemDecoration(new SpacesItemDecoration(2));
                // Set up click and drag listeners for each item in the RecyclerView
                recyclerView.setOnDragListener(adapter.getDragListener());
                adapter.setOnItemClickListener(this::handleItemClick);
                adapter.setOnDragListener(this::handleDrag);
                // Send initial random indices to the Server
                String initial_message = "Initial random indices: " + indices.toString();
                webSocketClient.sendMessage(initial_message);
                Log.d(Constants.TAG, "Initial random indices: " + indices);
        }
        private boolean areIndicesInOrder() {
                for (int i = 0; i < indices.size() - 1; i++) {
                        if (indices.get(i) > indices.get(i + 1)) {
                                // Indices are not in order
                                return false;
                        }
                }
                return true;
        }
        private void handleItemClick(int position) {
                // Check if it's the first click
                if (adapter.getFirstClickedPosition() == -1) {
                        //Get the original index from the Piece object associated with the clicked position
                        int originalIndex = indices.get(position);
                        adapter.setFirstClickedPosition(position);
                        highlightView(Objects.requireNonNull(findImageViewByIndex(position)));
                        unhighlightView(Objects.requireNonNull(findImageViewByIndex(lastClickedPosition)));
                        lastClickedPosition = position;
                        Log.d(Constants.TAG, "First click at position: " + position + "with tag" + originalIndex);
                } else {
                        // It's the second click
                        int firstClickedPosition = adapter.getFirstClickedPosition();
                        Log.d(Constants.TAG, "Second click at positions: " + firstClickedPosition + " and " + position);
                        highlightView(Objects.requireNonNull(findImageViewByIndex(position)));
                        unhighlightView(Objects.requireNonNull(findImageViewByIndex(lastClickedPosition)));
                        swapImages(firstClickedPosition, position);
                        // Reset for the next set of clicks
                        adapter.setFirstClickedPosition(-1);
                        lastClickedPosition = position;
                }
        }

        private boolean handleDrag(View v, DragEvent event) {
                int action = event.getAction();
                int draggedIndex= (int) event.getLocalState();
                ImageView draggedImageView = findImageViewByIndex(draggedIndex);
                switch (action) {
                        case DragEvent.ACTION_DRAG_STARTED:
                                if (draggedImageView != null){
                                        unhighlightView(Objects.requireNonNull(findImageViewByIndex(lastClickedPosition)));
                                        //Log.d(Constants.TAG, "Drag started. Found Piece position: " + draggedIndex);
                                        highlightView(draggedImageView);
                                }
                                break;
                        case DragEvent.ACTION_DRAG_ENTERED:
                                if (v instanceof ImageView && isDraggedViewCorrect((ImageView) v, event)) {
                                        assert draggedImageView != null;
                                        draggedImageView.setVisibility(View.INVISIBLE);
                                        highlightView((ImageView) v);
                                }
                                break;
                        case DragEvent.ACTION_DRAG_EXITED:
                                if (v instanceof ImageView && draggedImageView != null ) {
                                        unhighlightView((ImageView) v);
                                }
                                break;
                        case DragEvent.ACTION_DRAG_ENDED:
                                assert draggedImageView != null;
                                draggedImageView.setVisibility(View.VISIBLE);
                                break;
                        case DragEvent.ACTION_DROP:
                                if (v instanceof ImageView && draggedImageView != null){
                                int newPosition = (int) v.getTag();
                                Log.d(Constants.TAG, "Dragged piece position " + draggedIndex);
                                Log.d(Constants.TAG, "Image dropped here: " + newPosition);
                                // Perform swapImages logic using the positions
                                swapImages( draggedIndex, newPosition);
                                unhighlightView((ImageView) v);
                                draggedImageView.setVisibility(View.VISIBLE);
                                lastClickedPosition = draggedIndex;
                                }
                                break;
                }
                return true;
        }

        private ImageView findImageViewByIndex(int index) {
                // Assuming you have set tags for ImageViews in your RecyclerView
                for (int i = 0; i < recyclerView.getChildCount(); i++) {
                        View itemView = recyclerView.getChildAt(i);
                        // Assuming that ImageView is the only type of view you want to retrieve the tag from
                        if (itemView instanceof ImageView) {
                                // Retrieve the tag for each ImageView based on index
                                Object tag = itemView.getTag();
                                // Use the tag as needed
                                if (tag != null && tag.equals(index)) {
                                        return (ImageView) itemView;
                                }
                        }
                }
                return null;
        }
        // Next classes are relative al on Drag event
        private void highlightView(ImageView imageView) {
                Drawable highlight = context.getResources().getDrawable( R.drawable.highlight);
                imageView.setBackgroundDrawable(highlight);
        }
        private void unhighlightView(ImageView imageView) {
                imageView.setBackgroundDrawable(null);
        }
        private boolean isDraggedViewCorrect( ImageView v, DragEvent event) {
                int pointingIndex = (int) v.getTag();
                ImageView child = (ImageView) recyclerView.findChildViewUnder(event.getX(), event.getY());
                if(child != null) {
                        int pointingIndex2 = (int) child.getTag();
                        return pointingIndex2 == pointingIndex;
                }
                return false;
        }
        private void swapImages(int firstIndex ,  int secondIndex) {
                ImageView firstImageView = findImageViewByIndex(firstIndex);
                ImageView secondImageView = findImageViewByIndex(secondIndex);
                // Swap the Image Views
                assert firstImageView != null && secondImageView != null;
                Drawable firstImage = firstImageView.getDrawable();
                Drawable secondImage = secondImageView.getDrawable();
                firstImageView.setImageDrawable(secondImage);
                secondImageView.setImageDrawable(firstImage);
                // Update the indices in the list
                Collections.swap(indices, firstIndex, secondIndex);
                Log.d(Constants.TAG, "New indices after swap: " + indices);
                // Send indices to Server
                String swap_message = "SWAP: position " + firstIndex + " , with " + secondIndex;
                String indices_message = "New indices: " + indices;
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
                        assert firstImageView != null && secondImageView != null;
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