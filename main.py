from fastapi import FastAPI,HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='postgres'
)

cursor = connection.cursor()
class Student(BaseModel):
    id:int = None
    name: str = None
    course:str = None

# Get all students
@app.get('/student')
def get_all_students():
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    print(rows)

    result = []

    for row in rows:
        result.append({
            'id': row[0],
            'name': row[1],
            'course': row[2]
        })

    return result
#GET single student
@app.get('/student/{id}')
def get_single_student(id:int):
    try:
        cursor.execute('SELECT * FROM students WHERE id =%s',(id,))
        row = cursor.fetchone()
        return{
            'id': row[0],
            'name': row[1],
            'course': row[2]
        }
    except:
        raise HTTPException(status_code=404,detail='Invalid Student ID')
# create student record
@app.post('/student')
def create_student_record(student:Student):
    try:
        cursor.execute('INSERT INTO students VALUES(%s,%s,%s)',(student.id,student.name,student.course))
        connection.commit()
        raise HTTPException(status_code=201,detail='Student Record Created Successfully')
    except psycopg2.IntegrityError:
  
        connection.rollback()
        raise HTTPException(status_code=500,detail="StudentID already exist")

# update student record
@app.put('/student/{id}')
def update_student_record(id:int,student:Student):
    cursor.execute('UPDATE students SET id=%s,name=%s,course=%s WHERE id=%s',(student.id,student.name,student.course,id))
    if(cursor.rowcount==0):
            raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    raise HTTPException(status_code=201,detail='Student Record Updated Successfully')

#partial update student record
@app.patch('/student/{id}')
def partial_update(id:int,student:Student):

    if(student.id != None):
        cursor.execute('UPDATE students SET id=%s WHERE id=%s',(student.id,id))
    if(student.name != None):
        cursor.execute('UPDATE students SET name=%s WHERE id=%s',(student.name,id))
    if(student.course != None):
        cursor.execute('UPDATE students SET course=%s WHERE id=%s',(student.course,id))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail='Invalid ID')
    connection.commit()
    raise HTTPException(status_code=200, detail='Partial Update successful')

# delete student record
@app.delete('/student/{id}')
def delete_student(id:int):
     cursor.execute('DELETE FROM students WHERE id=%s',(id,))
     if(cursor.rowcount==0):
             raise HTTPException(status_code=404,detail='Invalid ID')
     connection.commit()
     raise HTTPException(status_code=200,detail='Delete Successfully')
