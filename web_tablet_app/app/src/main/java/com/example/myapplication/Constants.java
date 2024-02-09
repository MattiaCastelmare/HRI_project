package com.example.myapplication;

public class Constants {
    public static final String TAG = "TABLET OUTPUT:";
    public static final String SERVER_URL = "ws://10.0.2.2:8888/websocket/Tablet"; // STANDARD FOR ANDROID STUDIO
    public static final double scaleParam =  0.9;
    public static final int number_of_pieces = 9;
    public static final int rows =3;
    public static final int cols =3;

    public static final int[] EASY_IMAGES = {
            R.drawable.napoleon,
            R.drawable.starry_night,
            R.drawable.self_portrait
    };

    public static final int[] MEDIUM_IMAGES = {
            R.drawable.iris,
            R.drawable.the_wave,
            R.drawable.crow,
            R.drawable.country_field
    };

    public static final int[] DIFFICULT_IMAGES = {
            R.drawable.kandinsky,
            R.drawable.women,
            R.drawable.bedroom
    };
}

