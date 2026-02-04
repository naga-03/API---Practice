from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

students = []
student_id = 1

class StudentIn(BaseModel):
    name: str
    department:str
    year:int
    
class StudentOut(StudentIn):
    id:int
    
@app.post("/students",response_model=StudentOut)
def create_student(student:StudentIn):
    global student_id
    
    new_student = {
        "id" : student_id,
        "name":student.name,
        "department" : student.department,
        "year" : student.year      
    }
    
    students.append(new_student)
    student_id += 1
    return new_student

@app.get("/students",response_model=list[StudentOut])
def list_all_student():
    return students

@app.get("/students/{student_id}",response_model=StudentOut)
def get_student(student_id:int):
    for student in students:
        if student["id"]==student_id:
            return student
    raise HTTPException(status_code=404,detail="student not found")
        
@app.put("/students/{student_id}",response_model=StudentOut)
def update_student(student_id:int,updated_student:StudentIn):
    for student in students:
        if student["id"]==student_id:
            student["name"]=updated_student.name
            student["department"]=updated_student.department
            student["year"]=updated_student.year
            return student
    raise HTTPException(status_code=404,detail="student not found")

@app.delete("/students/{student_id}",response_model=StudentOut)
def delete_student(student_id:int):
    for index,student in enumerate (students):
        if student["id"]==student_id:
            deleted_student = students.pop(index)
            return deleted_student
    raise HTTPException(status_code=404,detail="student not found")
        