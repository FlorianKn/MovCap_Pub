import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np

eF, eS, sF, sA, sR = [],[],[],[],[]

# Store all lines with same label in one array
def getGestures(label):
    with open('data/data_xxl.csv', 'r') as csvfile:
        plots= csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] != "Time":
                if row[7] == label:
                    eF.append(float(row[1]))
                    eS.append(float(row[2]))
                    sF.append(float(row[3]))
                    sA.append(float(row[4]))
                    sR.append(float(row[5]))

# Divide array in many arrays with length of 30
def divide(a):
    overhead = len(a) % 30
    newArr = a[overhead:]
    newArr = np.array(newArr)
    arr = np.split(newArr, len(newArr)/30)
    return arr;

# Calculate all mean values of the given gesture 
def calcMean(arrays):
    first, sec, third, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    lst = []
    meanValues = []
    for arr in arrays:
        first = first + arr[0]
        sec = sec + arr[1]
        third = third + arr[2]
        e4 = e4 + arr[3]
        e5 = e5 + arr[4]
        e6 = e6 + arr[5]
        e7 = e7 + arr[6]
        e8 = e8 + arr[7]
        e9 = e9 + arr[8]
        e10 = e10 + arr[9]
        e11 = e11 + arr[10]
        e12 = e12 + arr[11]
        e13 = e13 + arr[12]
        e14 = e14 + arr[13]
        e15 = e15 + arr[14]
        e16 = e16 + arr[15]
        e17 = e17 + arr[16]
        e18 = e18 + arr[17]
        e19 = e19 + arr[18]
        e20 = e20 + arr[19]
        e21 = e21 + arr[20]
        e22 = e22 + arr[21]
        e23 = e23 + arr[22]
        e24 = e24 + arr[23]
        e25 = e25 + arr[24]
        e26 = e26 + arr[25]
        e27 = e27 + arr[26]
        e28 = e28 + arr[27]
        e29 = e29 + arr[28]
        e30 = e30 + arr[29]
		

    lst.extend((first, sec, third, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30));
    for val in lst:
        mean = val / len(lst)
        meanValues.append(mean)
    return meanValues



def mean(label):
    getGestures(label);
    elbowFlex = divide(eF);
    elbowSup = divide(eS);
    shoulderFlex = divide(sF);
    shoulderAb = divide(sA);
    shoulderRot = divide(sR);

    mEF  = calcMean(elbowFlex)
    mES  = calcMean(elbowSup)
    msF  = calcMean(shoulderFlex)
    msA  = calcMean(shoulderAb)
    msR  = calcMean(shoulderRot)
	
    #plt.legend(['ElbowFlexion', 'ElbowSupination', 'ShoulderFlexion', 'ShoulderAbduction', 'ShoulderRotation'], loc='lower left')
    #plt.plot(mEF)
    #plt.plot(mES)
    #plt.plot(msF)
    #plt.plot(msA)
    #plt.plot(msR)
    #plt.show()
    mEF.insert(0,"ElbowFlexion")
    mES.insert(0,"ElbowSupination")
    msF.insert(0,"ShoulderFlexion")
    msA.insert(0,"ShoulderAbduction")
    msR.insert(0,"ShoulderRotation")
    allMeans = [[]]
    allMeans.extend((mEF, mES, msF, msA, msR));

    csvName = label + "_mean.csv" 
    df = pd.DataFrame(allMeans);

    df.to_csv(csvName, index=False, index_label=False)

