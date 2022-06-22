from contextlib import closing
import csv
import glob
import os
import pprint
import re
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

# wav file handling
import scipy.io.wavfile as sio_wavfile

import textgrids

pp = pprint.PrettyPrinter(indent=4)

def write_fav_input(table, filename):
    # Finally dump all the metadata into a csv-formated file to
    # be read by FAVE.
    with closing(open(filename, 'w')) as csvfile:
        fieldnames = ['id', 'speaker', 'begin', 'end', 'word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, 
                                delimiter='\t', quoting=csv.QUOTE_NONE,
                                extrasaction='ignore')

        map(writer.writerow, table)

    print("Wrote file " + filename + " for FAVE align.")


def write_results(table, filename):
    # Finally dump all the metadata into a csv-formated file to
    # be read by Python or R.
    with closing(open(filename, 'w')) as csvfile:
        fieldnames = ['id', 'speaker', 'sliceBegin', 'beep', 'begin', 'end', 'word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        map(writer.writerow, table)

    print("Wrote file " + filename + " for R/Python.")


def read_pronunciation_dict(filename):
    """
    Read the pronuciation dictionary and return it as a dict.

    The file is assumed to be in tab separated format and to 
    contain one word on each line followed by the X-SAMPA transcription
    of the expected pronunciation (phonological transcription).

    Returns a dict where each entry is a list of phonomes.
    """
    pronunciation_dict = {}
    if os.path.isfile(filename):
        with closing(open(filename, 'r')) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            pronunciation_dict = {row[0]: row[1:] for row in reader}
        return pronunciation_dict
    else:
        print("Didn't find {pronunciation_dict}. Exiting.")
        sys.exit()


def write_concatenated_textgrid(table, filename, dirname):
    print(table)
    print(filename)
    print("textgrids does not yet support all the operations we need. work on that.")

    pronunciation_dict = read_pronunciation_dict(os.path.join(dirname, 
                                                'pronunciation_dict.csv'))

def read_na_list(dirname):
    """
    Read the exclusion list from na_list.txt.
    
    If no exclusioin list file is present, return an empty array
    after warning the user.
    """
    na_file = os.path.join(dirname, 'na_list.txt')
    if os.path.isfile(na_file):
        na_list = [line.rstrip('\n') for line in open(na_file)]
    else:
        na_list = []
        print("Didn't find na_list.txt. Proceeding anyhow.")
    return na_list


def processWavFile(table_entry, wav_file, filename, prompt_file, uti_file, 
                    na_list, output, samplerate, number_of_channels, cursor):
    if filename in na_list:
        print('Skipping {filename}: Token is in na_list.txt.', filename=filename)
        return
    elif not os.path.isfile(uti_file):
        print ('Skipping {filename}. Token has no ultrasound data.', 
            filename=filename)
        return
        
    with closing(open(prompt_file, 'r')) as prompt_file:
        line = prompt_file.readline().strip()
        line = " ".join(re.findall("[a-zA-Z]+", line))
        if line == 'water swallow' or line == 'BITE PLANE':
            print('Skipping {file} is a {prompt}', file=prompt_file, prompt=line)
            return

        table_entry['word'] = line

    (next_samplerate, frames) = sio_wavfile.read(wav_file)
    n_frames = frames.shape[0]
    n_channels = frames.shape[1]

    if next_samplerate != samplerate:
        print('Mismatched sample rates in sound files.')
        print("{next_samplerate} in {infile} is not the common one: {samplerate}", 
            next_samplerate=next_samplerate, infile=wav_file, samplerate=samplerate)
        print('Exiting.')
        exit()

    if n_channels != number_of_channels:
        print('Mismatched numbers of channels in sound files.')
        print("{n_channels} in {infile} is not the common one: {number_of_channels}", 
            n_channels=n_channels, infile=wav_file, number_of_channels=number_of_channels)
        print('Exiting.')
        exit()

    duration = n_frames / float(samplerate)

    # this rather than full path to avoid upsetting praat/FAV
    table_entry['id'] = filename

    table_entry['sliceBegin'] = cursor

    # give fav the stuff from 1.5s after the audio recording begins
    table_entry['begin'] = cursor + 1.5 

    cursor += duration
    table_entry['end'] = round(cursor, 3)

    # TODO: does this actually append rather than overwrite?
    sio_wavfile.write(output, samplerate, frames)

    return cursor


def concatenateWavs(dirname, outfilename, speaker_id):
    wav_files = glob.glob(os.path.join(dirname, '*.wav')) 

    if(len(wav_files) < 1):
        print("Didn't find any sound files to concatanate in \'"+dirname+"\'.")
        exit()

    # Split first to get rid of the suffix, then to get rid of the path.
    filenames = [filename.split('.')[-2].split('/').pop() 
                 for filename in wav_files]

    # initialise table with the speaker_id and name repeated, wav_file name
    # from the list, and other fields empty
    table = [{
                'wav_path': wavfile,
                'id':'n/a',
                'speaker':speaker_id, 
                'sliceBegin':'n/a',
                'beep':'n/a',
                'begin':'n/a', 
                'end':'n/a', 
                'word':'n/a'} 
             for i, wavfile in  enumerate(wav_files)]

    prompt_files = glob.glob(os.path.join(dirname, '*.txt')) 

    if(len(prompt_files) < 1):
        print("Didn't find any prompt files.")
        exit()
    else:
        # ensure one to one correspondence between wavs and prompts 
        prompt_files = [os.path.join(dirname, filename) + '.txt'
                       for filename in filenames]

    na_list = read_na_list(dirname)

    outwave = outfilename + ".wav"
    outfav = outfilename + ".txt"
    outcsv = outfilename + ".csv"
    out_textgrid = outfilename + ".TextGrid"
    
    uti_files = [os.path.join(dirname, filename) + '.ult' 
                 for filename in filenames]
    
    # find params from first file
    (samplerate, test_data) = sio_wavfile.read(wav_files[0])
    number_of_channels = test_data.shape[1]

    cursor = 0.0
    with closing(outwave, 'w') as output:
        for i in range(len(wav_files)):
            cursor = processWavFile(table[i], wav_files[i], filenames[i], 
                    prompt_files[i], uti_files[i], 
                    na_list, output, samplerate, number_of_channels, cursor)

    # Weed out the skipped ones before writing the data out.
    table = [token for token in table if token['id'] != 'n/a']
    write_fav_input(table, outfav)
    write_results(table, outcsv)
    write_concatenated_textgrid(table, out_textgrid, dirname)
    #pp.pprint(table)


def main(args):
    outfilename = args.pop()
    original_dirname = args.pop()
    speaker_id = args.pop()
    concatenateWavs(speaker_id, original_dirname, outfilename)


if (len(sys.argv) != 4):
    print("\nex1_concat.py")
    print("\tusage: ex1_concat.py speaker_id original_directory outputfilename")
    print("\n\tConcatenates wav files from AAA.")
    print("\tWrites a huge wav-file and a .txt for potential input to FAVE.")
    print("\tAlso writes a richer metafile to be read by ex1_extract.py or similar.")
    sys.exit(0)


if (__name__ == '__main__'):
    t = time.time()
    main(sys.argv[1:])
    print('Elapsed time {elapsed_time}', elapsed_time = (time.time() - t))


