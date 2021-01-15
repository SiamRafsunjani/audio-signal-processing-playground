from pydub import AudioSegment
from pydub.playback import play
import os 
import random
import string

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
                mixedFile.append(file, crossfade=random.randint(minCrossfade, maxCrossfade))
            else:
                mixedFile = file + mixedFile

        mixedFile = file 

    return mixedFile

def exportSamples( files ):
    for file in files:
        file.export(random.choice() + '.mp3', format="mp3")

# Takes an array of sound path and creates a random crossfade 
# with random time interval
# paths             = array of file names  
# samplesToCreate   = number of mixes to create 
# numberOfPersons   = max number of files to take in a mix 
# bufferCount       = Other class buffer. 
# mixCrossfade, maxCrossfade = min max crossfade time
def CreateSamples( paths, samplesToCreate, numberOfPersons, bufferCount, minCrossfade, maxCrossfade ):
    counterOther, counterMain, state = 0, 0, 0
    generatedFiles = []
    for i in range(samplesToCreate):
        samplesToTake = random.randint(1, numberOfPersons + bufferCount)
        if samplesToTake > numberOfPersons: counterOther = counterOther + 1
        else: counterMain = counterMain + 1

        if state + samplesToTake > len(paths): state = 0

        slicedFiles = paths[state: state+samplesToTake]
        state = state + samplesToTake
        
        generatedFiles.append( CreateCrossFade(slicedFiles, minCrossfade, maxCrossfade) )


    print("Other " + str( counterOther ))
    print("Main " +  str( counterMain ))
    return generatedFiles


paths = ReadDataset('Dataset', 2)
samples = CreateSamples(paths, 20, 5, 2, 0, 3)
exportSamples(samples)

