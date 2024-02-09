//https://dragosholban.com/2018/03/09/how-to-build-a-jigsaw-puzzle-android-game/
package com.example.myapplication;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.util.Log;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.graphics.BitmapFactory;
import android.view.ViewGroup;
import java.util.ArrayList;

public class Puzzle {
    int screenWidth;
    int screenHeight;
    int imageHeight;
    int imageWidth;
    int random_id;
    private Context context;
    private Activity parentActivity;
    int difficulty;
    int count;
    ArrayList<Piece> pieces;

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
            count+=1;
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
        ImageView imageView = parentActivity.findViewById(R.id.intact_image);
        BitmapDrawable drawable = (BitmapDrawable) imageView.getDrawable();
        Bitmap bitmap = drawable.getBitmap();
        // scale the image
        Bitmap scaledBitmap = Bitmap.createScaledBitmap(bitmap, imageWidth, imageHeight, true);
        // Compute H W of pieces
        int pieceWidth  = (imageWidth/Constants.cols)-1;
        int pieceHeight = (imageHeight/Constants.rows)-1;
        Log.d(Constants.TAG, "Piece Width: " + pieceWidth);
        Log.d(Constants.TAG, "Piece Height: " + pieceHeight);
        // Create each bitmap piece and add it to the resulting array
        int yCord = 0;
        for (int row = 0; row < Constants.rows; row++) {
            int xCord = 0;
            for (int col = 0; col < Constants.cols; col++) {
                Piece piece = new Piece(bitmap.createBitmap(scaledBitmap, xCord, yCord, pieceWidth, pieceHeight),xCord,yCord,pieceWidth,pieceHeight);
                pieces.add(piece);
                xCord += pieceWidth;
                Log.d(Constants.TAG, "X: " + xCord);
            }
            yCord += pieceHeight;
            Log.d(Constants.TAG, "Y: " + yCord);
        }
        return pieces;
    }
    private void addPiecesGrid(ArrayList<Piece> pieces) {
        parentActivity.setContentView(R.layout.grid);
        final GridLayout layout = parentActivity.findViewById(R.id.grid);
        for (Piece piece : pieces) {
            Bitmap bitmap = piece.getBitmap();
            int x = piece.getX();
            int y = piece.getY();
            ImageView iv = new ImageView(context);
            iv.setImageBitmap(bitmap);
            // Set the x and y coordinates using GridLayout.LayoutParams
            GridLayout.LayoutParams params = new GridLayout.LayoutParams();
            params.rowSpec = GridLayout.spec(x);
            params.columnSpec = GridLayout.spec(y);
            iv.setLayoutParams(params);
            layout.addView(iv);
        }
    }
}

// Class to store the image (piece of puzzle) and it s predetermined position
class Piece {
    public Bitmap bitmap;
    private int x;
    private int y;

    public Piece(Bitmap bitmap, int x, int y, int w, int h) {
        this.bitmap = bitmap;
        this.x = x + w;
        this.y = y + h;
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





