import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import csv
from datetime import datetime
from datetime import timedelta
import subprocess
import os
import time
import utm
import requests
import json
import urllib2

# Here is a list of arguments to pass to the script
# 1. Location of the directory to watch containing the Ishmael log.txt file
# 2. Location of .arr file
# 3. Duration of audio files
# 4. Location of the FOLDER containing the FOLDERS with the GPS files
# 5. Add as many folder names as you like that contain GPS file -- Ex: Recorder_1 Recorder_2 ... Recorder_N

last_hyperloc_pos = 0,0

class Event(LoggingEventHandler):

    def dispatch(self, event):
        global last_hyperloc_pos
        print "Watchdog file event: ", event, 'last_hyperloc_pos', last_hyperloc_pos
        event_str = str(event)
        fn = ''
        et = ''
        if event_str.startswith('<FileModifiedEvent:') and event_str.endswith("ish_log.txt'>"):
            try:
                data = parse_log_file(event_str)
                if data is not None:
                    fn = data[0]
                    et = data[1]
                    working_dir = os.path.join(sys.argv[4])
                    recorder_dirs = sys.argv[5:]
                    duration = int(sys.argv[3])

                    print 'Calling build array with params', working_dir, et, fn, recorder_dirs, duration
                    build_arr_file(working_dir, et, fn, recorder_dirs, duration)
                else:
                    print 'Doing nothing'
            except Exception, e:
                print '', e
                return

            # working_dir = os.path.join(sys.argv[4])
            # recorder_dirs = sys.argv[5:]
            # duration = int(sys.argv[3])
            # if fn is not None and et is not None:
            #     print 'Calling buld array with params', working_dir, et, fn, recorder_dirs, duration
            #     build_arr_file(working_dir, et, fn, recorder_dirs, duration)
            # else:
            #     print ''

    def on_modified(self, event):
        print("Doh", event)


def http_post_request(data):
    print 'Sending POST request: to 192.168.1.84:4200 with data:', data
    headers = {'content-type': 'application/json'}
    r = requests.post("http://localhost:4200/update", data, headers)
    print(r.status_code, r.reason)
    return r.status_code1


def build_post_request(whale_num, data):
    params = {"id": whale_num, "lat": data[0], "lng": data[1]}
    print 'BUILT PARAMS', params
    return params


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
    print 'Elapsed Time Piece: ', et
    if et.startswith('sel=('):
        print 'Parsing with sel=('
        start_time = et[5:]
    else:
        print 'Parsing with sel='
        et = et[4:]
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

    try:
        with open(logfile_path, 'r') as content_file:
            content = content_file.read()
    except Exception, e:
        print 'Exception opening logfile ', e
        return

    if not content or content == '':
        print 'Ish Log File empty'
        return
    elif content.startswith('Hyperbolic:'):
        print 'Found Hyperbolic: data', content
        append_to_complete_log(content)
        filename, elapsed_time = extract_log_hyperbolic_data(content)
        clear_ish_log(logfile_path)
        return filename, elapsed_time
    elif content.startswith('hyperbolicLocPosition'):
        print 'Found hyperbolicLocPosition: data', content
        append_to_complete_log(content)
        clear_ish_log(logfile_path)
        return
    elif content.startswith('plotLoc'):
        whale_num = content[7:8]
        global last_hyperloc_pos
        print 'Using this value for last_hyperloc_pos:', last_hyperloc_pos

        # payload = {'lat': 36.78848171840966, 'lng': -121.82906786028143, 'id': '1'}
        payload = {'lat': last_hyperloc_pos[0], 'lng': last_hyperloc_pos[1], 'id': whale_num}
        print "Payload before request", payload

        req = urllib2.Request('http://localhost:4200/update')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(payload))

        append_to_complete_log(content)
        clear_ish_log(logfile_path)
        return
    elif content.startswith('plotRecorders'):
        parts = content.split(' ')
        wav_file = parts[1]
        wav_file = wav_file[6:]

        recorder_dirs = sys.argv[5:]
        for dir in recorder_dirs:
            csv = get_gps_file_name(wav_file, dir)
            working_dir = os.path.join(sys.argv[4])
            gps_file_path = working_dir + '\\' + dir + '\\' + csv
            lat, lng = extract_data_from_gps_csv(gps_file_path)
            payload = {'lat': lat, 'lng': lng}
            print "Payload before request", payload

            req = urllib2.Request('http://localhost:4200/recorder')
            req.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(req, json.dumps(payload))

        append_to_complete_log(content)
        clear_ish_log(logfile_path)

    elif content.startswith('Location'):
        print 'Location CONTENT', content
        if "position=(" in content:
            try:
                parts = content.split('position=(')
                pos = parts[len(parts) - 1:]
                print 'HOPEFULLY FOUND POS STR -->', pos
                utm_parts = pos[0].split(',')
                part_a = utm_parts[0].strip()
                part_b = utm_parts[1].split(')')
                part_b = part_b[0]

                a = float(part_a)
                b = float(part_b)
                print 'Parts = ', part_a, part_b, a, b
                # l = utm.to_latlon(a, b, 32, 'U')
                # l = utm_to_lat_lon(10, a, b)
                l = utm.to_latlon(a, b, 10, 'S')
                global last_hyperloc_pos
                last_hyperloc_pos = l
                print 'And back to LAT LON???', l

            except Exception, e:
                print 'Most likely some bad data in Ish Localization', e
            append_to_complete_log(content)
            clear_ish_log(logfile_path)
            return
    else:
        print 'Found something else in log file appending anyways ...', content
        # parts = content.split('position=(')
        # if len(parts) > 1:
        #     position_data = parts[0]
        #     print 'FOUND POSITION DATA', position_data[1]
        append_to_complete_log(content)
        clear_ish_log(logfile_path)
        return

    return


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
    print 'Elapsed Time', elapsed_time, 'Converted time', str(mins) + ':' + str(secs) + '.' + str(ms)
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