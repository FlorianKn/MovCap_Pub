package com.example.harapp;

import android.app.Activity;
import android.content.Context;
import android.content.res.AssetFileDescriptor;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;
import org.tensorflow.lite.Interpreter;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;


public class TensorFlowClassifier {
    static {
        System.loadLibrary("tensorflow_inference");
    }
    /* USE:
    * https://github.com/curiousily/TensorFlow-on-Android-for-Human-Activity-Recognition-with-LSTMs/tree/master/AndroidApp
    * https://medium.com/@rdeep/tensorflow-lite-tutorial-easy-implementation-in-android-145443ec3775
    * */

    private TensorFlowInferenceInterface inferenceInterface;
    private static final String MODEL_FILE = "file:///android_asset/frozen_har.pb";
    private static final String INPUT_NODE = "X";
    private static final String[] OUTPUT_NODES = {"y_pred_softmax"};
    private static final String OUTPUT_NODE = "y_pred_softmax";
    private static final long[] INPUT_SIZE = {1, 200, 5};
    private static final int OUTPUT_SIZE = 4;
    //Interpreter tflite;

    public TensorFlowClassifier(final Context context) {
        inferenceInterface = new TensorFlowInferenceInterface(context.getAssets(), MODEL_FILE);
    }
   /*public TensorFlowClassifier(Activity activity) {
       try {
           tflite = new Interpreter(loadModelFile(activity, MODEL_FILE));
       }
       catch (IOException e) {
           e.printStackTrace();
       }
   }*/



    public float[] predictProbabilities(float[] data) {
        float[] result = new float[OUTPUT_SIZE];

        inferenceInterface.feed(INPUT_NODE, data, INPUT_SIZE);
        inferenceInterface.run(OUTPUT_NODES);
        //inferenceInterface.fetch(OUTPUT_NODE, result);


        //tflite.run(data, result);
        //HAMMER_CURLS, BICEPS_CURLS, TRICEPS_DRUECKEN, REVERSE_CURLS
        return result;
    }


    /*private MappedByteBuffer loadModelFile(Activity activity, String MODEL_FILE) throws IOException {
        AssetFileDescriptor fileDescriptor = activity.getAssets().openFd(MODEL_FILE);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }*/
}