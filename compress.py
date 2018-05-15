import numpy as np
from math import *
import time
import warnings

#compress function
def compress(original_series, tolerance):
    '''
    compress original series, each segment in this form: [a, b, t]
    a, b is two parameters of the regression line, t is the location of the
    last point in the whole series 
    return a list of segments
    '''
    compressed_list = []
    segment = []
    index = 0
    #start of a segment
    start = 0
    segment.append(original_series[0])
    for i in original_series[1:]:
        #store the start index of a segment
        if len(segment) is 1:
            start = index
        temp_list = segment
        #append a new point to current segment
        temp_list.append(i)
        #liner regression
        paras = list(np.polyfit(range(len(temp_list)), temp_list, 1))
        if not exceed_tolerance(temp_list, paras, tolerance):
            #not exceed tolerance, keep the new point
            segment = temp_list
        else:
            #exceed tolerance, append the segment to result list and start a
            #new segment
            paras = list(np.polyfit(range(len(segment)), segment, 1))
            l = []
            l.append(paras[0])
            l.append(paras[1])
            l.append(start + len(segment))
            compressed_list.append(l)
            segment = []
            segment.append(i)
        index += 1
    #append the last segment of the list
    paras = list(np.polyfit(range(len(segment)), segment, 1))
    l = []
    l.append(paras[0])
    l.append(paras[1])
    l.append(start + len(segment))
    compressed_list.append(l)
    return compressed_list

#decompress function
def decompress(filepath):
    '''
    decompress, return a decompressed list
    '''
    decompressed_list = []
    f = open(filepath)
    #store the end position of previous segment
    prev_end = 0
    for line in f.readlines():
        line = line.strip().split()
        l = [float(x) for x in line[:2]]
        l.append(int(line[2]))
        end = l[2]
        #get the parameters of the line
        paras = l[:2]
        #recover the values
        for i in range(end - prev_end):
            t = paras[0] * i + paras[1]
            if t < 0:
                t = 0
            t = int(t)
            decompressed_list.append(t)
        prev_end = end
    return decompressed_list

#write compressed list to specified file
def write_to_file(compressed_list, filepath):
    f = open(filepath, 'w')
    for i in compressed_list:
        for item in i:
            f.write(str(round(item)) + ' ')
        f.write('\n')

#to see if the varience exceeds tolerance
def exceed_tolerance(segment, paras, tolerance):
    index = 0
    #check every point to see if the varience exceeds tolerance 
    for i in segment:
        t = paras[1] + paras[0] * index
        if abs(t - i) > i * tolerance:
            return 1
        else:
            index += 1
    return 0
