import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed) VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()

            # Update object with the assigned ID
            self.id = CURSOR.lastrowid
            # Return the saved Dog instance
            return self
        else:
             # Update existing record
            sql = """ UPDATE dogs SET name=?, breed=? WHERE id=? """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()
            # Return the saved Dog instance
            return self

    def update(self, new_name):
        # Update the name of the Dog instance
        self.name = new_name
        # Save the updated Dog instance to the database
        return self.save()

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        rows = CURSOR.execute(sql).fetchall()

        dogs_list = [cls.new_from_db(row) for row in rows]
        return dogs_list

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()

        return cls.new_from_db(row)

    @classmethod
    def find_by_id(cls, dog_id):
        sql ="""
            SELECT *
            FROM dogs
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (dog_id,)).fetchone()

        return cls.new_from_db(row)

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)

        if existing_dog:
            return existing_dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog