# Import the module
import subprocess

xlPath = "D:/For Sage/converter.xlsx"
# fileStartTime = args[1];
#             string nextFileStartTime = args[2];
#             string elapsedTime = args[3];
#             string currentLat  = args[4];
#             string currentLon  = args[5];
#             string nextLat     = args[6];
#             string nextLon     = args[7];

fst = '17:30:00'
nfst = '17:35:00'
et = '2:30.0'
clat = '39'
clon = '40'
nlat = '40'
nlon = '41'
# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['D:/For Sage/ConsoleApp1.exe', xlPath, fst, nfst, et, clat, clon, nlat, nlon], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]

print output

