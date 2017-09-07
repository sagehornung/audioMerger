import csv
import sys
import subprocess
import os

def extract_data_from_gps_csv(file_path):
    with open(file_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data  = [[] for x in xrange(4)]
        for row in spamreader:
            print row[0], row[1], row[2], row[3], row[4], row[5]
            print(', ').join(row)
            data[0].append(row[0])
            data[1].append(row[1])
            data[2].append(row[2])
            data[3].append(row[3])

    print data
    print data[2][1], data[3][1]
    return data[2][1], data[3][1]


#extract_data_from_gps_csv('C:\Users\BIOWAVES\PycharmProjects\\audioMerger\\test\Recorder_3\D3-170813-153500.csv')


def write_to_array_file(arr_path, listdata):
    f = open(arr_path, 'w')
    for item in listdata:
        f.write("%s\t%s\n" % (item[0], item[1]))

p = 'C:\Users\BIOWAVES\PycharmProjects\\audioMerger\\test\\tmp\myfile.arr'
l = [[100, 120], [200, 220]]
# write_to_array_file(p, l)


def get_gps_file_name(wave_file_name, recorder_dir):
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

n = 'M-170813-153000.wav'
r = 'Recorder_3'
# get_gps_file_name(n, r)

import datetime
now = datetime.datetime.now()


def get_data_from_excel_script(fst, nfst, et, clat, clon, nlat, nlon):
    # process = subprocess.Popen(['path/to/.exe', 'arg1', 'arg2'], stdout=subprocess.PIPE)
    # output = process.communicate()[0]
    # return output
    print os.path.realpath(__file__), sys.argv[0], os.path.dirname(sys.argv[0])
    project_root_dir = os.path.dirname(sys.argv[0])
    xlPath = project_root_dir + '/shared/converter.xlsx'
    # fileStartTime = args[1];
    #             string nextFileStartTime = args[2];
    #             string elapsedTime = args[3];
    #             string currentLat  = args[4];
    #             string currentLon  = args[5];
    #             string nextLat     = args[6];
    #             string nextLon     = args[7];

    # fst = '17:30:00'
    # nfst = '17:35:00'
    # et = '2:30.0'
    # clat = '39'
    # clon = '40'
    # nlat = '40'
    # nlon = '41'
    # Set up the echo command and direct the output to a pipe
    p1 = subprocess.Popen(['./shared/ConsoleApp1.exe', xlPath, fst, nfst, et, clat, clon, nlat, nlon], stdout=subprocess.PIPE)

    # Run the command
    output = p1.communicate()[0]

    # print 'Output from excel script',  output
    actual_data = output.split('LAT_LON: ')
    print "Actual Data", actual_data
    return actual_data[1]

def convert_dateobject_to_file_name(old_filename, dateobject):
    print dateobject.hour, dateobject.minute, dateobject.second
    print dateobject.year, dateobject.month, dateobject.day
    print ensure_double_digits(dateobject.year)
    print ensure_double_digits(dateobject.month)
    print ensure_double_digits(dateobject.day)
    print ensure_double_digits(dateobject.second)

def ensure_double_digits(num):
    number = str(num)
    if len(number) == 1:
        return "0" + number
    elif len(number) == 2:
        return number
    else:
        return number[2:]

# convert_dateobject_to_file_name(n, now)

log_line = 'Hyperbolic: input=M-170813-153500.wav, sel=(84.010 s, 68.97 Hz) to (128.475 s, 5655.17 Hz)'

def extract_log_hyperbolic_data(line):
    line = line[18:]
    comma = line.index(',')
    file_name = line[:comma]
    line_chunks = line.split(' ')
    et = line_chunks[1]
    et = et[5:]
    print 'Extracing filename: ', file_name, 'Time: ', et
    return  file_name, et

extract_log_hyperbolic_data(log_line)
