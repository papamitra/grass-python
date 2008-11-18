#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

def debug_str(x):
    if isinstance(x, list):
        return '[' + ','.join([debug_str(item) for item in x]) + ']'
    elif isinstance(x, tuple):            
        return '(' + ','.join([debug_str(item) for item in x]) + ')\n'
    else:
        return x.__str__()

class App:
    def __init__(self, func_pos, arg_pos):
        self._func_pos = func_pos
        self._arg_pos = arg_pos

    def apply(self, c, e, d):
        
        func = e[self._func_pos-1]

        if isinstance(func, tuple):
            cm = func[0]
            em = func[1]
            
            arg = e[self._arg_pos-1]

            d.insert(0, (c[:], e[:]))
            e[:] = [arg] + em
            c[:] = cm

        else: # primitive
            """ this implement is out of document!!! """
            ret = func.call(e[self._arg_pos-1])
            e.insert(0, ret)
    
    def __str__(self):
        return "App(%d,%d)" % (self._func_pos, self._arg_pos)


class Abs:
    def __init__(self, argc, body):
        self._argc = argc
        self._body = body

    def apply(self, c, e, d):
        if 1 == self._argc:
            e.insert(0, (self._body[:], e[:]))
        else:
            e.insert(0, ([Abs(self._argc-1, self._body[:]), PrimE()], e[:]))

    def __str__(self):
        return "Abs(%d," % (self._argc) + [x.__str__() for x in self._body].__str__() + ")"

class PrimE:
    def apply(self, c, e, d):
        dump = d.pop(0)

        if isinstance(dump, PrimE):
            sys.exit("end")

        cd = dump[0]
        ed = dump[1]

        e[1:] = ed
        
        c[:] = cd

    def call(self, arg):
        """ this implement is out of document!!! """
        return arg

    def __str__(self):
        return 'PrimE'

class PrimOut:
    def call(self, arg):
#        sys.stdout.write(arg.char())
        print(arg.char())
#        print "%X" % ord(arg.char())
        return arg

    def __str__(self):
        return 'Out'

class PrimIn:
    def call(self, arg):
        s = raw_input('>')
        if s == '' : return arg
        else: return PrimChar(unichr(ord(s[0])))

    def __str__(self):
        return 'In'

class PrimSucc:
    def call(self, arg):
        next_char = unichr((ord(arg.char()) + 1) % 256)
        return PrimChar(next_char)

    def __str__(self):
        return 'Succ'

class PrimChar:
    def __init__(self, char):
        self._char = char

    def char(self):
        return self._char
    
    def call(self, arg):
        if self._char == arg.char():
            return ChurchBoolean(True)
        else:
            return ChurchBoolean(False)

    def __str__(self):
        return "Char('%c')" % self._char

class ChurchBoolean:
    """ this implement is out of document!!! """

    _x = None

    def __init__(self, bool):
        self._bool = bool

    def call(self, arg):
        if _x:
            if _bool: return _x
            else: return arg #  return y
        else:
            _x = arg
            return self

    def __str__(self):
        if self._bool: bool_str = "True"
        else: bool_str = "False"

        if _x:
            return bool_str + "(%s, )" % _x.__str__()
        else:
            return bool_str + "( , )"

class GrassInterp:
    def __init__(self, code):
        self._C = code
        self._E = [PrimOut(), PrimSucc(), PrimChar(u'w'), PrimIn(), PrimE()]
        self._D = [([App(1,1), PrimE()], [PrimE()]), ([PrimE()], [PrimE()]), PrimE()]

    def run(self):
        while(1):
            print "C=" + debug_str(self._C)
            print "E=" + debug_str(self._E)
            print ""
            code = self._C.pop(0)
            code.apply(self._C, self._E, self._D)

if __name__ == "__main__":
#    C =  [Abs(1, [App(2,4), PrimE()]), PrimE()]
#    C =  [Abs(1, [App(2,4), App(2,2), PrimE()]), PrimE()]
    C = [Abs(1, [App(1,1), PrimE()]), PrimE()]
    GrassInterp(C).run()
