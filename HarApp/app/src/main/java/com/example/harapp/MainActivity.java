package com.example.harapp;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private static final int N_SAMPLES = 200;
    private static List<Float> ElbowFlexion;
    private static List<Float> ElbowSupination;
    private static List<Float> ShoulderFlexion;
    private static List<Float> ShoulderAbduction;
    private static List<Float> ShoulderRotation;

    private TextView Hammer_TextView;
    private TextView Biceps_TextView;
    private TextView Triceps_TextView;
    private TextView Reverse_TextView;

    private float[] results;
    private TensorFlowClassifier classifier;

    private String[] labels = {"HAMMER_CURLS", "BICEPS_CURLS", "TRICEPS_DRUECKEN", "REVERSE_CURLS"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ElbowFlexion = new ArrayList<>();
        ElbowSupination = new ArrayList<>();
        ShoulderFlexion = new ArrayList<>();
        ShoulderAbduction = new ArrayList<>();
        ShoulderRotation = new ArrayList<>();

        Hammer_TextView = (TextView) findViewById(R.id.hammer_prob);
        Biceps_TextView = (TextView) findViewById(R.id.bicurls_prob);
        Triceps_TextView = (TextView) findViewById(R.id.tricurls_prob);
        Reverse_TextView = (TextView) findViewById(R.id.reverse_prob);

        classifier = new TensorFlowClassifier(this);
        addValue();
        activityPrediction();
    }

    /*@Override
    public void onInit(int status) {
        Timer timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
            @Override
            public void run() {
                if (results == null || results.length == 0) {
                    return;
                }
                float max = -1;
                int idx = -1;
                for (int i = 0; i < results.length; i++) {
                    if (results[i] > max) {
                        idx = i;
                        max = results[i];
                    }
                }

                textToSpeech.speak(labels[idx], TextToSpeech.QUEUE_ADD, null, Integer.toString(new Random().nextInt()));
            }
        }, 2000, 5000);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        activityPrediction();
        x.add(event.values[0]);
        y.add(event.values[1]);
        z.add(event.values[2]);
    }*/


    private void activityPrediction() {
        if (ElbowFlexion.size() == N_SAMPLES && ElbowSupination.size() == N_SAMPLES && ShoulderFlexion.size() == N_SAMPLES && ShoulderAbduction.size() == N_SAMPLES && ShoulderRotation.size() == N_SAMPLES) {
            List<Float> data = new ArrayList<>();
            data.addAll(ElbowFlexion);
            data.addAll(ElbowSupination);
            data.addAll(ShoulderFlexion);
            data.addAll(ShoulderAbduction);
            data.addAll(ShoulderRotation);

            results = classifier.predictProbabilities(toFloatArray(data));

            Hammer_TextView.setText(Float.toString(round(results[0], 2)));
            Biceps_TextView.setText(Float.toString(round(results[1], 2)));
            Triceps_TextView.setText(Float.toString(round(results[2], 2)));
            Reverse_TextView.setText(Float.toString(round(results[3], 2)));

            ElbowFlexion.clear();
            ElbowSupination.clear();
            ShoulderFlexion.clear();
            ShoulderAbduction.clear();
            ShoulderRotation.clear();
        }
    }

    private float[] toFloatArray(List<Float> list) {
        int i = 0;
        float[] array = new float[list.size()];

        for (Float f : list) {
            array[i++] = (f != null ? f : Float.NaN);
        }
        return array;
    }

    private static float round(float d, int decimalPlace) {
        BigDecimal bd = new BigDecimal(Float.toString(d));
        bd = bd.setScale(decimalPlace, BigDecimal.ROUND_HALF_UP);
        return bd.floatValue();
    }

    void addValue(){

        for(int i = 0; i < 200; i++){
            ElbowFlexion.add((float) 0.81);
            ElbowSupination.add((float) 0.17);
            ShoulderFlexion.add((float) 0.08);
            ShoulderAbduction.add((float) 0.05);
            ShoulderRotation.add((float) 0.48);
        }


        System.out.println("---------------------");
        System.out.println(ElbowFlexion);
    }
}
