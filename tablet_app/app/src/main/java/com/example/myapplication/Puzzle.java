//https://dragosholban.com/2018/03/09/how-to-build-a-jigsaw-puzzle-android-game/
package com.example.myapplication;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.graphics.drawable.BitmapDrawable;
import android.util.Log;
import android.util.SparseArray;
import android.view.View;
import android.widget.ImageView;
import android.graphics.BitmapFactory;
import android.view.ViewGroup;
import androidx.recyclerview.widget.RecyclerView;
import androidx.recyclerview.widget.StaggeredGridLayoutManager;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Puzzle {
    int screenWidth, screenHeight;
    int imageHeight, imageWidth;
    int pieceWidth, pieceHeight;
    int count, difficulty;
    int [] chosen_images;
    private static int number_of_pieces;
    private static int rows;
    public static  int cols;
    private final Context context;
    private final Activity parentActivity;
    public final int imageid;
    ArrayList<Piece> pieces;
    PieceAdapter adapter;
    StaggeredGridLayoutManager layoutManager;
    List<Integer> initial_indices = new ArrayList<>();

    public Puzzle(int difficulty, int[] resolution, Context context) {
        this.parentActivity = (MainActivity) context;;
        this.context = context;
        this.screenHeight = resolution[0];
        this.screenWidth = resolution[1];
        this.difficulty = difficulty;
        this.chosen_images = chooseDifficulty(difficulty);
        this.imageid = getRandomImage(chosen_images);
        ResizeImage();
        setRandomImage();
        this.pieces = splitImage();
        addPiecesGrid(pieces);
    }
    public void setRandomImage() {
        // Get the ImageView
        parentActivity.setContentView(R.layout.variable_image_layout);
        ImageView mImageView = parentActivity.findViewById(R.id.intact_image);
        // Set the layout parameters of the ImageView based on image dimensions
        ViewGroup.LayoutParams layoutParams = mImageView.getLayoutParams();
        layoutParams.width = imageWidth;
        layoutParams.height = imageHeight;
        // Set the image
        mImageView.setImageResource(imageid);
    }
    public int getRandomImage(int[] images) {
        // Get a random between 0 and images.length-1
        Random random = new Random();
        int random_id = random.nextInt(images.length);
        Log.d(Constants.TAG, "id: " + random_id);
        Log.d(Constants.TAG, "image: " + images[random_id]);
        // Decode the image to obtain its dimensions
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(context.getResources(), images[random_id], options);
        // Get the dimensions of the image
        imageWidth = options.outWidth;
        imageHeight = options.outHeight;
        Log.d(Constants.TAG, "IMAGE Width: " + imageWidth + ", Height: " + imageHeight);
        return images[random_id];
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
            number_of_pieces = 9;
            rows = 3;
            cols = 3;
            return Constants.EASY_IMAGES;
        } else if (difficulty == 2) {
            number_of_pieces = 9;
            rows = 3;
            cols = 3;
            return Constants.MEDIUM_IMAGES;
        } else if (difficulty == 3) {
            number_of_pieces = 16;
            rows = 4;
            cols = 4;
            return Constants.DIFFICULT_IMAGES;
        } else {
            throw new IllegalArgumentException("Invalid difficulty level: " + difficulty);
        }
    }
    private ArrayList<Piece> splitImage() {
        ArrayList<Piece> pieces = new ArrayList<>(number_of_pieces);
        final ImageView imageView = parentActivity.findViewById(R.id.intact_image);
        BitmapDrawable drawable = (BitmapDrawable) imageView.getDrawable();
        Bitmap bitmap = drawable.getBitmap();
        // scale the image
        Bitmap scaledBitmap = Bitmap.createScaledBitmap(bitmap, imageWidth, imageHeight, true);
        // Compute H W of pieces
        pieceWidth = (imageWidth / cols) - 1;
        pieceHeight = (imageHeight / rows) - 1;
        Log.d(Constants.TAG, "Piece Width: " + pieceWidth);
        Log.d(Constants.TAG, "Piece Height: " + pieceHeight);
        // Create each bitmap piece and add it to the resulting array
        int xCord = 0;
        for (int col = 0; col < cols; col++)  {
            int yCord = 0;
            for (int row = 0; row <rows; row++) {
                //Log.d(Constants.TAG, "X: " + xCord + " Y: " + yCord);
                // Calculate the index based on column-wise counting
                int pieceIndex = col * rows + row;
                Log.d(Constants.TAG, "index: " + pieceIndex + " row: " + row + " col: " + col);
                Piece piece = new Piece(Bitmap.createBitmap(scaledBitmap, xCord, yCord, pieceWidth, pieceHeight), pieceIndex);
                pieces.add(piece);
                yCord += pieceHeight;
            }
            xCord += pieceWidth;
        }
        // Create random indices
        Collections.shuffle(pieces);
        // Save initial indices
        for (int i = 0; i < pieces.size(); i++) {
            int index = pieces.get(i).getIdx();
            initial_indices.add(index);
        }
        return pieces;
    }
    private void addPiecesGrid(ArrayList<Piece> pieces) {
        parentActivity.setContentView(R.layout.activity_main);
        final RecyclerView recyclerView = parentActivity.findViewById(R.id.grid);
        // Create a StaggeredGridLayoutManager with 3 columns
        this.layoutManager = new StaggeredGridLayoutManager(cols, StaggeredGridLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(layoutManager);
        // Create an adapter for the RecyclerView
        this.adapter = new PieceAdapter(context, pieces, pieceWidth, pieceHeight);
        recyclerView.setAdapter(adapter);
        //recyclerView.addItemDecoration(new SpacesItemDecoration(1));
    }
}
 class SpacesItemDecoration extends RecyclerView.ItemDecoration {
        private final int spacing;
        public SpacesItemDecoration(int spacing) {
            this.spacing = spacing;
        }
        @Override
        public void getItemOffsets(Rect outRect,  View view, RecyclerView parent, RecyclerView.State state) {
            outRect.left = spacing;
            outRect.right = spacing;
            outRect.top = spacing;
            outRect.bottom = spacing;
        }
    }

