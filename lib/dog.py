import sqlite3

CONN = sqlite3.connect('lib/dogs.db')

CURSOR = CONN.cursor()

class Dog:

    new = []

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None
        


    @classmethod
    def create_table(self):
        sql = """
              CREATE TABLE IF NOT EXISTS dogs (
              id INTEGER PRIMARY KEY,
              name TEXT,
              breed TEXT
              )
              """
        CURSOR.execute(sql)

        CONN.commit()

    
    def save(self):
      
       sql = """ INSERT INTO dogs (name, breed) VALUES (?,?)"""
       CURSOR.execute(sql, (self.name, self.breed))

       self.id = CURSOR.lastrowid
       CONN.commit()
    
    @classmethod
    def create(cls, name, breed):

        sql = """INSERT INTO dogs (name, breed) VALUES (?,?)"""
        CURSOR.execute(sql, (name,breed))
        CONN.commit()
        new_dog = cls(name, breed)
        new_dog.id = CURSOR.lastrowid
        return new_dog

    @staticmethod
    def drop_table():

        sql = """
              DROP TABLE IF EXISTS dogs
              """
        CURSOR.execute(sql)

        CONN.commit()

    @classmethod
    def new_from_db(cls,db_data):
        #new dog instance from db
        id,name, breed = db_data
        new_dog = cls(name, breed)

        new_dog.id = id
        return new_dog
    @classmethod
    def get_all(cls):
        sql = """
              SELECT * FROM dogs
          """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dogs.append(cls.new_from_db(row))

        return dogs
    @classmethod
    def find_by_name(cls, name):
       
            sql = "SELECT * FROM dogs WHERE name = ?"
            CURSOR.execute(sql, (name,))
            row = CURSOR.fetchone()
            if row:
                return cls.new_from_db(row)
            
            else:
                return None
        
    @classmethod
    def find_by_id(cls, id):
            sql = "SELECT * FROM dogs WHERE id = ?"
            CURSOR.execute(sql, (id,))
            row = CURSOR.fetchone()
            if row:
                return cls.new_from_db(row)
            
            else:
                return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)
        
    def update(self, new_name, new_breed):
        
        self.name = new_name
        self.breed = new_breed
        self.save()
    







