import sqlite3

dbase = sqlite3.connect("dbase.db")

# dbase.execute(''' CREATE TABLE Satranc(
# ID INT PRIMARY KEY NOT NULL,
# moveLog TEXT NOT NULL,
# Oyunİsmi Text
# ) ''')

def insert(name,movestring,tahta,sırasayısı,taraf,renk):
    dbase.execute('''INSERT INTO Satranc(moveLog,Oyunİsmi,tahta,sırasayısı,taraf,renk) VALUES(?,?,?,?,?,?)''',(movestring,name,tahta,sırasayısı,taraf,renk))
    dbase.commit()

def show():
    index = dbase.execute('''SELECT ID,Oyunİsmi,moveLog,tahta,sırasayısı,taraf,renk FROM Satranc''')
    return index
def delete(id):
    idt = id
    sttt = str(idt)
    dbase.execute('''DELETE FROM Satranc WHERE ID = ?''',(sttt))
    dbase.commit()