# -*- coding: utf-8 -*-
# @Author: UnsignedByte
# @Date:   03:13:05, 14-Aug-2020
# @Last Modified by:   UnsignedByte
# @Last Modified time: 14:17:36, 14-Aug-2020


import sqlite3

connection = sqlite3.connect('test.db');
c = connection.cursor();\

c.execute('''CREATE TABLE test
             (pid integer)''')