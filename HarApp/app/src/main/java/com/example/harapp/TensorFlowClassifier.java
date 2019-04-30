package com.example.harapp;

import android.content.Context;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;


public class TensorFlowClassifier {
    static {
        // TODO: Fix bug here
        System.loadLibrary("tensorflow_inference");
    }
    /* USE:
    * https://github.com/curiousily/TensorFlow-on-Android-for-Human-Activity-Recognition-with-LSTMs/tree/master/AndroidApp
    * https://medium.com/@rdeep/tensorflow-lite-tutorial-easy-implementation-in-android-145443ec3775
    * */

    private TensorFlowInferenceInterface inferenceInterface;
    private static final String MODEL_FILE = "converted_model.tflite";
    private static final String INPUT_NODE = "inputs";
    private static final String[] OUTPUT_NODES = {"y_"};
    private static final String OUTPUT_NODE = "y_";
    private static final long[] INPUT_SIZE = {1, 200, 3};
    private static final int OUTPUT_SIZE = 6;

    public TensorFlowClassifier(final Context context) {
        inferenceInterface = new TensorFlowInferenceInterface(context.getAssets(), MODEL_FILE);
    }

    public float[] predictProbabilities(float[] data) {
        float[] result = new float[OUTPUT_SIZE];
        inferenceInterface.feed(INPUT_NODE, data, INPUT_SIZE);
        inferenceInterface.run(OUTPUT_NODES);
        inferenceInterface.fetch(OUTPUT_NODE, result);

        //HAMMER_CURLS, BICEPS_CURLS, TRICEPS_DRUECKEN, REVERSE_CURLS
        return result;
    }
}