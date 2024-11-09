import sqlite3

class ReportDB():
    def __init__(self):
        self.db_name = "report.db"
        self.init_db()

    def init_db(self):
        con = sqlite3.connect("report.db")
        cur = con.cursor()
        
        cur.execute("""
            create table if not exists 
            database_connection (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , 
                alias TEXT UNIQUE,
                db_type TEXT NOT NULL,
                connection_string TEXT NOT NULL
            )""")

        cur.execute("""
            create table if not exists
            group_type (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                name TEXT UNIQUE
            )""")

        cur.execute("""
            create table if not exists
            report (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                name TEXT UNIQUE,
                command TEXT,
                db_conn INTEGER,
                FOREIGN KEY(db_conn)
                    REFERENCES database_connection(id)
            )""")

        cur.execute("""
            create table if not exists
            report_group (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                report INTEGER,
                group_type INTEGER,
                FOREIGN KEY(report)
                    REFERENCES report(id)
                FOREIGN KEY(group_type)
                    REFERENCES group_type(id)
            )""")

        cur.execute("""
            create table if not exists
            report_parameter (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                is_default BOOLEAN,
                report INTEGER
                    REFERENCES report(id)
            )""")

        cur.execute("""
            create table if not exists
            parameter (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                key TEXT NOT NULL,
                value TEXT,
                report_parameter INTEGER
                    REFERENCES report_parameter(id)
            )""")

        con.commit()
        con.close()


    """//////////// database_connection ////////////////"""


    def add_db_connections(self, data):
        self.add_all("""
            insert into database_connection(
                alias, db_type, connection_string
            ) values (
                :alias, :db_type, :connection_string
            )""", data)
   
    def update_db_connection(self, data):
        self.update("""
        update database_connection
        set connection_string=:con_str
        where id=:con_id
        """, data)

    def remove_db_connection(self, _id):
        """ removes db connection """    
        self.remove_one("""
            delete from database_connection
            where id=:id
        """, {"id":_id})

    def list_db_connections(self):
        """ lists all database connections """
        return self.list("select * from database_connection")


    """//////////////// report_group /////////////////"""


    def add_groups(self, data):
        """ add multiple groups """
        self.add_all("""
            insert into group_type(
                 name
            ) values (
                :name
            )""", data)

    def remove_group(self, _id):
        """ removes group """
        self.remove_one("""
            delete from group_type
            where id=:i
        """, {i:_id})

    def list_groups(self):
        """ lists all groups"""
        return self.list("select * from group_type")

    
    """////////////////// report_group ///////////////// """


    def  list_report_group_by_group(self, grp_id):
        query = f"""select * from report_group where
                         group_type={grp_id}"""
        return self.list(query)
    

    """///////////////// parameter ////////////////// """

    def list_default_parameters_by_report(self,rep_id):
        query = f"""
            select 
                * 
            from parameter 
            where report_parameter = (
                select id 
                from report_parameter
                where report={rep_id} and is_default=True
            )"""
        return self.list(query)

    """////////////////// report //////////////////////// """


    def list_reports(self):
        """ provides the list of reports """
        self.list("select * from report")

    def list_reports_by_group(self, grp_id):
        rep_grps = self.list_report_group_by_group(grp_id)
        report_ids = [ str(rg[2]) for rg in rep_grps ] 
        ids = ", ".join(report_ids)
        return self.list(f"select * from report where id in ({ids})")

    def add_report(self, data):
        """ creates new report """
        
        rep_id = self.add_one("""
            insert into report (name, command, db_conn)
            values (:name, :cmd, :conn)
            """, {
                "name": data['name'], 
                "cmd": data['command'], 
                "conn": data["db_conn"]})
        
        if len(data["groups"]) > 0:
            rep_grp = []
            for grp_id in data["groups"]:
                rep_grp.append({"r_id": rep_id, "g_id": grp_id})
            self.add_all("""
                insert into report_group(report, group_type)
                values (:r_id, :g_id)
                """, rep_grp)
        rep_param = data["report_parameter"]
        if "parameters" in rep_param and len(rep_param["parameters"]) > 0:
            is_default = rep_param["is_def"]
            rp_id = self.add_one("""
                insert into report_parameter(is_default, report)
                values (:d, :r)
                """, {"d": is_default, "r":rep_id})
            params = []
            for param in rep_param["parameters"]:
                params.append({
                    "k": param["key"], 
                    "v": param["value"], 
                    "rp": rp_id
                })
            self.add_all("""
                insert into parameter (key,value,report_parameter)
                values(:k, :v, :rp)
                """, params)


    def remove_report(self, _id):
        """ removes report by report id """
        self.remove_one("""
            delete from report
            where id=:i
        """, {i:_id})

    """///////////////// generic functions ///////////////"""


    def list(self, query):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute(query)
        res = cur.fetchall()

        con.close()
        return res

    def add_all(self, query, data):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.executemany(query, data)
        
        con.commit()        
        con.close()

    def add_one(self, query, data):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute(query, data)
        rowId = cur.lastrowid
        con.commit()        
        con.close()
        return rowId

    def remove_one(self, query, data):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute(query,data)

        con.commit()
        con.close()

    def update(self, query, data): 
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        cur.execute(query,data)

        con.commit()
        con.close()
