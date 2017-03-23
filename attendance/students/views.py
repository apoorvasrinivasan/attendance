from flask import Blueprint, render_template, abort, request
from .models import Batch
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
    # return utils.response([b.to_dict(True) for b in Batch.objects.all()])
    return Batch.objects.all().to_json()

