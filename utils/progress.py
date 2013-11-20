#! /usr/bin/env python 
# -*- coding: utf-8 -*-

'''
@filename :   demo.py
@authors  :   U{peterguo<mailto: peterguo@tencent.com>}
@copyright:   tencent
@date     :   2012-11-15
@version  :   1.0.0.1
'''
import os
import sys
import time
import thread

g_nTotal = 100
g_nProcessed = 0
g_fStartTime = time.time()


def simpleThdreadFun(interval):
    global g_nProcessed
    global g_nTotal
    while g_nTotal > g_nProcessed:
        time.sleep(interval)
        g_nProcessed += 1
    thread.exit_thread()


def test():
    global g_nTotal
    global g_nProcessed
    global g_fStartTime
    g_fStartTime = time.time()

    thread.start_new_thread(simpleThdreadFun, (1,))
    thread.start_new_thread(simpleThdreadFun, (2,))
    thread.start_new_thread(simpleThdreadFun, (3,))
    thread.start_new_thread(simpleThdreadFun, (4,))

    while True:
        time.sleep(0.5)
        fRunTime = time.time() - g_fStartTime
        nLeftNum = g_nTotal - g_nProcessed
        fLeftTime = fRunTime * nLeftNum / (g_nProcessed + 0.1)
        fPrograss = 100.0 * g_nProcessed / g_nTotal

        os.write(1, "\rLeftTime[%.3f]\tLeftNum[%d]\tProgress[%.3f %% (%d/%d) ]" %
                    (fLeftTime, nLeftNum, fPrograss, g_nProcessed, g_nTotal))
        sys.stdout.flush()
        if g_nTotal <= g_nProcessed:
            break
    print "\nTest Done, use %.3f seconds" % time.time() - g_fStartTime


if __name__ == '__main__':
    test()

