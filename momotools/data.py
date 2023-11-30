#!/usr/bin/env python3
"""
   module supporting data functions

   * dfFromCSV
   * getDictItem
   * atob
   * assert_type
   * compare
"""

import base64
# import pandas as pd
# import numpy as np
from operator import itemgetter
# from scipy.sparse import csr_matrix
from io import StringIO

import momotools as momo
from momotools import logging
logger = momo.logging.Logger.getLogger()


T_INT = type(7)
T_FLOAT = type(7.7)
T_STRING = type("7")
T_DICT = type({})
T_LIST = type([])
T_SET = type(set())
# T_DF = type(pd.DataFrame())
# T_NPARRAY = type(np.array([]))
# T_NPMATRIX = type(np.matrix([]))
# T_CSRMATRIX = type(csr_matrix((0,0)))
# T_PDSERIES = type(pd.Series())
T_HASSHAPE = []
T_HASLEN = [T_DICT, T_LIST, T_SET, T_STRING]

# def dfFromCSV(csvString, sep_, msg):
#   assert_type(csvString, type(""), msg);
#   try:
# #    df = pd.read_csv(StringIO(csvString), sep=sep_, dtype=str);
#     # na_values=None makes that none-values are read as na,
#     # fillna('') then makes these into empty strings
#     df = pd.read_csv(StringIO(csvString), sep=sep_, na_values=None, dtype=str);
#     df = df.fillna('');
#     dfInfo = StringIO()
#     df.info(buf=dfInfo)
#     logger.debug("read into df,  " + msg + ': '  + dfInfo.getvalue())
#     return df
#   except Exception as e:
#     raise Exception(" could not read into df: " + str(e) )

# def embed_csr(sp, colTitles, newColTitles):
# 
#   """
#   used to add new named but empty columns to a csr-matrix. The data
#   must be provided as a csr_matrix that is defined with respect to a (shorter)
#   list of column-titles and we return a new csr_matrix that defines the
#   same data with respect to a longer list of column-titles in any order. An
#   exception is thrown if any old coltitle is not contained in the list of new ones
#   """
# 
#   try:
# 
#     logger.debug_("enter embed_csr", 2)
#     momo.data.assert_type(colTitles, T_LIST, "colTitles")
#     momo.data.assert_type(newColTitles, T_LIST, "newColTitles")
#     momo.data.assert_type(sp, T_CSRMATRIX, "sp")
#   
#     #% Get shape, indices and data of old csr-matrix
#     numRows, numCols = sp.shape                # two ints
#     data = sp.data                             # a numpy 1d array
#     row_indices, col_indices = sp.nonzero()    # two numpy 1d arrays
#     newShape = (numRows, len(newColTitles))
# 
#     # return an empty csr if there are no data (otherwise itemgetter fails in next paragraph)
#     if len(data) == 0:
#       logger.debug_("exit", -2)
#       return csr_matrix(newShape)
#   
#     # re-map the col-indices on the new list of column-titles
#     col_codes = pd.Series(itemgetter(*col_indices)(colTitles))             # pd.Series of strings
#     new_col_indices = col_codes.astype(pd.CategoricalDtype(newColTitles)).cat.codes   # pd.Series of indices
#     if (len(new_col_indices.loc[new_col_indices<0]) > 0):
#       raise Exception("cannot embed coltitles that are unknown in new list: " 
#       + str(col_codes.loc[new_col_indices<0].values)[0:40] )
#   
#     # return a new sparse matrix with the same data
#     logger.debug_("exit", -2)
#     return csr_matrix((data, (row_indices, new_col_indices)), shape=newShape)
# 
#   except Exception as e:
#     logger.error_(str(e), -2)
#     raise Exception(str(e) + " <pre> << embed_csr")
# 
# def filter_csr(sp, colTitles, colTitleSelection):
#   """
#   counterpart of embed_csr: from a csr_matrix that is defined with respect to a 
#   (shorter) list of column-titles, we return a new csr_matrix, returning only the
#   columns as specified in the list newColTitles. An exception is thrown if any
#   new coltitle is not available
#   """
#   try:
#     colIndexSelection = pd.Series(colTitleSelection) \
#                           .astype(pd.CategoricalDtype(colTitles)).cat.codes
#     if (len(colIndexSelection.loc[colIndexSelection<0]) > 0):
#       raise Exception("cannot filter for unknown coltitles: " 
#       + str(pd.Series(colTitleSelection).loc[colIndexSelection<0].values)[0:40] )
#     return sp.copy()[:, colIndexSelection]
# 
#   except Exception as e:
#     logger.error_(str(e), -2)
#     raise Exception(str(e), " <pre> << filter_csr")
# 
# def getDFColTitles(df, msg):
#   assert_type(df, type(pd.DataFrame()), msg);
#   return list(df.columns)


