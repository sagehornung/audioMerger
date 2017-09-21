from os import listdir
import os
from os.path import isfile, join
from pydub import AudioSegment
import ntpath
import sys
import ConfigParser
import logging


def config_section_map(section):
    config_dict = {}
    options = Config.options(section)
    for option in options:
        try:
            config_dict[option] = Config.get(section, option)
            if config_dict[option] == -1:
                logging.debug("skip: %s" % option)
        except:
            logging.error("exception on %s!" % option)
            config_dict[option] = None
    return config_dict


# "E:\Monterey Bay 13Aug2017" "24000" "Recorder_1" "Recorder_2" "Recorder_3" "Recorder_5"

# Program Args
# 1. Path of the directory containing the folders with audio files
#   a. Sub directories must have the form (No spaces allowed) ->  NAME_1 or Recorder_1 or Buoy_1 .... Buoy_N
# 2. This argument is the frequency to downsample the files . Ex -> 96000, 48000, 16000 (NO commas)
#   a. You have to enter this argument. If you do not want to down sample files put a zero digit -> 0
# 3. The next arguments are for entering the subdirectories you are going to merge (This is multiple args)
#    Ex. -> "Recorder_1" "Recorder_2" "Recorder_3" "Recorder_5"


def get_valid_recorder_nums(files_list):
    rec_nums = ''
    for f in files_list:
        f = path_leaf(f)
        f = f.split("-")
        f = f[0]
        f = f[1:]
        rec_nums += f
    return rec_nums

def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_wav_files = [f for f in onlyfiles if f.endswith('.wav')]
    return only_wav_files


def change_file_name_based_on_folder(file_name, dir_num):
    file_name_split = file_name.split('-')
    updated_name = 'D' + dir_num
    for part in file_name_split[1:]:
        updated_name += '-' + part
    return updated_name


def get_file_path_based_on_folder(base_dir, file_name, folder):
    folder_split = folder.split('_')
    recorder_num = folder_split[-1]
    f = change_file_name_based_on_folder(file_name, recorder_num)
    other_ch_file = base_dir + '\\' + folder + '\\' + f
    return other_ch_file


def validate_file_list(files):
    valid_files = []
    for f in files:
        if file_exists(f):
            valid_files.append(f)
    return valid_files


def build_single_ch_file_list(project_dir, file_name, dirs):
    file_paths = []
    for d in dirs:
        file_paths.append(get_file_path_based_on_folder(project_dir, file_name, d))
    return file_paths


def merge_audio_files(project_dir, ch_one_files, dir_list):

    for recording in ch_one_files:
        paths_list = build_single_ch_file_list(project_dir, recording, dir_list)
        logging.info('Validating files %s' % paths_list)
        valid_paths = validate_file_list(paths_list)

        logging.info('Found %s valid matching files for %s' % (len(valid_paths), recording))

        if len(valid_paths) < len(paths_list):
            logging.warning('Found less valid files (%s) than recording folders (%s) %s' % (len(valid_paths), len(paths_list), valid_paths))
        if len(valid_paths) < int(script_params["minnumfilesformerge"]):
            logging.warning('Not enough files to merge, skipping: %s' % recording)
            continue

        try:
            audio_segs = load_audio_segments(valid_paths)
            logging.info('Success loading audio segments: %s' % valid_paths)
        except Exception, e:
            logging.error('Error loading an audio segment %s', e)
            continue

        if script_params["downsampleaudio"]:
            try:
                audio_segs = [down_sample_audio(f) for f in audio_segs]
            except Exception, e:
                logging.error('Error down sampling audio %s', e)
                continue
        try:
            multi = AudioSegment.from_mono_audiosegments(*audio_segs)
            logging.info('Success merging mono audio segments: %s' % valid_paths)
        except Exception, e:
            logging.error('Failed to merge mono audio segments for file %s, Error: %s' % (recording, e))
            continue

        folders_used = get_valid_recorder_nums(valid_paths)
        save_name = create_multi_ch_name(recording, folders_used)

        write_file_to_disk(multi, save_name)


def write_file_to_disk(multi, filename):
    try:
        file_handle = multi.export(os.path.join(output_dir_path, filename), format="wav")
        logging.info('Successfully saved multi-channel file: %s' % filename)
    except Exception, e:
        logging.error('Failed to save multi-channel file: %s Error: %s' % (filename, e))


def load_audio_segments(files_list):
    return [AudioSegment.from_wav(segment) for segment in files_list]


def down_sample_audio(audio_file):
    sample_rate = int(script_params["samplerate"])
    logging.info('Attempting to convert audio to sample rate %s' % sample_rate)
    reduced_audio_file = audio_file.set_frame_rate(sample_rate)
    logging.info('Success down sampling audio %s' % sample_rate)
    return reduced_audio_file


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def create_multi_ch_name(single_ch_name, folders_used):
    file_name_split = single_ch_name.split('-')
    updated_name = 'M' + folders_used
    for part in file_name_split[1:]:
        updated_name += '-' + part
    return updated_name


def create_output_dir():
    output_dir = "Multichannel_Output"
    if script_params["downsampleaudio"]:
        output_dir += "_" + str(script_params["samplerate"])
    project_dir = script_params["projectdirpath"]
    path = os.path.join(project_dir, output_dir)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logging.info("Successfully created output directory at: %s" % path)
        except Exception, e:
            logging.error("%s" % e)
            return None
    return path


def get_output_dir_name():
    if script_params["downsampleaudio"]:
        return "Multichannel_Output_" + str(script_params["samplerate"])
    return "Multichannel_Output"


def file_exists(fname):
    return os.path.isfile(fname)


def get_dirs_from_config(dirs_str):
    return [dir_name.strip() for dir_name in dirs_str.split(',')]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    Config = ConfigParser.ConfigParser()
    cwd = os.getcwd()
    config_file = os.path.join(cwd, "config.ini")
    Config.read(config_file)

    script_params = config_section_map("ScriptParams")
    output_dir_path = create_output_dir()
    logging.info('Saving files in directory: %s at sample rate: %s' % (output_dir_path, script_params["samplerate"]))

    audio_dirs = config_section_map("Directories")
    dir_list = get_dirs_from_config(audio_dirs['dirnames'])
    logging.info('Found the following audio directories in config file %s' % dir_list)

    project_dir = script_params["projectdirpath"]
    ch_one_files = get_files(os.path.join(project_dir, dir_list[0]))
    logging.info('NumFiles: %s .wav file/s found in directory: %s' % (len(ch_one_files), dir_list[0]))

    merge_audio_files(project_dir, ch_one_files, dir_list)

