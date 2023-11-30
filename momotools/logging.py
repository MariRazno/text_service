#!/usr/bin/env python3
"""
   module supporting logging functions
"""

import datetime


class Logger():
  """
    logging functionality allowing to log at different log-levels, optionally
    including date and time, optionally indenting according to call hierarchy. 
    
    implemented as a singleton with a public constructor that throws if called
    twice.
    
    Use, in the main module:
    
    .. code-block:: python

      from momotools import logging
      logger = logging.Logger({
        "logFile" : "debug.log",
        "logLevel" : "DEBUG"
      });
      logger.debug("first logged message")``

    and in other modules
    
    .. code-block:: python

      from momotools import logging
      logger = logging.Logger.getLogger()
      logger.debug("another logged message")
  """

  # static variables
  DEBUGLEVEL = 40
  INFOLEVEL = 30                # message that provide context to error messages 
  WARNLEVEL = 20
  ERRORLEVEL = 10
  logger = None                 # the one instance that is set in a private constructor call
  ofname = "debug.log"
  ostream = None                # opened in the first log-message to the path in ofname
  level = ERRORLEVEL
  indent = 0                    # the number of spaces prefixed before the next message
  lastMessage = None            # used to detect the firsts log-message
  logTimeSlice = None           # co-logs messages from a call to startTimeSlice, to be retrieved with getTimeSliceLog 
  timeSliceLevel = WARNLEVEL    # the logging-level that is to be co-logged

  LEVELMAP = {
   "DEBUG" : DEBUGLEVEL,
   "INFO" : INFOLEVEL,
   "WARN" : WARNLEVEL,
   "ERROR" : ERRORLEVEL
  }

  # "singleton" get
  @staticmethod
  def getLogger():
    if Logger.logger == None:
      logger = Logger()
    return Logger.logger

  def setLogFile(self, logFilePath):
    Logger.ofname = logFilePath

  def setLogLevel(self, level):
    try:
      self.level = self.LEVELMAP[level]
    except KeyError as e:
      raise Exception("invalid log level: " + level + " use one of: DEBUG, WARN, INFO, ERROR")



  # singleton constructor, throws if logger has been instantiated before
  def __init__(self):
    """
    instantiate and set the logLevel according to request.logLevel (default:ERRORLEVEL) 
    and set the name of the output-file according to request.logFile (default: debug.log)
    """

    if Logger.logger == None:
      Logger.logger = self
    else:
      # a logger has been instantiated, which can only be the result of user-code
      # calling this constructor, which is not intended
      raise Exception("incorrect constructor call:  Please use Logger.getLogger() instead")


  #
  def startTimeSlice(self, level):
    self.logTimeSlice = ''
    try:
      self.timeSliceLevel = self.LEVELMAP[level]
    except KeyError as e:
      raise Exception("invalid log level: " + level + " use one of: DEBUG, WARN, INFO, ERROR")

  def getTimeSliceLog(self):
    logged_msg = self.logTimeSlice
    self.logTimeSlice = None
    return logged_msg

  # the simplest call
  def debug(self, msg):
    self.debug_(msg, 0)

  # prepend the message with a timestamp
  def debugTime(self, msg):
    self.debug_(str(datetime.datetime.now()) + ": "  + msg, 0)

  # with '_' allows to specify an indent-change
  def debug_(self, msg, indentChange):
    self.log(self.DEBUGLEVEL, msg, indentChange)

  # both  timestamp and indent-change
  def debugTime_(self, msg, indentChange):
    self.debug_(str(datetime.datetime.now()) + ": "  + msg, indentChange)

  # the same 4 methods for level=WARNING
  def warning(self, msg):
    self.warning_(msg, 0)
  def warningTime(self, msg):
    self.warning_(str(datetime.datetime.now()) + ": "  + msg, 0)
  def warningTime_(self, msg, indentChange):
    self.warning_(str(datetime.datetime.now()) + ": "  + msg, indentChange)
  def warning_(self, msg, indentChange):
    self.log(self.WARNLEVEL, msg, indentChange)

  # only the basic method for level=INFO
  def info(self, msg):
    self.log(self.INFOLEVEL, msg, 0)

  # the same 4 methods for level=ERROR
  def error(self, msg):
    self.error_(msg, 0)
  def errorTime(self, msg):
    self.error_(str(datetime.datetime.now()) + ": "  + msg, 0)
  def errorTime_(self, msg, indentChange):
    self.error_(str(datetime.datetime.now()) + ": "  + msg, indentChange)
  def error_(self, msg, indentChange):
    self.log(self.ERRORLEVEL, msg, indentChange)

  # flush doesnt seem to flush ??? currently not used 
  def flush(self):
    self.ostream.close()
    self.ostream = open(self.ofname, "a")

  # meant to be "private": the method that 
  # implements the logging.
  def log(self, level, msg, indentChange):

    if level > self.level:
      return

    if type(msg) != type("string"):
      msg = str(msg)

    if Logger.lastMessage == None:
      # this is the first logging message, need to open log-file
      Logger.lastMessage = msg
      self.ostream = open(Logger.ofname, 'w')
      self.ostream.write( str(datetime.datetime.now()) + " logging started with level: " + str(Logger.level))

    self.ostream.write('\n' + (' '*self.indent) + msg)
    self.ostream.flush()

    # append a copy of the msg to logTimeSlic if active (i.e. not None)
    if type(self.logTimeSlice) == type('') and level <= self.timeSliceLevel:
      self.logTimeSlice = self.logTimeSlice + '\n' + (' '*self.indent) + msg

    # adapte indent based on the argument indentChange
    if indentChange > 0:
      self.indent += indentChange
    if indentChange < 0:
      self.indent += indentChange
      if self.indent < 0:
        self.indent = 0

    

