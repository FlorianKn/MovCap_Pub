import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import csv

columns = ['Time','ElbowFlexion','ElbowSupination', 'ShoulderFlexion', 'ShoulderRotation', 'User', 'Label']
df = pd.read_csv('data/alt_data.csv', header = None, names = columns)
df.head()
# Without first header
df = df.iloc[2:]

def plotLabels():
    df['Label'].value_counts().plot(kind='bar', title='Training examples by activity type');
    plt.show()

def plotActivity(label):
    x, eF, eS, sF, sA, sR = [],[],[],[],[],[]	
    counter = 0;
    	
    with open('data/alt_data.csv', 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] != "Time":
                if row[7] == label:
                    x.append(counter)
                    eF.append(float(row[1]))
                    eS.append(float(row[2]))
                    sF.append(float(row[3]))
                    sA.append(float(row[4]))
                    sR.append(float(row[5]))
                    counter += 1;
					
    plt.plot(x, eF)
    plt.plot(x, eS)
    plt.plot(x, sF)
    plt.plot(x, sA)
    plt.plot(x, sR)

    plt.legend(['ElbowFlexion', 'ElbowSupination', 'ShoulderFlexion', 'ShoulderAbduction', 'ShoulderRotation'], loc='lower left')
    plt.show()

print 'Success'
