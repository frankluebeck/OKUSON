# -*- coding: ISO-8859-1 -*-
#                       Frank Lübeck 
#
"""This modules provides access to a list of GAP jobs running in the
background.
Basic usage:
   AddGAPJob(gap='gapL', handler='')
   job = FindGAPJob()   # use a pool of GAP jobs by several threads
   job.Write("2^1000;")
   print job.Read()
   ReleaseGAPJob(job)   # give it back to the pool
"""

CVS = '$Id: GAPJob.py,v 1.1 2003/10/06 13:01:06 luebeck Exp $'

import os, sys, time, types, cStringIO, threading 

# here is a list of strings, interpreted in strings in GAP input as
# characters 0..255.
GAPchars = [
  '\\000', '\\>', '\\<', '\\c', '\\004', '\\005', '\\006', 
  '\\007', '\\b', '\\t', '\\n', '\\013', '\\014', '\\r', '\\016', 
  '\\017', '\\020', '\\021', '\\022', '\\023', '\\024', '\\025', 
  '\\026', '\\027', '\\030', '\\031', '\\032', '\\033', '\\034', 
  '\\035', '\\036', '\\037', ' ', '!', '\\"', '#', '$', '%', 
  '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', 
  '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', 
  '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 
  'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 
  'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\\\', 
  ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 
  'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
  's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', 
  '~', '\\177', '\\200', '\\201', '\\202', '\\203', '\\204', 
  '\\205', '\\206', '\\207', '\\210', '\\211', '\\212', '\\213', 
  '\\214', '\\215', '\\216', '\\217', '\\220', '\\221', '\\222', 
  '\\223', '\\224', '\\225', '\\226', '\\227', '\\230', '\\231', 
  '\\232', '\\233', '\\234', '\\235', '\\236', '\\237', '\\240', 
  '\\241', '\\242', '\\243', '\\244', '\\245', '\\246', '\\247', 
  '\\250', '\\251', '\\252', '\\253', '\\254', '\\255', '\\256', 
  '\\257', '\\260', '\\261', '\\262', '\\263', '\\264', '\\265', 
  '\\266', '\\267', '\\270', '\\271', '\\272', '\\273', '\\274', 
  '\\275', '\\276', '\\277', '\\300', '\\301', '\\302', '\\303', 
  '\\304', '\\305', '\\306', '\\307', '\\310', '\\311', '\\312', 
  '\\313', '\\314', '\\315', '\\316', '\\317', '\\320', '\\321', 
  '\\322', '\\323', '\\324', '\\325', '\\326', '\\327', '\\330', 
  '\\331', '\\332', '\\333', '\\334', '\\335', '\\336', '\\337', 
  '\\340', '\\341', '\\342', '\\343', '\\344', '\\345', '\\346', 
  '\\347', '\\350', '\\351', '\\352', '\\353', '\\354', '\\355', 
  '\\356', '\\357', '\\360', '\\361', '\\362', '\\363', '\\364', 
  '\\365', '\\366', '\\367', '\\370', '\\371', '\\372', '\\373', 
  '\\374', '\\375', '\\376', '\\377' ]

# rewrite a string for GAP input
def StringToGAP(s):
  res = cStringIO.StringIO()
  for c in s:
    res.write(GAPchars[ord(c)])
  out = res.getvalue()
  res.close()
  return out

# Translate a query dictionary to a GAP record assigned to the global
# variable GAPQUERY. Because of GAP's limitation for the maximal length of
# identifiers we cut the keys after 1000 characters.
def QueryToGAP(req):
  try: 
    qu = req.query
  except:
    qu = {}
  if not types.DictType == type(qu):
    qu = {}
  res = cStringIO.StringIO()
  res.write('GAPQUERY:=rec();;')
  for k in qu.keys():
    res.write('GAPQUERY.("')
    if len(k) > 1000:
      res.write(StringToGAP(k[:1000]))
    else:
      res.write(StringToGAP(k))
    res.write('"):="')
    res.write(StringToGAP(str(qu[k])))
    res.write('";;')
  res.write('\n')
  s = res.getvalue()
  res.close()
  return s

GAPJobs = []

# Utility to write input to a GAP job. This is done by a thread such that for 
# big input the main process can work on reading the output buffer to avoid a
# dead lock.
def WriteThreadTarget(tofile, str):
  tofile.write(str)
  tofile.write('Print("\\nGAPREQ READY\\n");\n')
  tofile.flush()

# a simple class for GAP jobs
class GAPJob(object):
  def __init__(self, inp, out):
    self.input = inp
    self.out = out
    self.lock = threading.Lock()

  # Writing and reading from a child GAP process is a bit tricky. One needs
  # some protocol to detect the end of the output for one request. And one 
  # has to avoid dead locks because of full input and/or output buffers. 
  # We provide the two functions 'WriteJobInput' and 'ReadJobOutput' as
  # examples how to avoid these traps.
  def Write(self, str):
    threading.Thread(target=WriteThreadTarget, args=(self.input, str)).start()

  # In an interactive program like GAP which is used as non-terminating 
  # filter one needs a protocol convention for marking the end of an 
  # output. We use the line 'GAPREQ READY\n' for this purpose.
  def Read(self):
    res = cStringIO.StringIO()
    l = self.out.readline()
    while l != 'GAPREQ READY\n':
      res.write(l)
      l = self.out.readline()
    str = res.getvalue()
    res.close()
    return str

# Returns a GAPJob object and appends it to the list GAPJobs.
# Be careful to use the lock in multithreaded server.
def AddGAPJob(gap='gap', handler='handler.g'):
  try:
    # Call GAP as quiet as possible, unfortunately the GAP kernel
    # writes warnings and error messages to stdout instead of stderr,
    # so be careful to avoid such garbage in your response.
    inp,out = os.popen2(gap+" -b -q -e -n -T -r "+handler, bufsize=0)
    GAPJobs.append(GAPJob(inp, out))
    return GAPJobs[-1]
  except:
    pass


# In a threading environment one has to make sure that the input of a
# background job is not clobbered by two or more threads at the same time.
# Therefore one first needs a lock for a GAP job before one should write to
# it. The following utility searches in the list of GAP jobs one that is not
# busy (i.e., used by another thread) and returns it. When all jobs are not
# available, it does a sleep for sleeptime (default 0.1) seconds and repeats
# the search up to maxtries times (the default maxtries=-1 means maxtries =
# infinity).
def FindGAPJob(sleeptime=0.1, maxtries=-1):
  tries = 0
  while tries != maxtries:
    for job in GAPJobs:
      if job.lock.acquire(0):
        return job
    time.sleep(sleeptime)
    tries += 1

def ReleaseGAPJob(job):
  job.lock.release()

