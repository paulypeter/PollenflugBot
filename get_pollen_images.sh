#!/bin/bash

for i in 1 2
do
	for j in {0..7}
	do
		wget "https://www.dwd.de/DWD/warnungen/medizin/pollen/pollen_${i}_${j}.png" -O "pollen_${i}_${j}.png"
	done
done
