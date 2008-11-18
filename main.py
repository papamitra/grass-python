#!/usr/bin/env python
# -*- coding:utf-8 -*-

from GrassScanner import GrassScanner
from grass import GrassInterp

str = 'wWWwwww' # 'w'を出力
#str = 'wWWwwwwWWww' # 無限に草植え
#str = 'wwWWwvwwwwWWWwwWwwWWWWWWwwwwWwwvwWWwwwWwwwwWwwwwwwWwwwwwwwww' # 英語版サイトより。1+1の答えを'w'の数であらわすらしい。

#str=u'ＹコンビネータｗｗＷＷｗｗＷｗｗｖちょｗｗＷＷＷｗＷＷＷｗｖおまｗＷＷｗＷｗｖ'

code = GrassScanner().scan(str)

print [x.__str__() for x in code]

GrassInterp(code).run()
