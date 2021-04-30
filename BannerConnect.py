#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import cx_Oracle
import base64
from json import dumps

try:
  Bcon = cx_Oracle.connect(base64.b64decode(b'{Put your base64 encoded Banner connection string here}').decode())
except:
  Bcon = {"success": False, "message": "Error connecting to database."}

if type(Bcon) is not dict:
  Bcur = Bcon.cursor()
