from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent/"students.json"
def read_file():
    with open(DATA_FILE,"r") as f:
        return json.load(f)
    
def write_file(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)
    
app = FastAPI()

class StudentIn(BaseModel):
    name: str
    department:str
    year:int
    
class StudentOut(StudentIn):
    id:int
    
@app.post("/students",response_model=StudentOut)
def create_student(student:StudentIn):
    data = read_file()
    
    new_id=data["last_id"]+1
    
    new_student = {
        "id" : new_id,
        "name":student.name,
        "department" : student.department,
        "year" : student.year      
    }
    
    data["students"].append(new_student)
    data["last_id"]=new_id
    write_file(data)
    return new_student

@app.get("/students",response_model=list[StudentOut])
def list_all_student():
    data=read_file()
    return data["students"]

@app.get("/students/{student_id}",response_model=StudentOut)
def get_student(student_id:int):
    data=read_file()
    for student in data["students"]:
        if student["id"]==student_id:
            return student
    raise HTTPException(status_code=404,detail="student not found")
        
@app.put("/students/{student_id}",response_model=StudentOut)
def update_student(student_id:int,updated_student:StudentIn):
    data=read_file()
    for student in data["students"]:
        if student["id"]==student_id:
            student["name"]=updated_student.name
            student["department"]=updated_student.department
            student["year"]=updated_student.year
            write_file(data)
            return student
    raise HTTPException(status_code=404,detail="student not found")

@app.delete("/students/{student_id}",response_model=StudentOut)
def delete_student(student_id:int):
    data=read_file()
    for index,student in enumerate (data["students"]):
        if student["id"]==student_id:
            deleted_student=data["students"].pop(index)
            write_file(data)
            return deleted_student
    raise HTTPException(status_code=404,detail="student not found")
        