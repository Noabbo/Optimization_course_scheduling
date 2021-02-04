Names and ID : Allen Bronshtein 206228751 , Noa Abbo 208523514

windows user --------> double click Scheduler.bat
linux user ------------> double click Scheduler.sh

Input System

Format for entering year number : Enter a positive integer, ex : 1 2 3 ... 

Format for entering a course number : Enter a positive integer, ex: 1 11 123 14242 ...
==========================NOTE============================ 
If course number is valid but doesn't exist in database , system will ignore the course number
AFTER EACH ENTRY PRESS ENTER
==========================================================

Format for entering unavailabe day and time : Enter day, then space , then start hour, then "-" then end hour, ex: sunday 08-14 monday 08-21 ...
==========================NOTE============================ 
AFTER EACH ENTRY PRESS ENTER
==========================================================

To run statistcs mode do as following :
Open cmd in cwd (same working directory as readme)
type the following :
1. cd Scheduler
2. python main.py -t arg1 arg2 arg3 arg4 arg5

Press enter and wait , the results will be in csv file named "Statistics Results" in same working directory as readme

arg1 - non-negative integer indecating how many runs we want to apply on each parameters test ex.: 10
arg2 - list of number of creations we want to test ex.: [10,20,30]
arg3 - list of number of generations we want to test ex.: [10,20,30]
arg4 - list of number of initial population we want to test ex.: [10,20,30]
arg5 - list of number of mutation probability we want to test ex.: [10,20,30]
