#!\Users\jaredfields\Anaconda3\envs\dev\python.exe

import boto3
from json import loads
from io import BytesIO, StringIO
import zipfile
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from copy import copy  # Hack to work around AWS Boto3 closing file object after upload...

from AccessKeys import dictAccessKeys
from Queries import _listActiveQueries
from BannerConnect import *
from Config import _SCHOOL_NAME, _DESTINATION, _ZIP_FILE_NAME, _WRITE_CSV_TO_DISK, _WRITE_ZIP_TO_DISK, _UPLOAD_FILES_TO_AWS

log = logging.getLogger("B&N Uploader")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh  = RotatingFileHandler("log.txt", maxBytes=5*1024**2)
ch  = logging.StreamHandler()
ch.setFormatter(formatter)
fh.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)

log.info("Script started")

errors = 0

# ~
# GET DATA
# ~

log.info("Getting data...")

_FilesAndData = list()

try:
  for name, query, headings in _listActiveQueries:
    _ShortName, _ = name.split(".")
    RS = Bcur.execute(query)
    fh = StringIO()
    if RS:
      log.info("'{_ShortName}' data retrieved. Generating CSV.".format(**locals()))
      strHeadings = ",".join([repr(i).replace("'", '"') for i in headings])
      fh.write(strHeadings+"\n")
      for row in RS:
        row = ",".join(tuple(['"'+str(val).replace('"', "")+'"' if val is not None else '""' for val in row]))
        fh.write(row+"\n")
      
      if _WRITE_CSV_TO_DISK:
        log.info("Writing {name} to disk.".format(**locals()))
        fh.seek(0)
        with open(name, 'w') as csvFile:
          csvFile.write(fh.read())
      _FilesAndData.append([name, fh.getvalue()])
    else:
      errors += 1
      log.critical("No data retrieved for '{_ShortName}'".format(**locals()))
except Exception as e:
  errors += 1
  log.critical("Exception on getting data: "+str(e))
  

# ~
# GENERATE ZIP
# ~

if not errors:
  log.info("Generating zip file...")

  try:
    _ZipFileObj = BytesIO()
    with zipfile.ZipFile(_ZipFileObj, "a", zipfile.ZIP_DEFLATED, False) as _ZipFileHandle:

      for _file_name, _data in _FilesAndData:
        _ZipFileHandle.writestr(_file_name, _data)

    if _WRITE_ZIP_TO_DISK:
      log.info("Writing {_ZIP_FILE_NAME} to disk.".format(**locals()))
      with open(_ZIP_FILE_NAME, "wb") as _ZipFile:
        _ZipFileObj.seek(0)
        _ZipFile.write(_ZipFileObj.getvalue())
  except Exception as e:
    errors += 1
    log.critical("Exception on generating ZIP file: "+str(e))

# ~
# UPLOAD ZIP
# ~

if _UPLOAD_FILES_TO_AWS and not errors:
  log.info("Uploading...")

  try:
    for bookStore in dictAccessKeys:
      _AccessKeyId     = dictAccessKeys[bookStore]["AccessKeyId"]
      _SecretAccessKey = dictAccessKeys[bookStore]["SecretAccessKey"]
      _Bucket          = dictAccessKeys[bookStore]["Bucket"]
      _Prefix          = dictAccessKeys[bookStore]["HomeDirectory"]+_DESTINATION
      _ZipFilePath     = _Prefix+_ZIP_FILE_NAME

      
      s3 = boto3.resource(
        "s3",
        aws_access_key_id=_AccessKeyId,
        aws_secret_access_key=_SecretAccessKey
      )

      bucket = s3.Bucket(_Bucket)

      # Hack to work around AWS Boto3 closing file object after upload...
      with copy(_ZipFileObj) as data:
        data.seek(0)
        bucket.upload_fileobj(data, _ZipFilePath)

      _FileList = [obj.key for obj in bucket.objects.filter(Prefix=_Prefix)]

      if any(_ZIP_FILE_NAME in key for key in _FileList):
        log.info("SUCCESS - Uploaded /{_ZipFilePath}".format(**locals()))
        with BytesIO() as data:
          bucket.download_fileobj(_ZipFilePath, data)
          if _ZipFileObj.getvalue() == data.getvalue():
            log.info("Upload verified. Data uploaded to bucket matches local copy.")
          else:
            errors += 1
            log.critical("Upload data failed verification!")

      else:
        errors += 1
        log.critical("FAILURE - Failed uploading /{_ZipFilePath}".format(**locals()))
  except Exception as e:
    errors += 1
    log.critical("Exception on upload: "+str(e))

if errors:
  log.critical("Errors encountered. Quitting.")

log.info("Script ended")