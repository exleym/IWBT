"""
    River Module contains class River
    Interacts with database for creating, accessing, and updating entries in Iwbt.Rivers
"""

import MySQLdb as mdb


class River(object):
    """ TODO: Write documentation for River class """

    def __init__(self, river_name=None, river_id=None, section=None, con=None):
        self.name = river_name
        self.section = section
        self.river_id = river_id
        self.con = self._make_db_con(con)
        self.check_river_id()

    def check_river_id(self):
        if self.river_id is None:
            assert self.section is not None
            sql = "SELECT RiverId FROM Rivers WHERE RiverName = '" + self.name + "' AND Section = '" + self.section + \
                "'"
            self.con.query(sql)
            river_id = self.con.store_results().fetch_row()
            if river_id is None:
                sql = "SELECT MAX(RiverId) FROM Rivers"
                self.con.query(sql)
                river_id = int(self.con.store_results().fetch_row()) + 1
            self.river_id = river_id
        else:
            sql = "SELECT * FROM Rivers WHERE RiverId = '" + self.river_id + "'"


    def _make_db_con(self, con=None, host='sharkbox'):
        if con is None:
            return mdb.connect(host=host, user='xwrite', pw='xwrite', db='Iwbt')
        else:
            return con

    def _set_river_id(self):
        pass

