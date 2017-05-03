from flask import Blueprint, render_template, abort, request
from .models import Batch, Student, Paper
from attendance import utils
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
            return utils.response({'error':'student doesnt exists'},400)
        except Exception ,e:
            return utils.response({'error':str(e)},500)
    
    batch_id = request.args.get('batch_id')
        # return utils.response([b.to_dict(True) for b in Student.objects.all()])
    if batch_id:
        return Student.objects.filter(batch_id = batch_id).to_json()
    return Student.objects.all().to_json()


@students.route('/attendance/<batch_id>', methods=['POST','GET'])
def attendance(roll=None):
    pass;