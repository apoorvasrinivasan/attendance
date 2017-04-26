

# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server, Command
from attendance import app, blue
# from blue import register_blueprints
manager = Manager(app)

# Turn on debugger by default and reloader

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

@manager.command
def createapp(name):
    "Cookie Cutter"
    os.makedirs(name)
    files = ['models', 'views','serialiser']
    for f in files:
        with open("%s/%s.py"%(name,f),'w'):
            pass;   
    with open("%s/__init__.py"%(name),'w') as f:
        f.write("from flask import Blueprint\n");
        x = "%s=Blueprint('%s', __name__)\n"%(name,name)
        f.write(x);
        f.write("import views\n");
    
@manager.command
def uploadStudents(name, paper):
    from attendance.students.models import *
    f = open('../students.csv');
    b,a =  Batch.objects.get_or_create(program=name, paper=paper)
    for ff in f.readlines():
        t,roll,name = ff.split(',')
        s = Student(tut_group = t, roll_no = roll, name = name, batch_id = b.batch_id)
        s.save()
    

if __name__ == "__main__":
    blue.register_blueprints(app)
    manager.run()
# manager.add_command("createapp", CookieCutter())
manager.add_command('createapp', createapp())