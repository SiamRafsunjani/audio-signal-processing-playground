import json
import os
import math
import librosa
import pandas as pd
import sys 

DATASET_PATH = "./" + sys.argv[1]
JSON_PATH = './' + sys.argv[2] + ".json"
LABEL_PATH = "./description.csv"

print(JSON_PATH)

def save_mfcc(dataset_path, json_path, num_mfcc=7, n_fft=2048, hop_length=1024, num_segments=5):
    # dictionary to store labels, and MFCCs
    data = {
        "mfcc": [],
        "labels": []
    }

    labels = pd.read_csv(LABEL_PATH)
    counter = 0
    for root, dirs, files in os.walk(dataset_path):
        if root is dataset_path:
            for file in files:                
                counter = counter + 1
                if counter > 40000: break 

                file_path = os.path.join(root, file)
                signal, sample_rate = librosa.load(file_path, sr=None)
                mfcc = librosa.feature.mfcc(signal, sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
                mfcc = mfcc.T

                print(counter)

                data["mfcc"].append([mfcc.tolist()])
                data["labels"].append(int( labels.loc[labels['name'] == file]['class'] ) )

    # save MFCCs to json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)
        
save_mfcc(DATASET_PATH, JSON_PATH, num_segments=1)