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

# Here is a list of arguments to pass to the script
# 1. Location of the directory to watch containing the Ishmael log.txt file
# 2. Location of .arr file
# 3. Duration of audio files
# 4. Location of the FOLDER containing the FOLDERS with the GPS files
# 5. Add as many folder names as you like that contain GPS file -- Ex: Recorder_1 Recorder_2 ... Recorder_N

class Event(LoggingEventHandler):
    def dispatch(self, event):

        args = sys.argv[:]
        print 'ARGS ... What do we got?', args
        print("Event caught", event)
        event_str = str(event)
        if event_str.endswith("ish_log.txt'>"):
        # if event_str == "<FileModifiedEvent: src_path=u'.\\\\dir\\\\log.txt'>)":
            print('Log file has been modified')
            try:
                fn, et = parse_log_file(event_str)
                # working_dir = 'C:\Users\BIOWAVES\PycharmProjects\\audioMerger\\test'
                working_dir = os.path.join(sys.argv[4])
                recorder_dirs = ['Recorder_1', 'Recorder_2', 'Recorder_3', 'Recorder_5']
                recorder_dirs2 = sys.argv[5:]
                print "Recorder Dirs from ARGS", recorder_dirs2
                duration = int(sys.argv[3])

                if fn and et:
                    build_arr_file(working_dir, et, fn, recorder_dirs, 5)
                else:
                    print 'Error Parsing Ishmial Log File'
            except:
                print 'File Watch Error'
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
    print 'Extracing filename: ', file_name, 'Time: ', et
    return  file_name, et


def parse_log_file(str):
    try:
        path = str.split("'")
        print 'parse_log_file', path
        f = open(path[1], 'r')
        file_line = f.readline()

        if not file_line:
            print('File is empty')
            return
        elif file_line == '':
            print('File is empty')
            return
        elif file_line.startswith('Hyperbolic:'):
            print 'Found Hyperbolic: data', file_line
            filename, elapsed_time = extract_log_hyperbolic_data(file_line)
            fh = open('./dir/log_complete.txt', 'a')
            fh.write(file_line + '\n')
            fh.close()
        elif file_line.startswith('hyperbolicLocPosition:'):
            print 'Found hyperbolicLocPosition: data'
            fh = open('./dir/log_complete.txt', 'a')
            fh.write(file_line)
            for line in f:
                fh = open('./dir/log_complete.txt', 'a')
                fh.write(line + '\n')
            fh.close()

        f.close()

        f = open(path[1], 'w')
        f.write('')
        f.close()
        return filename, elapsed_time
    except Exception, e:
        print 'Exception Thrown', e
        return

def get_gps_file_name(wave_file_name, recorder_dir):
    print wave_file_name
    gps_file_name = wave_file_name.split('.')
    gps_file_name = gps_file_name[0].split('-')

    recorder_dir_num = recorder_dir.split('_')
    recorder_dir_num = recorder_dir_num[1]

    name = 'D' + recorder_dir_num
    for part in gps_file_name[1:]:
        name += '-' + part

    name += '.csv'
    print name
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
    print(datetime_object)

    now_plus_delta = datetime_object + timedelta(minutes=int(delta))
    print(now_plus_delta)

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

    print data
    print data[2][1], data[3][1]
    return data[2][1], data[3][1]


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
    print 'MAIN PATH', path
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