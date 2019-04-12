import numpy as np
import pandas as pd

LABELS = np.array([["Label", 1], ["HAMMER_CURLS", 247]])

def readCSV(path):
    arr = np.genfromtxt(path, delimiter=',', dtype=None, encoding=None)
    return arr

# Concat column wise
def concatArrays(arr1, arr2):
    concArr = np.concatenate((arr1, arr2), axis=1)
    return concArr

def addLabels():
    arr = np.array([])

    for label, num in LABELS:
        x = 0;
        r = np.fromstring(num, dtype=int, sep=',')
        for x in range(0, r):
             arr = np.append(arr, label);

    return arr;

# Delete second "time" column
def deleteCol(arr):
    return np.delete(arr,(3), axis=1)

def writeCsv(arr):
    df = pd.DataFrame(arr);
    df.to_csv("data/data.csv", index=False, index_label=False)

# Append column wise
def appendCol(arr1, arr2):
    return np.append(arr1, arr2, axis=1)

# Convert 1d-Array to 2d
def To2d(arr):
    return np.reshape(arr, (-1, 1));

# Delte indices of first line
def deleteFirstLine():
    with open('data/data.csv', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('data/data.csv', 'w') as fout:
        fout.writelines(data[1:])


def main():
    arr1 = readCSV("data/Angles_LeftElbow.csv");
    arr2 = readCSV("data/Angles_LeftShoulder.csv");

    array = concatArrays(arr1, arr2);
    array = deleteCol(array);

    labels = addLabels();
    labels = To2d(labels)

    array = appendCol(array, labels)
    writeCsv(array);
        
    deleteFirstLine();
    print "Success"
main()