def getDictKeys(dict_, msg):
  assert_type(dict_, type({}), msg);
  return list(dict_.keys())


def getDictItem(dict_, key, msg):
  assert_type(dict_, type({}), msg);
  if (key not in dict_):
    raise Exception("no key " + key + " in: " +  msg)
    
  return dict_[key]

def getTypedDictItem(dict_, key, type_ , msg):
  item = getDictItem(dict_, key, msg)
  assert_type(item, type_, msg + '[' + key + ']')
  return item


def btoa(decoded_as_string, msg):

  decoded_as_bytes = ''
  encoded_as_bytes = ''
  encoded_as_string = ''
  assert_type(decoded_as_string, type(""), msg)
  try:
    decoded_as_bytes = decoded_as_string.encode('utf-8')
  except Exception as e:
    raise Exception("ERROR encoding base64: " + msg + " not a valid utf-8: " + str(e))

  try:
    encoded_as_bytes = base64.b64encode(decoded_as_bytes)
    encoded_as_string = encoded_as_bytes.decode('utf-8')
  except Exception as e:
    raise Exception("unexpected ERROR encoding base64: " + msg + str(e))

  return encoded_as_string


def atob(encoded_as_string, msg):

  decoded_as_bytes =  ''
  decoded_as_string = ''

  assert_type(encoded_as_string, type(""), msg)
  
  encoded_as_bytes = encoded_as_string.encode('utf-8')

  try:
    decoded_as_bytes = base64.b64decode(encoded_as_bytes)
  except Exception as e:
    raise Exception(" invalid base64: " + str(e))

  try:
    decoded_as_string = decoded_as_bytes.decode('utf-8')
  except Exception as e:
    raise Exception("invalid utf8: " + str(e))

  return decoded_as_string


def assert_type( x, expected, label):
  shapeInfo = ''
  if type(x) == expected:
    if (logger.level <= logger.DEBUGLEVEL):
      if (type(x) in T_HASSHAPE):
        shapeInfo = ' w. shape: ' + str(x.shape) 
      elif (type(x) in T_HASLEN):
        shapeInfo = ' w. len: ' + str(len(x)) 
    logger.debug(label + " is of type: " + str(expected)
                       + shapeInfo + ": " + str(x)[0:40])
  else:
    msg = label + " must be of type " + str(expected) + ", not: " + str(type(x))
    raise Exception(msg);

# def assert_df_colType(df, colTitle, expectedType, label):
# 
#   if colTitle not in list(df.columns):
#     raise Exception("no column " + colTitle + " in dataframe " + label)
#   myCol = df.loc[:,colTitle]
#   assert_pdseries_type(myCol, expectedType, " column " + colTitle + " in dataframe " + label)
# 
# def assert_pdseries_type(series, expectedType, label):
#   for i in range(0, len(series)):
#     if (type(series[i]) != expectedType):
#       raise Exception("unexpected type " + str(type(series[i])) + " at row " + str(i) 
#       + " in " + label + ", expected:" + str(expectedType))
#   logger.debug(label + " is of type: " + str(expectedType) + " len:" + str(len(series)) + " content:" + str(series))
 

