import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import csv
from datetime import datetime
from datetime import timedelta
import subprocess
import os
import time

# Here is a list of arguments to pass to the script
# 1. Location of the directory to watch containing the Ishmael log.txt file
# 2. Location of .arr file
# 3. Duration of audio files
# 4. Location of the FOLDER containing the FOLDERS with the GPS files
# 5. Add as many folder names as you like that contain GPS file -- Ex: Recorder_1 Recorder_2 ... Recorder_N


class Event(LoggingEventHandler):

    def dispatch(self, event):
        print "Watchdog file event: ", event
        event_str = str(event)
        fn = ''
        et = ''
        if event_str.startswith('<FileModifiedEvent:') and event_str.endswith("ish_log.txt'>"):
            print 'ish_log.txt modified'
            try:
                fn, et = parse_log_file(event_str)
            except Exception, e:
                print 'Error parsing ishmeal log file', e

            working_dir = os.path.join(sys.argv[4])
            recorder_dirs = sys.argv[5:]
            print "Extracting data from directories (Args passed to program): ", recorder_dirs
            duration = int(sys.argv[3])
            if not fn == '' and not et == '':
                print 'Calling buld array with params', working_dir, et, fn, recorder_dirs, duration
                build_arr_file(working_dir, et, fn, recorder_dirs, duration)
            else:
                print 'Not building .arr file'

            # build_arr_file(working_dir, elapsed_time, fn, recorder_dirs, wav_file_len_in_mins):
    # def on_modified(self, event):
    #     print("Doh", event)


def write_to_array_file(listdata):
    # arr_path = 'C:\Users\BIOWAVES\PycharmProjects\\audioMerger\\test\\tmp\myfile.arr'
    try:
        arr_path = os.path.join(sys.argv[2])
        print "This is the .arr file path", arr_path, 'Arr Data: ', listdata
        f = open(arr_path, 'w')
        for item in listdata:
            f.write(item[0] + "\t" + item[1] + '\n')
        print '\n\n**************\nARRAY FILE WRITTEN\nPROCEDE TOM N -->\n**************\n'
    except Exception, e:
        print 'Failure writing .arr file', e


def extract_log_hyperbolic_data(line):
    line = line[18:]
    comma = line.index(',')
    file_name = line[:comma]
    line_chunks = line.split(' ')
    et = line_chunks[1]
    et = et[5:]
    et = et.split('-')
    start_time = et[0]
    print 'Extracting from log: filename:', file_name, ', Time:', start_time
    return file_name, start_time


def append_to_complete_log(content):
    fh = open('./dir/log_complete.txt', 'a')
    fh.write(content + '\n')
    fh.close()


def clear_ish_log(p):
    f = open(p, 'w')
    f.write('')
    f.close()


def parse_log_file(event_str):

    logfile_path = event_str.split("'")
    logfile_path = logfile_path[1]
    print 'Audio filename from ish_log.txt', logfile_path

    try:
        with open(logfile_path, 'r') as content_file:
            content = content_file.read()
    except Exception, e:
        print 'Exception opening logfile ', e

    if not content or content == '':
        print 'File empty'
        return
    elif content.startswith('Hyperbolic:'):
        print 'Found Hyperbolic: data', content
        append_to_complete_log(content)
        filename, elapsed_time = extract_log_hyperbolic_data(content)
        clear_ish_log(logfile_path)
        return filename, elapsed_time
    elif content.startswith('hyperbolicLocPosition:'):
        print 'Found hyperbolicLocPosition: data', content
        append_to_complete_log(content)
        clear_ish_log(logfile_path)
        return
    else:
        print 'Found something else in log file appending anyways ...', content
        append_to_complete_log(content)
        clear_ish_log(logfile_path)
        return
    #     f = open(path[1], 'r')
    #     file_line = f.readline()
    #     print 'First line of log file after opening: ', file_line
    #     print 'First line of log file after opening: ', file_line
    #     if not file_line or file_line == '':
    #         print 'First line is empty'
    #         return
    #     elif file_line.startswith('Hyperbolic:'):
    #         print 'Found Hyperbolic: data', file_line
    #         filename, elapsed_time = extract_log_hyperbolic_data(file_line)
    #         fh = open('./dir/log_complete.txt', 'a')
    #         fh.write(file_line)
    #         fh.close()
    #     elif file_line.startswith('hyperbolicLocPosition:'):
    #         print 'Found hyperbolicLocPosition: data'
    #         fh = open('./dir/log_complete.txt', 'a')
    #         fh.write(file_line)
    #         for line in f:
    #             fh = open('./dir/log_complete.txt', 'a')
    #             fh.write(line + '\n')
    #         fh.close()
    #
    #     f.close()
    #
    #     f = open(path[1], 'w')
    #     f.write('')
    #     f.close()
    #     return filename, elapsed_time
    # except Exception, e:
    #     print 'Exception Thrown', e
    #     return


def get_gps_file_name(wave_file_name, recorder_dir):
    gps_file_name = wave_file_name.split('.')
    gps_file_name = gps_file_name[0].split('-')

    recorder_dir_num = recorder_dir.split('_')
    recorder_dir_num = recorder_dir_num[1]

    name = 'D' + recorder_dir_num
    for part in gps_file_name[1:]:
        name += '-' + part

    name += '.csv'
    print 'GPS File name:', name
    return name


