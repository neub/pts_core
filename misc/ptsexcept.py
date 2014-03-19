class PtsException(Exception):
    pass

class PtsCritical(PtsException):
    """critical error, abort the whole test suite"""
    pass

class PtsUser(PtsException):
    """error, user intervention required"""
    pass

class PtsWarning(PtsException):
    """warning, a cautionary message should be displayed"""
    pass

class PtsInvalid(PtsException):
    """reserved: invalid parameters"""

class PtsNoBatch(PtsInvalid):
    """reserved: a suite was created without batch of tests to run"""
    pass

class PtsBadTestNo(PtsInvalid):
    """reserved: a bad test number was given"""
    pass

class PtsInfo(PtsException):
    """Information from the test, not an error"""


class PtsError(PtsException):
    """error, continue remaining tests in test suite"""
    pass

class PTS_ERROR_LOGGER:
    """Log errors and continue testing without raising an exception"""

    def __init__(self, inf, log):
        """Create PTS logger.
        :param inf is for generic *inf*ormation
        :param log is only for error
        """
    	self.inf = inf
    	self.log = log
    	self.er_count = 0

    def set(self, msg):
	self.inf.write(msg + "\n")
	self.log.write(msg + "\n")
	self.er_count = self.er_count + 1

    def get(self):
	return self.er_count


if __name__ == '__main__':
    pass
