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


def upload(baseurl):
  """
  Prompts the user for a local filename and user id, 
  and uploads that asset (PDF) to S3 for processing. 

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    print("Enter PDF filename>")
    local_filename = 'reviewtest.pdf'

    if not pathlib.Path(local_filename).is_file():
      print("PDF file '", local_filename, "' does not exist...")
      return

    #
    # build the data packet. First step is read the PDF
    # as raw bytes:
    #
    infile = open(local_filename, "rb")
    bytes = infile.read()
    infile.close()

    #
    # now encode the pdf as base64. Note b64encode returns
    # a bytes object, not a string. So then we have to convert
    # (decode) the bytes -> string, and then we can serialize
    # the string as JSON for upload to server:
    #
    
    datastr = ""
    data = base64.b64encode(bytes)
    datastr = data.decode('utf-8')

    data = {"file": datastr}

    #
    # call the web service:
    #
    
    res = None
    jobid='fuck'
    # TODO: ???
    url = f"{baseurl}/extract"
    headers = {'Content-Type': 'application/json'}
    res = requests.get(url, json=data, headers=headers)
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
  
upload('https://ecgcragkbd.execute-api.us-east-2.amazonaws.com/prod')