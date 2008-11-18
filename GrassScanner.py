#!/usr/bin/env python
# -*- coding:utf-8 -*-

from grass import App, Abs, PrimE

UPPER_CASE = [u'W', u'\uff37']
LOWER_CASE = [u'w', u'\uff57']
CHAR_V = [u'v', u'\uff56']

class GrassScanner:
    
    code = []
    chlist = []

    def scan(self, str):
        self.chlist = list(str)

        while(1):
            try:
                ch = self.chlist[0]
                if(ch in LOWER_CASE):
                    self.code.append(self.get_abs())
                elif(ch in UPPER_CASE):
                    self.code.append(self.get_apps())
                else:
                    self.chlist.pop(0)
            except IndexError:
                break;

        self.code.append(PrimE())
        return self.code

    def get_abs(self):
        argc = self.count_char(LOWER_CASE, UPPER_CASE + CHAR_V)
        apps = self.get_apps()
        return Abs(argc, apps)

    def get_apps(self):
        ret = []
        while(1):
            func_pos = self.count_char(UPPER_CASE, LOWER_CASE + CHAR_V)
            arg_pos = self.count_char(LOWER_CASE, UPPER_CASE + CHAR_V)
        
            ret.append(App(func_pos, arg_pos))

            if 0 == len(self.chlist): break
            if self.chlist[0] in CHAR_V:
                self.chlist.pop(0)
                break

        ret.append(PrimE())
        return ret
                
    def count_char(self, targets, terminals):
        cnt = 0
        index = 0

        for ch in self.chlist:
            if ch in targets:
                cnt += 1
            elif ch in terminals:
                break

            index += 1
        
        self.chlist = self.chlist[index:]
        return cnt
