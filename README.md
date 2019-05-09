# MovCap
Capture and classify movements with NN 
## Explore dataset  
`python -c "from plot import plotLabels; print plotLabels()"`  
![Fig1](data/fig/fig1.png)  

`python -c "from plot import plotActivity; print plotActivity('HAMMER_CURLS')"`  
![Fig2](data/fig/fig2.png) 
## Prepare notch data  
Each notch sensor stores its data in one csv file. To put those files in an appropriate format *prepareNotchData.py* can be used. Before running the script adapt the following lines in *prepareNotchData.py*:  
```python
USERS = np.array([["User", 1], ["1", 200], ["2", 47]])  
# ["userID", number of rows userID should be attached to]
LABELS = np.array([["Label", 1], ["HAMMER_CURLS", 100], ["BICEPS_CURLS", 50], ["TRICEPS_DRUECKEN", 50], ["REVERSE_CURLS", 47]])  
# ["Label", number of rows Label should be attached to]
```  
Afterwards run `python prepareNotchData.py`.  
## Train model  
Run `python activity_recognition.py` to train and test the model.  
After running the script results (accuracy, loss and graphs) are displayed on TensorBoard.  
Run `tensorboard --logdir=data/summary`
## Export model to Android  
Run `python freezeModel.py` to freeze the model.  
Copy the generated `frozen_har.pb` into the asset folder of an android-studio project.  
  
Most important part can be seen below:

```java
private TensorFlowInferenceInterface inferenceInterface;
private static final String MODEL_FILE = "file:///android_asset/frozen_har.pb";
private static final String INPUT_NODE = "X";
private static final String[] OUTPUT_NODES = {"y_pred_softmax"};
private static final String OUTPUT_NODE = "y_pred_softmax";
private static final long[] INPUT_SIZE = {1, 180, 5};
private static final int OUTPUT_SIZE = 4;

public TensorFlowClassifier(final Context context) {
inferenceInterface = new TensorFlowInferenceInterface(context.getAssets(), MODEL_FILE);
}
// Make predictions
public float[] predictProbabilities(float[] data) {
float[] result = new float[OUTPUT_SIZE];

try {
    inferenceInterface.feed(INPUT_NODE, data, INPUT_SIZE);
    inferenceInterface.run(OUTPUT_NODES);
    inferenceInterface.fetch(OUTPUT_NODE, result);
} catch (Exception e){
    System.out.println(e);
}
return result;
}
```  
*Note if you have problems with libandroid_tensorflow_inference_java.jar you might need to update it: https://bintray.com/google/tensorflow/tensorflow#files/org%2Ftensorflow%2Ftensorflow-android. The package is called tensorflow-android-1.9.0.aar*  
  
The screen of the app can be seen below:  
  
![App](data/fig/app_screen.png) 


