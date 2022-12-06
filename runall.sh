#!/bin/bash

mkdir mat
for METHOD in "rand" "deg" "SO" "BFS" "SB" "birand" "bideg" "biSO" "fastpi" "IBSO"; do
    mkdir mat/${METHOD}
done

for DATA in "filmtrust" "IMDB" "Marvel" "ml-1m" "NIPS" "theMovies"; do
    for METHOD in "rand" "deg" "SO" "BFS" "SB" "birand" "bideg" "biSO" "fastpi" "IBSO"; do
        python3 main.py --data ${DATA} --method ${METHOD} --size 128 --save mat/${METHOD}/${DATA}_128.pkl
    done
done