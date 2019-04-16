import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

columns = ['Time','ElbowFlexion','ElbowSupination', 'ShoulderFlexion', 'ShoulderRotation', 'User', 'Label']
df = pd.read_csv('data/data.csv', header = None, names = columns)
df.head()
# Without first header
df = df.iloc[2:]

def plotLabels():
    df['Label'].value_counts().plot(kind='bar', title='Training examples by activity type');
    plt.show()

def plot_activity(activity, df):
    # TODO: plot axis of one specific Label
    PASS
print 'Success'
