from flask_restful import Resource, fields, marshal_with,reqparse
from models import Course
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
        print( "using course get method for course id ")
        course = db.session.query(Course).filter(Course.course_id == courseId).first()

        if course:
            return { "course_id": course.course_id, "course_name": course.course_name, "course_code": course.course_code, "course_description": course.course_description}
        else:
            return "", 404
    
    def post(self):
        args =Course_parser.parse_args()
        course_name = args.get("course_name", None) 
        course_code = args.get("course_code", None)
        course_description = args.get("course_description", None)

        if course_name is None:
            raise BusinessValidationError(status_code= 400, error_code=	"COURSE001", error_message= "Course Name is required")
        pass
class student(Resource):
    def get(self, student_id):
        print( "your student_id is : " + str(student_id))
        return str(student_id)