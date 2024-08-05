"""
4. Design a Logging and Monitoring System:
Question: Design a logging and monitoring system for a distributed data processing application.
The system should collect logs from different components and provide real-time monitoring and alerting.

PROPOSED SOLUTION:
each component will have a uses-a relationship with the logger
one monitor which will aggregate all the logger files' data into one and give alerts
logger object writes to a particular path for each component
logger read and write operations
"""

from abc import ABC, abstractmethod
from typing import List


class LogWriter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def write(self, data, location=None):
        pass


class StdOutWriter(LogWriter):
    def write(self, data, location=None):
        print(data)


class DiskWriter(LogWriter):
    def write(self, data, location=None):
        if not location:
            raise Exception("Location for writing the log not provided.")
        with open(f"{location}", 'a') as file:
            file.write(data)


class RemoteWriter(LogWriter):
    # writing at an endpoint
    def write(self, data, location=None):
        if not location:
            raise Exception("Location for writing the log not provided.")
        with open(f"{location}", 'a') as file:
            file.write(data)


class Logger:
    def __init__(self, logwriter:List[int], dest_path:str=None, filename:str=None ):
        """

        :param dest_path: path to where the log file be saved and written to
        :param filename: log file name
        :param logwriter: {0: StdOutWriter, 1: DiskWriter, 2: RemoteWriter}
        """

        self.location =  dest_path +"/"+ filename if dest_path and filename else None
        log_writer_map = {0: StdOutWriter, 1: DiskWriter, 2: RemoteWriter}
        self.logWriter: List[LogWriter] = []
        for writer in logwriter:
            if writer in log_writer_map:
                self.logWriter.append(log_writer_map[writer]())
            else:
                raise Exception("Wrong Logwriter type input. Can be:{0: StdOutWriter, 1: DiskWriter, 2: RemoteWriter}")

    def write(self, data):
        for writer in self.logWriter:
            writer.write(data, self.location)

# class Monitor:
#     def __init__(self, src_path):
#         self.src_path = src_path
#
#     def read_log(self, file_name):
#         with open(f"{self.src_path}/{file_name}", "r") as file:
#             for line in file:
#                 print(line)


if __name__ == "__main__":
    logger = Logger([0])
    logger.write("hello world")

    logger_2 = Logger([0, 1], ".", "mylog.log")
    logger_2.write("hello world for 0 and 1")


