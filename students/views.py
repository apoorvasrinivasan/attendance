from flask import Blueprint, render_template, abort, request
from .models import Batch, Student, Paper, Attendance
from attendance import utils
import datetime
students = Blueprint('students', __name__,
                     template_folder='templates')


@students.route('/', methods=['GET'])
# @login_required
def hello():
    return "hello world"
    # return utils.response([s.to_dict() for s in SendLog.objects.all()])


@students.route('/batch', methods=['GET'])
@students.route('/batch/<bid>', methods=['GET'])
def batches(bid=None):
    if bid:
        b = Batch.objects.get(batch_id=bid)
        return b.to_json()
    detailed = request.args.get('detailed')
    if detailed:
        return utils.response([b.to_dict(True) for b in Batch.objects.all()])
    return Batch.objects.all().to_json()


@students.route('/paper', methods=['GET'])
@students.route('/paper/<pid>', methods=['GET'])
def papers(pid=None):
    if pid:
        p = Paper.objects.get(paper_id=pid)
        return p.to_json()
    detailed = request.args.get('detailed')
    if detailed:
        return utils.response([p.to_dict(True) for p in Paper.objects.all()])
    return Paper.objects.all().to_json()


@students.route('/student', methods=['GET'])
@students.route('/student/<roll>', methods=['GET'])
def student(roll=None):
    if roll:
        try:
            s = Student.objects.get(roll_no=roll)
            return s.to_json()
        except Student.DoesNotExist:
            return utils.response({'error': 'student doesnt exists'}, 400)
        except Exception, e:
            return utils.response({'error': str(e)}, 500)

    batch_id = request.args.get('batch_id')
    # return utils.response([b.to_dict(True) for b in Student.objects.all()])
    if batch_id:
        return Student.objects.filter(batch_id=batch_id).to_json()
    return Student.objects.all().to_json()

import json
@students.route('/attendance', methods=['POST'])
def attendance():
    '''
     attedance for a class
        student, tut_group, lecture, batch
    pass;
    '''
    # perm = PermSerialiser(a.object.campaigns)
    print request.data
    form_data = json.loads(request.data)
    roll_no = form_data['roll_no']
    try:
        s = Student.objects.get(roll_no=roll_no)
    except Student.DoesNotExist:
        return utils.response({"error": "Student Does not exists"}, status=400)
    paper = form_data['paper']
    student_paper = s.has_paper(paper)
    if not student_paper:
        return utils.response({"error": "Student doesnt belong to paper"},
                              status=400)
    tod = datetime.date.today()
    try:
        p = Paper.objects.get(semester__start_date__lte=tod,
                              semester__end_date__gt=tod, paper_id=paper)
    except Paper.DoesNotExist:
        return utils.response({"error": "Semester Over"}, status=400)

    at, fl = Attendance.objects.get_or_create(
        student=s.roll_no,
        paper_id=paper,
        class_type=form_data['class_type']
    )
    if not fl:
        at.present = []
    if 'present' in form_data:
        at.present.append(datetime.datetime.now())
    else:
        at.absent.append(datetime.datetime.now())
    at.save()
    # student = db.StringField(required=True)
    # paper_id = db.IntField(required=True)
    # class_type = db.IntField(choices=[(i,x) for i,x in enumerate(ATTENDANCE_OPTIONS)], default=2)
    return utils.response( status=201)
