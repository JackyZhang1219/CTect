import requests
import jsons

import uuid
import pathlib
import logging
import sys
import os
import base64
import time
import random 
from configparser import ConfigParser
import pymysql

def upload(baseurl):

  try:
    print("Enter PDF filename>")
    local_filename = 'reviewtest.pdf'

    if not pathlib.Path(local_filename).is_file():
      print("PDF file '", local_filename, "' does not exist...")
      return

    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()
    
    datastr = ""
    data = base64.b64encode(bytes)
    datastr = data.decode('utf-8')

    data = {"file": datastr}

    
    res = None
    url = f"{baseurl}/extract"
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, json=data, headers=headers)
    #
    # let's look at what we got back:
    #
    if res.status_code == 200: #success
      pass
    elif res.status_code == 400: # no such user
      body = res.json()
      print(body)
      return
    else:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      print(res.json())
      if res.status_code == 500:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # success, extract jobid:
    #
    body = res.json()

    jobid = body

    print("PDF uploaded, job id =", jobid)
    return

  except Exception as e:
    logging.error("**ERROR: upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  
# upload('https://4xva6b2e07.execute-api.us-east-2.amazonaws.com/prod')



db_config = {
    'user': 'admin',
    'password': 'pdfstoragedatabase',
    'host': 'pdfstore-database.c5ggmgyguhw5.us-east-2.rds.amazonaws.com',
    'database': 'pdfstore'
}

dbConn = pymysql.connect(**db_config)
dbCursor = dbConn.cursor()

insert_query = """
INSERT INTO jobs (status, classname, extractedtext, averagerating)
VALUES (%s, %s, %s, %s)
"""

values = ('completed', f"cs310", "AAAAAAAAAA IO HATE IT I HfATE IT", None)

dbCursor.execute(insert_query, values)
dbConn.commit()