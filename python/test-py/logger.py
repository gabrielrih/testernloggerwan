# Reference: https://docs.python.org/3/library/logging.html
import logging

# Create and configure connectionLog
logging.basicConfig(filename="test.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w')
 
# Creating an object
connectionLog = logging.getLogger()
 
# Setting the threshold of connectionLog to DEBUG
connectionLog.setLevel(logging.DEBUG)
 
# Test messages
connectionLog.debug("Harmless debug Message")
connectionLog.info("Just an information")
connectionLog.warning("Its a Warning")
connectionLog.error("Did you try to divide by zero")
connectionLog.critical("Internet is down")