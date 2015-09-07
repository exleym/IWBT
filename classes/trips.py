__author__ = 'exley'

"""
    Classes for Constructing, Editing, and Accessing data from Trips and TripData
"""

import data.dbcon as db

class LogEntry(object):
    def __init__(self):
        self.TripId = None
        self.UserId = None
        self.TripData = dict()
        self.con = None

    def construct(self):
        if self.con is None:
            self.con = db.make_db_connection('Iwbt', user='root', password='Z3pp3l1n')
        self.TripId = self.get_tripid()
        print self.TripId

    def get_tripid(self):
        if self.TripId is None:
            sql = "SELECT max(TripId) FROM Trips;"
            max_id = db.get_data(self.con, sql, ret_type='item')
            if max_id is not None:
                self.TripId = max_id + 1
        return self.TripId


if __name__ == '__main__':
    test = LogEntry()
    test.construct()