class PieceAdapter extends RecyclerView.Adapter<PieceAdapter.PieceViewHolder> {
    private final Context context;
    private final List<Piece> pieces;
    private final int pieceWidth, pieceHeight;
    private OnItemClickListener listener;
    private View.OnDragListener dragListener;
    private int firstClickedPosition = -1;
    private final SparseArray<ImageView> imageViewMap = new SparseArray<>();

    public PieceAdapter(Context context, List<Piece> pieces, int pieceWidth, int pieceHeight) {
        this.context = context;
        this.pieces = pieces;
        this.pieceWidth = pieceWidth;
        this.pieceHeight = pieceHeight;

    }
    public int getFirstClickedPosition() {
        return firstClickedPosition;
    }
    public View.OnDragListener getDragListener() { return dragListener; }
    public interface OnItemClickListener { void onItemClick(int position) throws InterruptedException; }
    public void setFirstClickedPosition(int position) {
        firstClickedPosition = position;
    }
    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }
    public void setOnDragListener(View.OnDragListener dragListener) { this.dragListener = dragListener; }
    public List<Piece> getPieces() { return pieces; }

    @Override
    public int getItemViewType(int position) { return position; }

    @Override
    public PieceViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        ImageView imageView = new ImageView(context);
        imageView.setLayoutParams(new ViewGroup.LayoutParams(pieceWidth, pieceHeight));
        int paddingInPixels = 4;
        imageView.setPadding(paddingInPixels, paddingInPixels, paddingInPixels, paddingInPixels);
        imageViewMap.put(viewType, imageView); // Update the mapping
        PieceViewHolder viewHolder = new PieceViewHolder(imageView);
        Log.d(Constants.TAG, "viewType: " + viewType);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(PieceViewHolder holder, int position) {
        // Set the position as a tag for the itemView
        holder.itemView.setTag(position);
        Log.d(Constants.TAG, "TAG SET: " + position);
        Piece piece = pieces.get(position);
        holder.imageView.setLongClickable(true);
        holder.imageView.setOnDragListener(dragListener);
        // Set click listener for each item
        holder.itemView.setOnClickListener(view -> {
            if (listener != null) {
                int adapterPosition = holder.getAdapterPosition();
                if (adapterPosition != RecyclerView.NO_POSITION) {
                    try {
                        listener.onItemClick(adapterPosition);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
        // Set long click listener on itemView to initiate the drag operation
        holder.itemView.setOnLongClickListener(view -> {
            // Retrieve the position from the itemView's tag
            Integer tag = (Integer) holder.itemView.getTag();
            //Log.d(Constants.TAG, "DRAGGED IMAGE HAS TAG: " + tag);
            if (tag != null && tag < pieces.size()) {
                View.DragShadowBuilder myShadow = new View.DragShadowBuilder(holder.itemView);
                view.startDrag(null, myShadow, tag, 0);
                return true;
            }
            return false;
        });
        holder.imageView.setImageBitmap(piece.getBitmap());
        // Update the mapping
        imageViewMap.put(position, holder.imageView);
    }

    @Override
    public int getItemCount() { return pieces.size(); }
    public static class PieceViewHolder extends RecyclerView.ViewHolder{
        ImageView imageView;
        public PieceViewHolder( ImageView itemView) {
            super(itemView);
            imageView = itemView;
        }
        public ImageView getImageView() { return imageView; }
    }
}
// Class to store the image (piece of puzzle) and it s predetermined position
class Piece {
    public Bitmap bitmap;
    private final int initial_index;

    public Piece(Bitmap bitmap, int idx) {
        this.bitmap = bitmap;
        this.initial_index = idx;
    }
    public Bitmap getBitmap() {
        return bitmap;
    }
    public int getIdx() {
        return initial_index;
    }
}






