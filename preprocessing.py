import json
import os
import math
import librosa

DATASET_PATH = "./Exports"
JSON_PATH = "data.json"

def save_mfcc(dataset_path, json_path, num_mfcc=13, n_fft=2048, hop_length=1024, num_segments=5):
    # dictionary to store mapping, labels, and MFCCs
    data = {
        "mapping": [],
        "labels": [],
        "mfcc": []
    }

    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
    counter = 0
    for root, dirs, files in os.walk(dataset_path):
        if root is dataset_path:
            for file in files:
                if counter == 10: break
                counter = counter + 1
                file_path = os.path.join(root, file)
                signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)
                mfcc = librosa.feature.mfcc(signal, sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
                mfcc = mfcc.T

                print(counter)
                print(file)
                print(len(mfcc))

                data["mfcc"].append(mfcc.tolist())
                # data["labels"].append(i-1)

    # save MFCCs to json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)
        
        
save_mfcc(DATASET_PATH, JSON_PATH, num_segments=1)