#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 17:21:42 2024

@author: romas
"""

import os
from time import sleep

n = 1
while True:
    print(n)
    
    if not n%10:
        print('forking')
        
        retval = os.fork()
        child = (retval == 0)

        mypid = os.getpid()

        if child:
           print('I am the child.  PID: %d.' % mypid)
           print('executing ls')
           os.execv('/usr/bin/ls' ,['/usr/bin/ls' , '-l' , '/home'])
       
        else:
           print('I am the parent.  PID: %d.  My child has PID %d.' % 
                 (mypid, retval))

            
            
    sleep(0.5)
    n += 1
    