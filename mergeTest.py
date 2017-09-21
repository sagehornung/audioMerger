from pydub import AudioSegment
from os import listdir
import os
from os.path import isfile, join
from pydub import AudioSegment
import ntpath

# p2 = "E:/__San Juan Island 2017/_Field Recordings/04JUN17/Buoy_2/D2-170604-224000.wav"
# p3 = "E:/__San Juan Island 2017/_Field Recordings/04JUN17/Buoy_3/D3-170604-224000.wav"
# p4 = "E:/__San Juan Island 2017/_Field Recordings/04JUN17/Buoy_4/D4-170604-224000.wav"
# p5 = "E:/__San Juan Island 2017/_Field Recordings/04JUN17/Buoy_5/D5-170604-224000.wav"
#
# ch2 = AudioSegment.from_wav(p2)
# reduced_ch2 = ch2.set_frame_rate(24000)
# ch3 = AudioSegment.from_wav(p3)
# reduced_ch3 = ch3.set_frame_rate(24000)
# ch4 = AudioSegment.from_wav(p4)
# reduced_ch4 = ch4.set_frame_rate(24000)
# ch5 = AudioSegment.from_wav(p5)
# reduced_ch5 = ch5.set_frame_rate(24000)
#
#
# multi = AudioSegment.from_mono_audiosegments(reduced_ch2, reduced_ch3, reduced_ch4, reduced_ch5)
# # reduced_multi = multi.set_frame_rate(24000)
# file_handle = multi.export("C:/Users/User/PycharmProjects/audioMerger/test/Multichannel_Output/test_merge.wav", format="wav")


# pp1 = "C:/Users/User/PycharmProjects/audioMerger/test/Recorder_1/D1-170813-153500.wav"
# pp2 = "C:/Users/User/PycharmProjects/audioMerger/test/Recorder_2/D2-170813-153500.wav"
# pp3 = "C:/Users/User/PycharmProjects/audioMerger/test/Recorder_3/D3-170813-153500.wav"
# pp5 = "C:/Users/User/PycharmProjects/audioMerger/test/Recorder_5/D5-170813-153500.wav"
#
# ch1a = AudioSegment.from_wav(pp1)
# ch2a = AudioSegment.from_wav(pp2)
# ch3a = AudioSegment.from_wav(pp3)
# ch5a = AudioSegment.from_wav(pp5)
#
# multi = AudioSegment.from_mono_audiosegments(ch1a, ch2a, ch3a, ch5a)
# # reduced_multi = multi.set_frame_rate(24000)
# file_handle = multi.export("C:/Users/User/PycharmProjects/audioMerger/test/Multichannel_Output/test_merge2.wav", format="wav")

def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_wav_files = [f for f in onlyfiles if f.endswith('.wav')]
    return only_wav_files

a = get_files('E:/__San Juan Island 2017/_Field Recordings/04JUN17/Buoy_2')
print a