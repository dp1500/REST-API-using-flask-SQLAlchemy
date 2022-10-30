from flask_restful import Resource, fields, marshal_with,reqparse
from models import Course, Student, Enrollments
from database import db
from validation import *

# #defining json structure for marshal

# output_field = {
#   "course_id": 201,
#   "course_name": "Maths1",
#   "course_code": "MA101",
#   "course_description": "Course Description Example"
# }

Course_parser = reqparse.RequestParser()
Course_parser.add_argument('course_name')
Course_parser.add_argument('course_code')
Course_parser.add_argument('course_description')

class CourseApi(Resource):
    def get(self, courseId):
        
        course = db.session.query(Course).filter(Course.course_id == courseId).first()

        if course:
            return { "course_id": course.course_id, "course_name": course.course_name, "course_code": course.course_code, "course_description": course.course_description}
        else:
            return "Course not found", 404

    def put(self, courseId):  
        course = db.session.query(Course).filter(Course.course_id == courseId).first()
        if course:
            args =Course_parser.parse_args()
            course_name = args.get("course_name", None) 
            course_code = args.get("course_code", None)
            course_description = args.get("course_description", None)
            
            if (course_name is None) or (course_code is None):
                raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
        
            course.course_name = course_name
            course.course_code = course_code
            course.course_description = course_description

            db.session.commit()
            return { "course_id": course.course_id, "course_name": course.course_name, "course_code": course.course_code, "course_description": course.course_description}, 200

        else:
            return "course not found", 404
    
    def delete(self, courseId):
        course = db.session.query(Course).filter(Course.course_id == courseId).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            return "Course not found", 404
        # course = Course.query.get_or_404(courseId)

    def post(self):
        args =Course_parser.parse_args()
        course_name = args.get("course_name", None) 
        course_code = args.get("course_code", None)
        course_description = args.get("course_description", None)

        if course_name is None:
            raise BusinessValidationError(status_code= 400, error_code=	"COURSE001", error_message= "Course Name is required")
        if course_code is None:
            raise BusinessValidationError(status_code= 400, error_code=	"COURSE002", error_message= "Course Code is required")
        
        courseDuplicate = db.session.query(Course).filter(Course.course_code == course_code).first()
        if courseDuplicate:
            # raise BusinessValidationError(status_code= 409, error_code= "None",error_message= "course_code already exist")
            return "course_code already exists", 409
        
        new_course = Course(course_code = course_code,course_name= course_name,course_description = course_description)
        db.session.add(new_course)
        db.session.commit()
        
        return { "course_id": new_course.course_id, "course_name": new_course.course_name, "course_code": new_course.course_code, "course_description": new_course.course_description}, 201
        # "Successfully Created",



student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name')
student_parser.add_argument('last_name')
student_parser.add_argument('roll_number')

class StudentApi(Resource):
    def get(self, studentId):
        student = db.session.query(Student).filter(Student.student_id == studentId).first()
        if student:
            return { "student_id": student.student_id , "first_name": student.first_name, "last_name": student.last_name , "roll Number": student.roll_number}, 200
        
        else:
            return "Student not found",404
    
    def post(self):
        args =student_parser.parse_args()
        first_name = args.get("first_name", None) 
        last_name = args.get("last_name", None)
        roll_number = args.get("roll_number", None)

        if first_name is None:
            raise BusinessValidationError(status_code= 400, error_code=	"STUDENT002", error_message= "First Name is required")
            
        if roll_number is None:
            raise BusinessValidationError(status_code= 400, error_code=	"STUDENT001", error_message= "Roll Number required")
            # return { "error_code": "string","error_message": "string"}
        
        courseDuplicate = db.session.query(Student).filter(Student.roll_number == roll_number).first()
        if courseDuplicate:
            # raise BusinessValidationError(status_code= 409, error_code= "None",error_message= "course_code already exist")
            return "Student already exists", 409

        new_student = Student(first_name = first_name, last_name= last_name, roll_number = roll_number)
        db.session.add(new_student)
        db.session.commit()
        
        return { "student_id": new_student.student_id , "first_name": new_student.first_name, "last_name": new_student.last_name , "roll Number": new_student.roll_number}, 201


    def put(self, studentId):
        student = db.session.query(Student).filter(Student.student_id == studentId).first()
        if student:
            args =student_parser.parse_args()
            first_name = args.get("first_name", None) 
            last_name = args.get("last_name", None)
            roll_number = args.get("roll_number", None)
            
            if (roll_number is None) or (first_name is None):
                raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
        
            student.first_name = first_name
            student.last_name = last_name
            student.roll_number = roll_number

            db.session.commit()
            return { "student_id": student.student_id , "first_name": student.first_name, "last_name": student.last_name , "roll Number": student.roll_number}, 200
        
        else:
            return "student not found", 404

    def delete(self, studentId):
        stduent = db.session.query(Student).filter(Student.student_id == studentId).first()
        if stduent:
            db.session.delete(stduent)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            return "student not found", 404


enrollement_parser = reqparse.RequestParser()
enrollement_parser.add_argument('courseID')
 
class EnrollementsApi(Resource):
    def get(self, studentId):
        if type(studentId) == int:
            enrollement = db.session.query(Enrollments).filter(Enrollments.estudent_id == studentId).first()
            if enrollement:
                return [ { "enrollment_id": enrollement.enrollment_id, "student_id": enrollement.estudent_id, "course_id": enrollement.ecourse_id } ], 200

            else:
                return "Student is not enrolled in any course",404
        else:
            raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
            
    
    def post(self,studentId):
        args =enrollement_parser.parse_args()
        courseID = args.get("courseID", None) 
        
        student = db.session.query(Student).filter(Student.student_id == studentId).first()
        if student:
            # print(courseID)
            course = db.session.query(Course).filter(Course.course_id == courseID).first()
            if course:
                new_enrollement = Enrollments(estudent_id = studentId, ecourse_id = courseID)
                db.session.add(new_enrollement)
                db.session.commit()
                return [ { "enrollment_id": new_enrollement.enrollment_id, "student_id": new_enrollement.estudent_id, "course_id": new_enrollement.ecourse_id } ], 201


            else:
                raise BusinessValidationError(status_code= 404, error_code=	"ENROLLMENT001", error_message= "Course does not exist.")
            
        else:
            raise BusinessValidationError(status_code= 404, error_code=	"ENROLLMENT002", error_message= "Student does not exist.")
            
    def delete(self, studentId,courseId):
        if studentId == None or courseId == None:
            raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
            
        enrollement = db.session.query(Enrollments).filter((Enrollments.estudent_id == studentId) & (Enrollments.ecourse_id == courseId)).first()
        if enrollement:
            db.session.delete(enrollement)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            return "Enrollment for the student not found", 404
        