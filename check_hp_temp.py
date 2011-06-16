#!/usr/bin/env python

import sys,os
from optparse import OptionParser

sensors = []
countOK = 0
countWarning = 0
countError = 0
countUnknown = 0

# clean up the arrray
def cleanArray(lines):
    lines = lines[3:]
    while (lines[-1] == []):
            lines.pop()
    return lines

def parseDegrees(line):
    if (line[2] == "-"):
        line[2] = 0;
        line[3] = 0;
    else:
        line[2] = int(line[2].split('/')[0].strip('C'))
        line[3] = int(line[3].split('/')[0].strip('C'))
    return line

def compareSensor(line):
       global countUnknown,countOK,countError
       sensorNum = line[0]	
       sensorName = line[1]
       current = line[2]
       threshold = line[3]
       if(current == 0):
               print('Sensor %s %s reports no temperature value' % (sensorName,sensorNum)) 
               countUnknown += 1
       elif(current >= threshold):      
               print("Too Hot! Sensor %s %s current temperature is %dC which" \
                     " exceeds threshold %dC" % (sensorName, sensorNum, current, threshold))
               countError += 1
       else:
               print("OK: Sensor %s %s current temperature is %dC which" \
                        " is below threshold %dC" \
                         % (sensorName, sensorNum,current, threshold))
               countOK += 1

def nagiosExitCode():
        if(countError > 0):
               print("%d sensors exceed thresholds. Too Hot!" % countError)
               sys.exit(2)
        else:
                print("%d sensors beneath thresholds. Nice and Cool!" % countOK)
                sys.exit(0)

usage = "usage: %prog [Options]"
parser = OptionParser(usage)
parser.add_option("-i", "--input-file", dest="infile",
                help="input file containing system temperatures")
(options, args) = parser.parse_args()

if (options.infile):
        infile = options.infile
        infile = open(options.infile)
else:
        stdin,stdout,stderr = os.popen3('hpasmcli -s "show temp;"')
        infile = stdout


for line in infile.readlines() :
    sensors.append(line.split())
sensors = cleanArray(sensors)
sensors = map(parseDegrees, sensors)
for sensor in sensors:
        compareSensor(sensor)

nagiosExitCode()


