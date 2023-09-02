import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name + '.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL)')
        self.conn.commit()

    def add(self, note):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO note (title, content) VALUES (?, ?)', (note.title, note.content))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, content FROM note')
        notes = []
        for row in cursor:
            note = Note(id=row[0], title=row[1], content=row[2])
            notes.append(note)
        return notes
    
    def get(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, content FROM note WHERE id = ?', (note_id,))
        row = cursor.fetchone()
        note = Note(id=row[0], title=row[1], content=row[2])
        return note
    
    def update(self, entry):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE note SET title = ?, content = ? WHERE id = ?', (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM note WHERE id = ?', (note_id,))
        self.conn.commit()