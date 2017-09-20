from os import listdir
import os
from os.path import isfile, join
from pydub import AudioSegment
import ntpath

# "E:\Monterey Bay 13Aug2017" "24000" "Recorder_1" "Recorder_2" "Recorder_3" "Recorder_5"

# Program Args
# 1. Path of the directory containing the folders with audio files
#   a. Sub directories must have the form (No spaces allowed) ->  NAME_1 or Recorder_1 or Buoy_1 .... Buoy_N
# 2. This argument is the frequency to downsample the files . Ex -> 96000, 48000, 16000 (NO commas)
#   a. You have to enter this argument. If you do not want to down sample files put a zero digit -> 0
# 3. The next arguments are for entering the subdirectories you are going to merge (This is multiple args)
#    Ex. -> "Recorder_1" "Recorder_2" "Recorder_3" "Recorder_5"

def get_recorder_nums(*args):
    nums = []
    for arg in args:
        recorder_num = arg.split('_')
        nums.append(recorder_num[-1])
    print 'Found Recorders', nums
    return nums


def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_wav_files = [f for f in onlyfiles if f.endswith('.wav')]
    return only_wav_files


def write_merged_file(multi_ch_file, output_dir):
    file_handle = multi_ch_file.export(output_dir + "/output.wav", format="wav")

# openFolder('C:\Users\BIOWAVES\Downloads')

def get_single_ch_paths():
    pass

def change_file_name_based_on_recorder(file_name, recorder_num):
    file_name_split = file_name.split('-')
    updated_name = 'D' + recorder_num
    for part in file_name_split[1:]:
        updated_name += '-' + part
    return updated_name

def get_file_path_based_on_folder(working_dir, file_name, folder):
    folder_split = folder.split('_')
    recorder_num = folder_split[-1]
    f = change_file_name_based_on_recorder(file_name, recorder_num)
    other_ch_file = working_dir + '\\' + folder + '\\' + f
    return other_ch_file


def get_all_channel_one_files(working_dir, sample_rate, folders):
    ch_one_folder = folders[0]
    other_channels = folders[1:]
    ch_one_files = get_files(os.path.join(working_dir, ch_one_folder))
    print 'get_all_channel_one_files', ch_one_folder, other_channels, ch_one_files, working_dir
    for ch_one_file in ch_one_files:
        multi_ch_paths = []
        if not ch_one_file.endswith('.wav'):
            pass
        multi_ch_paths.append(working_dir + '\\' + ch_one_folder + '\\' + ch_one_file)
        for ch in other_channels:
            multi_ch_paths.append(get_file_path_based_on_folder(working_dir, ch_one_file, ch))
        print 'Files to merge', multi_ch_paths
        name = path_leaf(multi_ch_paths[0])
        new_name = create_multi_ch_name(name)
        try:
            ch1 = AudioSegment.from_wav(multi_ch_paths[0])
            print 'Got CH1'
            ch2 = AudioSegment.from_wav(multi_ch_paths[1])
            print "Got CH2"
            ch3 = AudioSegment.from_wav(multi_ch_paths[2])
            print "Got CH3"
            ch4 = AudioSegment.from_wav(multi_ch_paths[3])
            print "Got CH4"
        except Exception, e:
            print 'Failed to open a file', e

        try:
            multi = AudioSegment.from_mono_audiosegments(ch1, ch2, ch3, ch4)
            if not sample_rate == "0":
                reduced_multi = multi.set_frame_rate(int(sample_rate))
        except Exception, e:
            print 'Failed to merge files to multi channel', new_name, e

        try:
            file_handle = reduced_multi.export(working_dir + "\\" + "Multichannel_Output\\" + new_name, format="wav")
        except Exception, e:
            print 'Failed to save file ', working_dir + "\\" + "Multichannel_Output\\" + new_name


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)



def create_multi_ch_name(single_ch_name):
    file_name_split = single_ch_name.split('-')
    updated_name = 'M'
    for part in file_name_split[1:]:
        updated_name += '-' + part
    return updated_name

def create_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    import sys
    print(sys.argv)
    print (len(sys.argv))
    working_dir = os.path.join(sys.argv[1])
    print 'Working dir in main', working_dir
    create_output_dir(working_dir + '/Multichannel_Output')
    sample_rate = sys.argv[2]
    args = sys.argv[3:]
    print 'Args', args, args[0], args[1:]
    get_all_channel_one_files(working_dir, sample_rate, args)
