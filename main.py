from os import listdir
import os
from os.path import isfile, join
from pydub import AudioSegment
import sys
import ntpath

def main(args):
    pass

# ch1 = AudioSegment.from_wav(cur_dir + "\D1-170813-153000.wav")
# ch2 = AudioSegment.from_wav(cur_dir + '\D2-170813-153000.wav')
# multi = AudioSegment.from_mono_audiosegments(ch1, ch2)
# file_handle = multi.export(cur_dir + "\output.wav", format="wav")



def get_recorder_nums(*args):
    nums = []
    for arg in args:
        recorder_num = arg.split('_')
        nums.append(recorder_num[-1])
    print 'Found Recorders', nums
    return nums


def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles


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


def get_all_channel_one_files(working_dir, folders):
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
            ch2 = AudioSegment.from_wav(multi_ch_paths[1])
            ch3 = AudioSegment.from_wav(multi_ch_paths[2])
            ch4 = AudioSegment.from_wav(multi_ch_paths[3])
            multi = AudioSegment.from_mono_audiosegments(ch1, ch2, ch3, ch4)
            file_handle = multi.export(working_dir + "\\" + "Multichannel_Output\\" + new_name, format="wav")
        except:
            print 'Failed to merge files', new_name


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
    args = sys.argv[2:]
    print 'Args', args, args[0], args[1:]
    get_all_channel_one_files(working_dir, args)
    recorder_nums = get_recorder_nums(*args)
    print 'Main Method', recorder_nums
    main(args)