class Comparator():
  """
    implements functionality to compare two data-structures on types, shape, content
  """

  compare_content = True
  compare_length = True
  checkNewCol = True
  checkMissingCol = True

  def __init__(self, logger_):
    global logger
    logger = logger_

  def dontCompareContent(self):
    self.compare_content = False

  def dontCompareLenght(self):
    self.compare_length = False
    self.compare_content = False

  def allowNewColInDF(self):
    self.checkNewCol = False;

  def allowMissingColInDF(self):
    self.checkMissingCol = False;

  def compare(self, label, x, y):
    """
    compare two datastructures x and y and throw a message that includes the provided label
    in case x doesn't equal y. The implementation is straightforward for x,y being primitive
    types and is based on a recursive call if x,y are lists or dicts. TODO: implement comparison
    of pandas.dataframes and it columns/rows/cells
    """
  
    if type(label) != type(""):
      raise Exception("1st argument to data.compare must be a string (label) ")
    try:
  
      if type(x) == T_STRING:  
        if type(y) != T_STRING:
          raise Exception(" expected string, not:" + str(type(y)))
        if self.compare_content and x != y: 
          raise Exception(" expected " + str(x) + " not:" + str(y))
        return
  
      if type(x) == T_INT: 
        if type(y) != T_INT:
          raise Exception(" expected integer, not:" + str(type(y)))
        if self.compare_content and x != y: 
          raise Exception(" expected " + str(x) + " not:" + str(y))
        return
  
      if type(x) == T_FLOAT:
        if type(y) != T_FLOAT:
          raise Exception(" expected float, not:" + str(type(y)))
        if self.compare_content and x != y: 
          raise Exception(" expected " + str(x) + " not:" + str(y))
        return
  
      if type(x) == T_LIST:
        if type(y) != T_LIST:
          raise Exception("expected list, not:" + str(type(y)))
        if self.compare_length and len(x) != len(y):
          raise Exception("expected list length: " 
          + str(len(x)) + " , not:" + str(len(y)))
        for i in range(0, min(len(x),len(y))):
          label_ = ":[" + str(i) + "]:"
          self.compare(label_, x[i], y[i]) 
        return
  
      if type(x) == T_DICT:
        if type(y) != T_DICT:
          raise Exception("expected dict, not:" + str(type(y)))
        if len(x.keys()) != len(y.keys()):
          raise Exception("expected num keys in dict: " 
          + len(x.keys()) + " , not:" + len(y.keys()))
        for key in x.keys():
          label_ = ":[\"" + key + "\"]:"
          self.compare(label_, x[key], y[key]) 
        return

      if type(x) == T_DF:
        if type(y) != T_DF:
          raise Exception("expected dataFrame, not:" + str(type(y)))

        for colKey in list(x.columns):
          if self.checkMissingCol and colKey not in list(y.columns):
            raise Exception("missing col in " + label + ": " + colKey);
          if x.dtypes[colKey] != y.dtypes[colKey]:
            raise Exception("unexpected type " + str(y.dtypes[colKey]) + " in col:" + colKey + " of: " + label + ", expected: " + str(x.dtypes[colKey]))
        for colKey in list(y.columns):
          if colKey not in list(x.columns):
            if self.checkNewCol :
              raise Exception("unexpected col in " + label + ": " + colKey);
            else:
              logger.debug("new column " + colKey + " in:" + label);

        return

      # rescue types that we did not implement abover: compare types and  string values 
      if type(x) != type(y):
        raise Exception("expected " + str(type(x)) + ", not:" + str(type(y)))
      if self.compare_content and str(x) != str(y):
        raise Exception(" expected " + str(x) + " not:" + str(y))
  
    except Exception as e:
      raise Exception(label + str(e))
    

