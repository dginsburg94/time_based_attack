time_based_attack.py
------
------

A simple script to test a timing based authentication flaw in a dummy command line application. The script uses zscores, or the number of standard of deviations a data point is from the mean of a data set, to determine the best guess for a password.

```
$ python3 time_based_attack.py -h                                                                                                                                                          

usage: time_based_attack.py [-h] filepath

Perform a time based brute force attack against a command line program expecting a password as a single argument.

positional arguments:
  filepath    An absolute filepath to the target command line program

optional arguments:
  -h, --help  show this help message and exit
```
