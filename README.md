# ADM22fall_team3
Implementation of IBSO (Iterative Bucket Shingle Ordering) and other compression-friendly vertices reordering baselines.
We provide nine baselines and six real-world datasets.

## Requirements
```
make setup
```
- click==8.0.3
- networkx==2.8.8
- numpy==1.23.4
- scipy==1.6.1
## Demo
```
make
```
Run IBSO algorithm on Filmtrust dataset with block size of 128.

## Usage
```
python main.py --opt1 arg1 --opt2 arg2 ...
```
- Options
  - seed : set a random seed (default 0)
  - data : select the dataset to run the graph reordering algorithm
  - method : choose the algorithm to run
  - size : set the size of each block in adjacency matrix
  - save : path to store the adjacency matrix (leave empty not to store)
  