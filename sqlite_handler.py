#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import logging
import os
import sqlite3
from datetime import datetime

class SQLiteHandler(logging.Handler): # Inherit from logging.Handler
    """
    Logging handler that write logs to SQLite DB
    """
    def __init__(self, filename=None, reset=False):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        if filename == None:
            filename = os.path.basename(__file__ + '.log.sqlite3db')
        self.filename = filename
        db = sqlite3.connect(self.filename)
        # collumn names from https://docs.python.org/3/library/logging.html#logrecord-attributes
        db.execute(
            'CREATE TABLE IF NOT EXISTS debug(args text, \
            created text, exc_info text, filename text, funcName text, \
            levelname text, levelno text, lineno text, module text, msecs text, \
            msg text, name text, pathname text, process text, processName text, \
            relativeCreated text, stack_info text, thread text, threadName text)')
        db.commit()
        db.close()

    def emit(self, record):
        # record.message is the log message
        db = sqlite3.connect(self.filename)

        # convert all record values into strings (using a copy of record.__dict__)
        recordDict = record.__dict__
        for key in recordDict.keys():
            recordDict[key] = str(recordDict[key])
            # print(key + '\t\t' + recordDict[key])

        db.execute(
            'INSERT INTO debug(args, created, exc_info, filename, \
            funcName, levelname, levelno, lineno, module, msecs, msg, name, \
            pathname, process, processName, relativeCreated, stack_info, \
            thread, threadName) \
            VALUES(:args, :created, :exc_info, :filename, \
            :funcName, :levelname, :levelno, :lineno, :module, :msecs, :msg, :name, \
            :pathname, :process, :processName, :relativeCreated, :stack_info, \
            :thread, :threadName)', recordDict)
        db.commit()
        db.close()

if __name__ == '__main__':
    # Create a logging object (after configuring logging)
    logger = logging.getLogger('someLoggerNameLikeDebugOrWhatever')
    logger.setLevel(logging.DEBUG)
    # logger.addHandler(SQLiteHandler('debugLog.sqlite3db'))
    logger.addHandler(SQLiteHandler())
    logger.debug('Test 1')
    # logger.warning('Some warning')
    # logger.error('Alarma!')
