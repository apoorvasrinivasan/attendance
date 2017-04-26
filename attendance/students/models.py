from attendance import db
import datetime


class StudentPaper(db.EmbeddedDocument):
    paper_id = db.IntField()
    tut_group = db.IntField()
    prac_group = db.IntField()

    
class Student(db.Document):
    batch_id = db.IntField(required=True)
    roll_no = db.StringField(required=True)
    name = db.StringField(max_length=255)
    papers = db.ListField(db.EmbeddedDocumentField(StudentPaper))
    def __str__(self):
        return self.name

    def to_dict(self):
      return {
        'roll_no' : self.roll_no,
        'name' : self.name,
        'tut_group' : self.tut_group
      }

class Batch(db.Document):
    batch_id = db.SequenceField(required=True, unique=True)
    program = db.StringField(max_length=255)
    course = db.StringField(max_length=255)
    section = db.StringField(max_length=255)
    is_active = db.BooleanField(default=True)
    created_on = db.DateTimeField(default=datetime.datetime.now)
    
    @property
    def students(self):
      return Student.objects.filter(batch_id = self.batch_id)      
    def __str__(self):
        return "%s (%s)" % (self.program, self.batch)
 
    def to_dict(self, full=False):
      keys = ['batch_id','program','course','section']
      temp  = {}
      for k in keys:
        temp[k] = getattr(self,k)
      temp['created_on'] = self.created_on.isoformat()
      if full:
        temp['students'] = [s.to_dict() for s in self.students]
      return temp

class Semester(db.EmbeddedDocument):
    name = db.IntField(
        default=1, required=True, choices=[(i, i) for i in range(6)])
    start_date = db.DateTimeField(default=datetime.datetime.now)
    end_date = db.DateTimeField(default=lambda :datetime.datetime.now() + datetime.timedelta(180))


    def __str__(self):
        return self.name

class Paper(db.Document):
    paper_id = db.IntField(required=True, unique=True)
    name = db.StringField(max_length = 255)
    batch = db.ReferenceField(Batch, required = True)
    semester = db.EmbeddedDocumentField(Semester)
    

ATTENDANCE_OPTIONS =[
 'practical',
 'tuitorial',
 'lecture',
]
class Attendance(db.Document):
    student = db.StringField(required=True)
    paper_id = db.SequenceField(required=True)
    class_type = db.IntField(choices=[(i,x) for i,x in enumerate(ATTENDANCE_OPTIONS)], default=2)
    group = db.IntField(null = True)
    present = db.ListField(db.DateTimeField(default=datetime.datetime.now))
    absent = db.ListField(db.DateTimeField(default=datetime.datetime.now))
    is_active = db.BooleanField(default=False)
    created_on = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "%s (%s)" % (self.batch_id, self.semester)
# signals.pre_save.connect(update_modified)



### ADMIN  

from attendance import  admin
from flask_admin.contrib.mongoengine import ModelView




class BatchView(ModelView):
    can_delete = False  
    # column_exclude_list = ['students', ]
    form_excluded_columns = ['created_on']
    form_widget_args = {
        'created_by': {
            'readonly': True
        },
    }
admin.add_view(BatchView(Batch))
admin.add_view(ModelView(Student))
admin.add_view(ModelView(Attendance))
