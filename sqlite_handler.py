import logging
import os
import sqlite3
from datetime import datetime

class SQLiteHandler(logging.Handler): # Inherit from logging.Handler
    """
    Logging handler that write logs to SQLite DB
    """
    def __init__(self, filename):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        self.filename = filename
        db = sqlite3.connect(self.filename) # might need to use self.filename
        db.execute("CREATE TABLE IF NOT EXISTS debug(date datetime, loggername text, filename, srclineno integer, func text, level text, msg text)")
        db.commit()
        db.close()

    def emit(self, record):
        # record.message is the log message
        db = sqlite3.connect(self.filename)
        thisdate = datetime.now()
        db.execute(
            'INSERT INTO debug(date, loggername, filename, srclineno, func, level, msg) VALUES(?,?,?,?,?,?,?)',
            (
                thisdate,
                record.name,
                os.path.abspath(record.filename),
                record.lineno,
                record.funcName,
                record.levelname,
                record.msg,
            )
        )
        db.commit()
        db.close()

if __name__ == '__main__':
    # Create a logging object (after configuring logging)
    logger = logging.getLogger('someLoggerNameLikeDebugOrWhatever')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(SQLiteHandler('debugLog.sqlite'))
    logger.debug('Test 1')
    logger.warning('Some warning')
    logger.error('Alarma!')
