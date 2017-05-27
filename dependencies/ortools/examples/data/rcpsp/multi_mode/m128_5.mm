************************************************************************
file with basedata            : cm128_.bas
initial value random generator: 719693738
************************************************************************
projects                      :  1
jobs (incl. supersource/sink ):  18
horizon                       :  78
RESOURCES
  - renewable                 :  2   R
  - nonrenewable              :  2   N
  - doubly constrained        :  0   D
************************************************************************
PROJECT INFORMATION:
pronr.  #jobs rel.date duedate tardcost  MPM-Time
    1     16      0       30       12       30
************************************************************************
PRECEDENCE RELATIONS:
jobnr.    #modes  #successors   successors
   1        1          3           2   3   4
   2        1          3           5   6   7
   3        1          1           6
   4        1          3          11  12  13
   5        1          3           9  12  13
   6        1          3           9  10  13
   7        1          1           8
   8        1          2          10  16
   9        1          2          11  14
  10        1          1          17
  11        1          2          15  16
  12        1          2          14  15
  13        1          2          14  15
  14        1          2          16  17
  15        1          1          18
  16        1          1          18
  17        1          1          18
  18        1          0        
************************************************************************
REQUESTS/DURATIONS:
jobnr. mode duration  R 1  R 2  N 1  N 2
------------------------------------------------------------------------
  1      1     0       0    0    0    0
  2      1     7       0    1    9    0
  3      1     2       0    4    7    0
  4      1     4       0    6    9    0
  5      1     5       0    5    0    9
  6      1     2       0    3    3    0
  7      1     5       0    3    0    9
  8      1     8       3    0    4    0
  9      1     6       0    5    0    5
 10      1     9       9    0    0    2
 11      1     7       8    0    4    0
 12      1     4       0    4    7    0
 13      1    10       5    0    0    9
 14      1     3       0    7    7    0
 15      1     3       0    6    0    6
 16      1     2       4    0    4    0
 17      1     1       3    0    0    8
 18      1     0       0    0    0    0
************************************************************************
RESOURCEAVAILABILITIES:
  R 1  R 2  N 1  N 2
   22   11   54   48
************************************************************************