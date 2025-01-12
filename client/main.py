#
# Client-side python app for ctex app, which is calling
# a set of lambda functions in AWS through API Gateway.
# The overall purpose of the app is to process a PDF and
# provide a summary and sentiment analysis of the contents
#
# Authors:
#   Ethan Guo
#   Jacky Zhang
#
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   CS 310
#

import requests
import pathlib
import logging
import sys
import base64
import time

from configparser import ConfigParser


############################################################
#
# classes
#
class User:

  def __init__(self, row):
    self.userid = row[0]
    self.username = row[1]
    self.pwdhash = row[2]


class Job:

  def __init__(self, row):
    self.jobid = row[0]
    self.userid = row[1]
    self.status = row[2]
    self.originaldatafile = row[3]
    self.datafilekey = row[4]
    self.resultsfilekey = row[5]


###################################################################
#
# web_service_get
#
# When calling servers on a network, calls can randomly fail. 
# The better approach is to repeat at least N times (typically 
# N=3), and then give up after N tries.
#
def web_service_get(url):
  """
  Submits a GET request to a web service at most 3 times, since 
  web services can fail to respond e.g. to heavy user or internet 
  traffic. If the web service responds with status code 200, 400 
  or 500, we consider this a valid response and return the response.
  Otherwise we try again, at most 3 times. After 3 attempts the 
  function returns with the last response.
  
  Parameters
  ----------
  url: url for calling the web service
  
  Returns
  -------
  response received from web service
  """

  try:
    retries = 0
    
    while True:
      response = requests.get(url)
        
      if response.status_code in [200, 400, 480, 481, 482, 500]:
        #
        # we consider this a successful call and response
        #
        break;

      #
      # failed, try again?
      #
      retries = retries + 1
      if retries < 3:
        # try at most 3 times
        time.sleep(retries)
        continue
          
      #
      # if get here, we tried 3 times, we give up:
      #
      break

    return response

  except Exception as e:
    print("**ERROR**")
    logging.error("web_service_get() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return None
    

############################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number

  Parameters
  ----------
  None

  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  try:
    print()
    print(">> Enter a command:")
    print("   0 => end")
    print("   1 => upload pdf")
    print("   2 => get analysis of pdf")
    print("   3 => chat")

    cmd = input()

    if cmd == "":
      cmd = -1
    elif not cmd.isnumeric():
      cmd = -1
    else:
      cmd = int(cmd)

    return cmd

  except Exception as e:
    print("**ERROR")
    print("**ERROR: invalid input")
    print("**ERROR")
    return -1

############################################################
#
# upload
#
def upload(baseurl):
  """
  Prompts the user for a local filename and classname, uploading
  to AWS for processing

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  extracted text from PDF
  """

  try:
    print("Enter PDF filename>")
    local_filename = input()

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
    
    print("Enter class name in format: 'cs310', with department and class number in all lowercase:")
    classname = input()

    datastr = ""
    
    data = base64.b64encode(bytes)
    datastr = data.decode('utf-8')

    data = {"filename": local_filename, "data": datastr, 'classname': classname}

    #
    # call the web service:
    #
    url = baseurl + '/upload'
    res = requests.post(url, json=data)

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
      if res.status_code == 500:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    print("PDF uploaded")
    return

  except Exception as e:
    logging.error("**ERROR: upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

def getsummary(baseurl):
  """
  Prompts the user for classname, performs Sentiment Analysis and submits results to GPT 4o-mini for summary

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  Sentiment Analysis Score / 10, GPT summary of key reviews
  """

  try:
    print("Enter class name in format: 'cs310', with department and class number in all lowercase:")
    classname = input()


    data = {'classname': classname}

    url = baseurl + '/summary'
    res = requests.post(url, json=data)

    print(res)

    #
    # let's look at what we got back:
    #
    if res.status_code == 200: #success
      print(res.json())
    elif res.status_code == 400: # no such user
      body = res.json()
      print(body)
      return
    else:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 500:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    return

  except Exception as e:
    logging.error("**ERROR: upload() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#
# chat
#
def chat(baseurl):
  """
  Prompts the user for a question and makes a call to Llama3 for an answer

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  Llama3 response to query
  """

  try:
    print("Starting the chat: you can ask general questions related to class selection or career advice. (type q to quit):")
    prompt = input()

    while (prompt != "q"):

      data = {"prompt": prompt}

      #
      # call the web service:
      #
      url = baseurl + '/chat'
      res = requests.post(url, json=data)

      print("\n")

      #
      # let's look at what we got back:
      #
      if res.status_code == 200: #success
        body = res.json()
        print(body['result'])

        print("\nYou can continue asking questions. Type q to quit.")
        prompt = input()
      elif res.status_code == 400:
        body = res.json()
        print(body)
        return
      else:
        # failed:
        print("Failed with status code:", res.status_code)
        print("url: " + url)
        if res.status_code == 500:
          # we'll have an error message
          body = res.json()
          print("Error message:", body)
        #
        return

    return

  except Exception as e:
    logging.error("**ERROR: chat() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

try:
  print('** Welcome to CTex **')
  print()

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0

  baseurl = 'base'

  #
  # make sure baseurl does not end with /, if so remove:
  #
  if len(baseurl) < 16:
    print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
    sys.exit(0)

  if baseurl == "https://YOUR_GATEWAY_API.amazonaws.com":
    print("**ERROR: update config file with your gateway endpoint")
    sys.exit(0)

  if baseurl.startswith("http:"):
    print("**ERROR: your URL starts with 'http', it should start with 'https'")
    sys.exit(0)

  lastchar = baseurl[len(baseurl) - 1]
  if lastchar == "/":
    baseurl = baseurl[:-1]

  #
  # main processing loop:
  #
  cmd = prompt()

  while cmd != 0:
    if cmd == 1:
      upload(baseurl)
    elif cmd == 2:
        getsummary(baseurl)
    elif cmd == 3:
      chat(baseurl)
    else:
      print("** Unknown command, try again...")
    #
    cmd = prompt()

  #
  # done
  #
  print()
  print('** done **')
  sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)