def get_mins_and_secs(elapsed_time):
    print 'Elapsed Time', elapsed_time
    elapsed_time_parts = elapsed_time.split('.')
    mins = int(elapsed_time_parts[0]) / 60
    secs = int(elapsed_time_parts[0]) % 60
    ms = elapsed_time_parts[1]
    return str(mins) + ':' + str(secs) + '.' + str(ms)


def build_arr_file(working_dir, elapsed_time, wav_file_name, recorder_dirs, wav_file_len_in_mins):
    arr_data = []
    for dir in recorder_dirs:

        gps_file = get_gps_file_name(wave_file_name=wav_file_name, recorder_dir=dir)
        gps_file_path = working_dir + '\\' + dir + '\\' + gps_file
        current_file_time = get_time_from_filename(gps_file)
        current_lat, current_lon = extract_data_from_gps_csv(gps_file_path)

        next_file_name = get_next_file_start_time(wav_file_name, wav_file_len_in_mins)
        gps_file = get_gps_file_name(wave_file_name=next_file_name, recorder_dir=dir)
        gps_file_path = working_dir + '\\' + dir + '\\' + gps_file
        next_file_time = get_time_from_filename(gps_file)
        next_lat, next_lon = extract_data_from_gps_csv(gps_file_path)

        et = get_mins_and_secs(elapsed_time)
        utm_coords = get_data_from_excel_script(current_file_time, next_file_time, et, current_lat, current_lon, next_lat, next_lon)
        print 'UTM COORDS:', utm_coords
        a = utm_coords.split('\t')
        arr_data.append([a[0], a[1]])
    print
    # p = 'C:\Users\BIOWAVES\PycharmProjects\\audioMerger\\test\\tmp\myfile.arr'
    write_to_array_file(listdata=arr_data)


def get_time_from_filename(filename):
    file_parts = filename.split('-')
    t = file_parts[2]
    return t[:2] + ':' + t[2:4] + ':' + t[4:6]


def get_current_file_start_time(file_name):
    name = file_name.split('_')
    return name[0] + '.wav'


def get_next_file_start_time(file_name, delta):
    datetime_pieces = file_name.split('-')

    _date = datetime_pieces[1]
    year = _date[:2]
    month = _date[2:4]
    day_of_month = _date[4:]

    _time = datetime_pieces[2]
    hour = _time[:2]
    minutes = _time[2:4]
    seconds = _time[4:6]

    datetime_object = datetime(year=int(year), month=int(month), day=int(day_of_month), hour=int(hour),
                               minute=int(minutes), second=int(seconds))
    print 'Current File Time:', datetime_object

    now_plus_delta = datetime_object + timedelta(minutes=int(delta))
    print 'Next File Time:', now_plus_delta

    #TODO Need to convert date object back to a filename string
    new_file_name = convert_dateobject_to_file_name(file_name, now_plus_delta)
    return new_file_name


def ensure_double_digits(num):
    number = str(num)
    if len(number) == 1:
        return "0" + number
    elif len(number) == 2:
        return number
    else:
        return number[2:]


def convert_dateobject_to_file_name(old_filename, dateobject):
    file_name_parts = old_filename.split('-')
    file_extension = old_filename.split('.')
    year = ensure_double_digits(dateobject.year)
    month = ensure_double_digits(dateobject.month)
    day = ensure_double_digits(dateobject.day)
    hour = ensure_double_digits(dateobject.hour)
    min = ensure_double_digits(dateobject.minute)
    sec = ensure_double_digits(dateobject.second)
    new_file_name = file_name_parts[0] + "-" + year + month + day + "-" + hour + min + sec + "." + file_extension[1]
    return new_file_name

def extract_data_from_gps_csv(file_path):
    print 'Reading data from GPS file:', file_path
    try:
        with open(file_path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            data = [[] for x in xrange(4)]
            for row in spamreader:
                # print row[0], row[1], row[2], row[3], row[4], row[5]
                # print(', ').join(row)
                data[0].append(row[0])
                data[1].append(row[1])
                data[2].append(row[2])
                data[3].append(row[3])

        print 'Succesfully extracted', data[2][1], data[3][1]
        return data[2][1], data[3][1]
    except Exception, e:
        print 'Error extracting GPS data', e


def get_data_from_excel_script(fst, nfst, et, clat, clon, nlat, nlon):

    print os.path.realpath(__file__), sys.argv[0], os.path.dirname(sys.argv[0])
    project_root_dir = os.path.dirname(sys.argv[0])
    xlPath = project_root_dir + '/shared/converter.xlsx'

    # Set up the echo command and direct the output to a pipe
    p1 = subprocess.Popen(['./shared/ConsoleApp1.exe', xlPath, fst, nfst, et, clat, clon, nlat, nlon], stdout=subprocess.PIPE)

    # Run the command
    output = p1.communicate()[0]

    # print 'Output from excel script',  output
    actual_data = output.split('LAT_LON: ')
    print "Actual Data", actual_data
    return actual_data[1]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = sys.argv[1]
    print 'Script running at: ', path
    print 'Agrs passed to script: ', sys.argv[:]

    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path + '\\', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()