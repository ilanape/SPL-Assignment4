import sqlite3
from DTO import Vaccine, Supplier, Clinic, Logistic

# Data Access Objects:
# All of these are meant to be singletons
class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier , quantity) VALUES (?, ?,?,?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def remove_amount_inventory(self, amount):
        c = self._conn.cursor()
        while amount > 0 :
            this_vaccine = c.execute(""" SELECT * FROM vaccines ORDER BY date LIMIT 1""").fetchone()
            if this_vaccine[3] > amount:
                self.update_quantity(this_vaccine[0], amount)
                amount = 0
            elif this_vaccine[3]== amount:
                c.execute("""DELETE FROM vaccines WHERE id == ?""", [this_vaccine[0]])  # all the amount is used
                amount = 0
            else: #vaccine.quantity < amount
                amount = amount - this_vaccine[3]
                c.execute("""DELETE FROM vaccines WHERE id == ?""", [this_vaccine[0]])  # all the amount is used

    def update_quantity(self, vaccine_id, amount):
        self._conn.execute("""UPDATE vaccines SET quantity = quantity - ? WHERE id = ? """, [amount, vaccine_id])

    #finds the next unique index to add
    def find_index(self):
        c = self._conn.cursor()
        max_index = c.execute(""" SELECT MAX(id) FROM vaccines""").fetchone()[0]
        return max_index + 1

    #for output
    def total_inventory(self):
        c = self._conn.cursor()
        s = c.execute(""" SELECT SUM(quantity) FROM vaccines """).fetchone()[0]
        return s



class Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name,logistic) VALUES (?, ?,?)
        """, [supplier.id, supplier.name, supplier.logistic])

    def find_by_name(self, _name):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE name= ?""", [_name])
        return Supplier(*c.fetchone())



class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id, location, demand,logistic) VALUES (?, ?, ?,?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find_by_location(self, _location):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM clinics WHERE location= ?
            """, [_location])
        return Clinic(*c.fetchone())

    def reduce_amount_demand(self, _id, amount):
        self._conn.execute("""
        UPDATE clinics SET demand = demand - ? WHERE id= ?""", [amount, _id])

    #for output
    def total_demand(self):
        c = self._conn.cursor()
        demand = c.execute(""" SELECT SUM(demand) FROM clinics """).fetchone()[0]
        return demand



class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO logistics (id, name, count_sent,count_received) VALUES (?, ?, ?,?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def update_count_received(self, logistic_id, amount):
        self._conn.execute("""UPDATE logistics SET count_received= count_received+ ? WHERE id=?""",
                           [amount, logistic_id])

    def update_count_sent(self, logistic_id, amount):
        self._conn.execute("""UPDATE logistics SET count_sent=count_sent+ ? WHERE id=?""", [amount, logistic_id])

    #for output
    def total_received(self):
        c = self._conn.cursor()
        received = c.execute(""" SELECT SUM(count_received) FROM logistics """).fetchone()[0]
        return received

    # for output
    def total_sent(self):
        c = self._conn.cursor()
        sent = c.execute(""" SELECT SUM(count_sent) FROM logistics """).fetchone()[0]
        return sent
