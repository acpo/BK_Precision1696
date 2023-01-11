# BK_Precision1696
Python controller for BK Precision 1696 for ETA experiments  
The goal is to control voltage, current, and time for a 5-step program.  BK Precision offers some help at https://github.com/BKPrecisionCorp/1696B_Series   The series is similar but not identical; although the library of functions should be useful.  Be cautious, there are some typos in the BK library and the move to Python 3 seems to have caused syntax changes.
## Completed:
- get list of all COM ports with PySerial, let user pick the port on drop-down list
- read and write programmed values as a text file
- error checking of numerical entries
- ability to run the program 
## To do:  
- report COM port baud, etc 
- make useful notifications for COM exceptions
