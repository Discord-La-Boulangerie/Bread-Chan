import datetime as dat
import os

def log(errorOrStr: Exception | str)-> None:
    log_fp = os.path.join(os.path.dirname(__file__), 'logs.log')
    msg = f"{dat.datetime.now().time()} | {errorOrStr}"
    print(msg)
    with open(log_fp, "a") as logFile:
        logFile.write(f"{msg}\n")
