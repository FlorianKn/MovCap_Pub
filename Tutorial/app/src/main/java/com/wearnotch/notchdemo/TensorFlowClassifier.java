package com.wearnotch.notchdemo;

import android.content.Context;
import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

public class TensorFlowClassifier {
    static {
        // If following line crashes you might have to download a newer version of libandroid_tensorflow_inference_java.jar
        System.loadLibrary("tensorflow_inference");
    }


    private TensorFlowInferenceInterface inferenceInterface;
    private static final String MODEL_FILE = "file:///android_asset/frozen_har.pb";
    private static final String INPUT_NODE = "X";
    private static final String[] OUTPUT_NODES = {"y_pred_softmax"};
    private static final String OUTPUT_NODE = "y_pred_softmax";
    private static final long[] INPUT_SIZE = {1, 150, 5};
    private static final int OUTPUT_SIZE = 4;

    public TensorFlowClassifier(final Context context) {
        inferenceInterface = new TensorFlowInferenceInterface(context.getAssets(), MODEL_FILE);
    }

    public float[] predictProbabilities(float[] data) {
        float[] result = new float[OUTPUT_SIZE];

        try {

            inferenceInterface.feed(INPUT_NODE, data, INPUT_SIZE);
            inferenceInterface.run(OUTPUT_NODES);
            inferenceInterface.fetch(OUTPUT_NODE, result);

        } catch (Exception e){
            System.out.println("Something went wrong: "+ e);
        }
        return result;
    }
}
