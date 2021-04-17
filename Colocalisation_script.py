#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:44:12 2020

@author: remisova
"""
import math
main_file=open("AL953_210331_RAD51(568)_CREST(488)_gH2AX(647)_20X_MA_001_Main.txt")
fociA_file=open("AL953_210331_RAD51(568)_CREST(488)_gH2AX(647)_20X_MA_001_RAD51 foci.txt")
fociB_file=open("AL953_210331_RAD51(568)_CREST(488)_gH2AX(647)_20X_MA_001_CREST  foci.txt")
fociA=fociA_file.readlines()
fociB=fociB_file.readlines()
main=main_file.readlines()
main_file.close()
fociA_file.close()
fociB_file.close()

head_main=main[0]
head_main=head_main.strip("")
head_main=head_main.split("       ")
head_main=head_main[0]
head_main=head_main.split("\t")

head_fociA=fociA[0]
head_fociA=head_fociA.strip("")
head_fociA=head_fociA.split("       ")
head_fociA=head_fociA[0]
head_fociA=head_fociA.split("\t")

head_fociB=fociB[0]
head_fociB=head_fociB.strip("")
head_fociB=head_fociB.split("       ")
head_fociB=head_fociB[0]
head_fociB=head_fociB.split("\t")

#indexing
centerxfociB=head_fociB.index("Center X ")
centeryfociB=head_fociB.index("Center Y ")
centerxfociA=head_fociA.index("Center X ")
centeryfociA=head_fociA.index("Center Y ")
index_fociB_ID=head_fociB.index("Parent Object ID (MO)")
index_fociA_ID=head_fociA.index("Parent Object ID (MO)")
index_fociA_area=head_fociA.index("Area ")
index_fociB_area=head_fociB.index("Area ")

number_of_cells=len(main)
pi=3.14159265359
fociB_dic_positions={}
fociA_dic_positions={}


for i, line in enumerate(fociA):
    if i>0:
        line=line.strip("")
        line=line.split()
        key=int(line[index_fociA_ID])
        x=float(line[centerxfociA])
        y=float(line[centeryfociA])
        area=float(line[index_fociA_area])
        value=[x,y,area]
        if key not in fociA_dic_positions:
            fociA_dic_positions[key]=[]
        if key in fociA_dic_positions:
            fociA_dic_positions[key].append(value)
            
for i, line in enumerate(fociB):
    if i>0:
        line=line.strip("")
        line=line.split()
        key=int(line[index_fociB_ID])
        x=float(line[centerxfociB])
        y=float(line[centeryfociB])
        area=float(line[index_fociB_area])
        value=[x,y,area]
        if key not in fociB_dic_positions:
            fociB_dic_positions[key]=[]
        if key in fociB_dic_positions:
            fociB_dic_positions[key].append(value)

colocalisation_list=[]
for i in range(number_of_cells):
    number_of_colocalisations=0
    if i in fociA_dic_positions and i in fociB_dic_positions:
        for foci in fociA_dic_positions[i]:
            x_fociA=foci[0]
            y_fociA=foci[1]
            area_fociA=foci[2]
            r_fociA=math.sqrt(area_fociA/pi)
            for droplet in fociB_dic_positions[i]:
                x_fociB=droplet[0]
                y_fociB=droplet[1]
                area_fociB=droplet[2]
                r_fociB=math.sqrt(area_fociB/pi)
                distance = math.sqrt((x_fociA-x_fociB)**2+(y_fociA-y_fociB)**2)
                if distance<r_fociA or distance<r_fociB:
                        number_of_colocalisations=number_of_colocalisations+1
    colocalisation_list.append([i,number_of_colocalisations])
        
#writting in the data
n=0
lines_together=""
for element in colocalisation_list:
    if n==0:
       line="Number of colocalisations"+"\n"
    else:
        line="{:d}".format(colocalisation_list[n-1][1])+"\n"
    n=n+1
    lines_together=lines_together+line
    
CoCo = open("CoCo3.0.txt","w")
CoCo.write(lines_together)
CoCo.close()
