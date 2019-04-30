import numpy as np
import pandas as pd

USERS = np.array([["User", 1], ["1", 200], ["2", 47]]) # ["userID", number of rows userID should be attached]
LABELS = np.array([["Label", 1], ["HAMMER_CURLS", 100], ["BICEPS_CURLS", 50], ["TRICEPS_DRUECKEN", 50], ["REVERSE_CURLS", 47]]) # ["Label", number of rows Label should be attached]
NEW_HEADER = np.array([["Time","ElbowFlexion", "ElbowSupination", "ShoulderFlexion", "ShoulderAbduction", "ShoulderRotation", "User", "Label"]])

def readCSV(path):
    arr = np.genfromtxt(path, delimiter=',', dtype=None)#, encoding=None)
    return arr

# Concat column wise
def concatArrays(arr1, arr2):
    concArr = np.concatenate((arr1, arr2), axis=1)
    return concArr

# Concat row wise
def concatArraysRow(arr1, arr2):
    concArr = np.concatenate((arr1, arr2), axis=0)
    return concArr

# Add labels or users
def addLabUsr(ARR):
    arr = np.array([])

    for label, num in ARR:
        x = 0;
        r = np.fromstring(num, dtype=int, sep=',')
        for x in range(0, r):
             arr = np.append(arr, label);

    return arr;

# Delete second "time" column
def deleteCol(arr):
    return np.delete(arr,(3), axis=1)

# Delete old header
def deleteHeader(arr):
    return np.delete(arr,(0), axis=0)

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

    users = addLabUsr(USERS);
    users = To2d(users)
    labels = addLabUsr(LABELS);
    labels = To2d(labels)

    array = appendCol(array, users)
    array = appendCol(array, labels)
    array = deleteHeader(array)
    # Set new header here
    array = concatArraysRow(NEW_HEADER, array)
    writeCsv(array);

    deleteFirstLine();
    print "Success"
main()
