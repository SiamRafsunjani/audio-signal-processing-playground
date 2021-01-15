from pydub import AudioSegment
from pydub.playback import play
import os 
import random
import string
import pandas as pd 

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def AddAmbientSound(path, ):
    print("TODO")

# Python 3 walk into folder with specific level  
# and returns an array of found locations 
# Folder structure used is the default of Bangali ASR dataset
def ReadDataset(location, level):
    paths = []
    counter = 0
    for root, dirs, files in os.walk(location):
        path = root.split(os.sep)
        if len(path) == level:
            for name in files:
                paths.append('./'+ '/'.join(path) + '/' + name)
                counter = counter + 1
    print("Found " + str(counter) + " Files")
    return paths

def CreateCrossFade( paths, minCrossfade, maxCrossfade ):
    mixedFile = None
    for path in paths:
        chance = random.randint(0, 100)
        file = AudioSegment.from_file( path, "flac" )
        if mixedFile is not None:
            if chance > 50:
                if (file.duration_seconds * 1000) > 1000: 
                    fadeIn = 1000
                else: 
                    fadeIn = 0

                mixedFile = mixedFile.append(file, crossfade=fadeIn)
            else:
                mixedFile = mixedFile + file

        else:
            mixedFile = file

            

    return mixedFile

def exportSample( file ):
    name = get_random_string(8) + '.mp3'
    file.export('./Exports/' + name, format="mp3")
    return name

# Takes an array of sound path and creates a random crossfade 
# with random time interval
# paths             = array of file names  
# samplesToCreate   = number of mixes to create 
# numberOfPersons   = max number of files to take in a mix 
# bufferCount       = Other class buffer. 
# mixCrossfade, maxCrossfade = min max crossfade time
def CreateSamples( paths, samplesToCreate, numberOfPersons, bufferCount, minCrossfade, maxCrossfade ):
    counterOther, counterMain, state = 0, 0, 0
    generatedFiles, personCount, filesAppended, samples = [], [], [], []

    for i in range(samplesToCreate):
        samplesToTake = random.randint(1, numberOfPersons + bufferCount)
        if samplesToTake > numberOfPersons: counterOther = counterOther + 1
        else: counterMain = counterMain + 1

        if state + samplesToTake > len(paths): state = 0

        slicedFiles = paths[state: state+samplesToTake]
        state = state + samplesToTake
        
        generatedFiles.append( CreateCrossFade(slicedFiles, minCrossfade, maxCrossfade) )
        personCount.append(samplesToTake)
        filesAppended.append(','.join(slicedFiles))

    print("Other " + str( counterOther ))
    print("Main " +  str( counterMain ))
    
    for index, file in enumerate(generatedFiles):
        sample = {}
        sample['name'] = exportSample(file)
        sample['class'] = personCount[index]
        sample['files'] = filesAppended[index]
        samples.append(sample)
    
    df = pd.DataFrame(samples)
    df.to_csv('./Exports/description.csv')    



paths = ReadDataset('Dataset', 2)
CreateSamples(paths, 20000, 5, 2, 0, 4)

# file = AudioSegment.from_file( '36a2c0f7dc.flac', "flac" )
# print( file.duration_seconds )