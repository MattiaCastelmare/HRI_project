package com.example.myapplication;

import android.util.Log;

import java.util.HashMap;
import java.util.Map;

public class Constants {
    public static final String TAG = "TABLET OUTPUT:";
    public static final String SERVER_URL = "ws://10.0.2.2:8888/websocket/Tablet"; // STANDARD FOR ANDROID STUDIO
    public static final double scaleParam =  0.9;
    public static final int number_of_pieces = 16;
    public static final int rows =4;
    public static final int cols =4;
    private static HashMap<Integer, String> resourceIdToFileNameMap;


    static {
        initializeResourceMap();
    }

    public static void initializeResourceMap() {
        resourceIdToFileNameMap = new HashMap<>();
        resourceIdToFileNameMap.put(R.drawable.bedroom, "bedroom.jpg");
        resourceIdToFileNameMap.put(R.drawable.country_field, "country_field.jpg");
        resourceIdToFileNameMap.put(R.drawable.crow, "crow.jpg");
        resourceIdToFileNameMap.put(R.drawable.iris, "iris.jpg");
        resourceIdToFileNameMap.put(R.drawable.kandinsky, "kandinsky.jpg");
        resourceIdToFileNameMap.put(R.drawable.napoleon, "napoleon.jpg");
        resourceIdToFileNameMap.put(R.drawable.self_portrait, "self_portrait.jpg");
        resourceIdToFileNameMap.put(R.drawable.starry_night, "starry_night.jpg");
        resourceIdToFileNameMap.put(R.drawable.the_wave, "the_wave.jpg");
        resourceIdToFileNameMap.put(R.drawable.women, "women.jpg");
    }

    public static HashMap<Integer, String> getResourceIdToFileNameMap() {
        return resourceIdToFileNameMap;
    }

    public static String getFileNameFromResourceId(int resourceId) {
        return resourceIdToFileNameMap.get(resourceId);
    }

    public static void printResourceIdsAndNames() {
        HashMap<Integer, String> resourceMap = getResourceIdToFileNameMap();
        for (Map.Entry<Integer, String> entry : resourceMap.entrySet()) {
            int resourceId = entry.getKey();
            String fileName = entry.getValue();
            Log.d(TAG, "Resource ID: " + resourceId + ", File Name: " + fileName);
        }
    }

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

