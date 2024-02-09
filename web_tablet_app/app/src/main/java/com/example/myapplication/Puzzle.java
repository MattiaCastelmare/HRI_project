//https://dragosholban.com/2018/03/09/how-to-build-a-jigsaw-puzzle-android-game/
package com.example.myapplication;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Point;
import android.graphics.Rect;
import android.graphics.drawable.BitmapDrawable;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.graphics.BitmapFactory;
import android.view.ViewGroup;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.StaggeredGridLayoutManager;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Puzzle {
    int screenWidth;
    int screenHeight;
    int imageHeight;
    int imageWidth;
    int pieceWidth;
    int pieceHeight;
    int random_id;
    private final Context context;
    private final Activity parentActivity;
    int difficulty;
    int count;
    ArrayList<Piece> pieces;
    PieceAdapter adapter;
    StaggeredGridLayoutManager layoutManager;

    public Puzzle(int difficulty, int[] resolution, Context context, Activity parentActivity) {
        this.parentActivity = parentActivity;
        this.context = context;
        this.screenHeight = resolution[0];
        this.screenWidth = resolution[1];
        this.difficulty = difficulty;
        int[] chosen_images = chooseDifficulty(difficulty);
        getRandomImage(chosen_images);
        ResizeImage();
        setRandomImage(chosen_images);
        this.pieces = splitImage();
        addPiecesGrid(pieces);
    }

    public void setRandomImage(int[] images) {
        // Get the ImageView
        parentActivity.setContentView(R.layout.variable_image_layout);
        ImageView mImageView = parentActivity.findViewById(R.id.intact_image);
        // Set the layout parameters of the ImageView based on image dimensions
        ViewGroup.LayoutParams layoutParams = mImageView.getLayoutParams();
        layoutParams.width = imageWidth;
        layoutParams.height = imageHeight;
        // Set the image
        mImageView.setImageResource(images[random_id]);
    }

    public void getRandomImage(int[] images) {
        // Get a random between 0 and images.length-1
        random_id = (int) (Math.random() * images.length);
        // Decode the image to obtain its dimensions
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(context.getResources(), images[random_id], options);
        // Get the dimensions of the image
        imageWidth = options.outWidth;
        imageHeight = options.outHeight;
        Log.d(Constants.TAG, "IMAGE Width: " + imageWidth + ", Height: " + imageHeight);
    }

    public void ResizeImage() {
        // Check if both dimensions are larger than the screen
        if (imageHeight > screenHeight || imageWidth > screenWidth) {
            count += 1;
            // Resize both dimensions
            imageHeight = (int) (imageHeight * Constants.scaleParam);
            imageWidth = (int) (imageWidth * Constants.scaleParam);
            Log.d(Constants.TAG, "RESIZED IMAGE Width: " + imageWidth + ", Height: " + imageHeight);
            // Recursive call to check again
            ResizeImage();
        }
    }

    public int[] chooseDifficulty(int difficulty) {
        if (difficulty == 1) {
            return Constants.EASY_IMAGES;
        } else if (difficulty == 2) {
            return Constants.MEDIUM_IMAGES;
        } else if (difficulty == 3) {
            return Constants.DIFFICULT_IMAGES;
        } else {
            throw new IllegalArgumentException("Invalid difficulty level: " + difficulty);
        }
    }

    private ArrayList<Piece> splitImage() {
        ArrayList<Piece> pieces = new ArrayList<>(Constants.number_of_pieces);
        final ImageView imageView = parentActivity.findViewById(R.id.intact_image);
        BitmapDrawable drawable = (BitmapDrawable) imageView.getDrawable();
        Bitmap bitmap = drawable.getBitmap();
        // scale the image
        Bitmap scaledBitmap = Bitmap.createScaledBitmap(bitmap, imageWidth, imageHeight, true);
        // Compute H W of pieces
        pieceWidth = (imageWidth / Constants.cols) - 1;
        pieceHeight = (imageHeight / Constants.rows) - 1;
        Log.d(Constants.TAG, "Piece Width: " + pieceWidth);
        Log.d(Constants.TAG, "Piece Height: " + pieceHeight);
        // Create each bitmap piece and add it to the resulting array
        int yCord = 0;
        for (int row = 0; row < Constants.rows; row++) {
            int xCord = 0;
            for (int col = 0; col < Constants.cols; col++) {
                Log.d(Constants.TAG, "X: " + xCord + " Y: " + yCord);
                Piece piece = new Piece(Bitmap.createBitmap(scaledBitmap, xCord, yCord, pieceWidth, pieceHeight), xCord, yCord);
                pieces.add(piece);
                xCord += pieceWidth;
            }
            yCord += pieceHeight;
        }
        Collections.shuffle(pieces);
        return pieces;
    }

    private void addPiecesGrid(ArrayList<Piece> pieces) {
        parentActivity.setContentView(R.layout.activity_main);
        final RecyclerView recyclerView = parentActivity.findViewById(R.id.grid);
        // Create a StaggeredGridLayoutManager with 3 columns
        this.layoutManager = new StaggeredGridLayoutManager(Constants.cols, StaggeredGridLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(layoutManager);
        // Create an adapter for the RecyclerView
        this.adapter = new PieceAdapter(context, pieces, pieceWidth, pieceHeight);
        recyclerView.setAdapter(adapter);
        recyclerView.addItemDecoration(new SpacesItemDecoration(2));
    }
}

 class SpacesItemDecoration extends RecyclerView.ItemDecoration {
        private int spacing;

        public SpacesItemDecoration(int spacing) {
            this.spacing = spacing;
        }
        @Override
        public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
            outRect.left = spacing;
            outRect.right = spacing;
            outRect.top = spacing;
            outRect.bottom = spacing;
        }
    }

    class PieceAdapter extends RecyclerView.Adapter<PieceAdapter.PieceViewHolder> {
        private Context context;
        private List<Piece> pieces;
        private int pieceWidth;
        private int pieceHeight;

        public PieceAdapter(Context context, List<Piece> pieces, int pieceWidth, int pieceHeight) {
            this.context = context;
            this.pieces = pieces;
            this.pieceWidth = pieceWidth;
            this.pieceHeight = pieceHeight;
        }
        @NonNull
        @Override
        public PieceViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            ImageView imageView = new ImageView(context);
            imageView.setLayoutParams(new ViewGroup.LayoutParams(pieceWidth, pieceHeight));
            return new PieceViewHolder(imageView);
        }
        @Override
        public void onBindViewHolder(@NonNull PieceViewHolder holder, int position) {
            holder.imageView.setImageBitmap(pieces.get(position).getBitmap());
        }
        @Override
        public int getItemCount() {
            return pieces.size();
        }
        public class PieceViewHolder extends RecyclerView.ViewHolder {
            ImageView imageView;
            public PieceViewHolder(@NonNull ImageView itemView) {
                super(itemView);
                imageView = itemView;
            }
        }
}

// Class to store the image (piece of puzzle) and it s predetermined position
class Piece {
    public Bitmap bitmap;
    private final int x;
    private final int y;

    public Piece(Bitmap bitmap, int x, int y) {
        this.bitmap = bitmap;
        this.x = x;
        this.y = y;
    }
    public Bitmap getBitmap() {
        return bitmap;
    }
    public int getX() {
        return x;
    }
    public int getY() {
        return y;
    }
}





