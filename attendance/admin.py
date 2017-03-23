from flask_admin import Admin, AdminIndexView, expose
# from flask import request, g
# import auth

def get_admin(app):
    return Admin(
        app, 
        name='attendanceApp', 
        template_mode='bootstrap3',
        # index_view=HomeView(url='/admin')
    )
 

# class HomeView(AdminIndexView):
#     @expose('/',methods=('GET', 'POST'))
#     def index(self):
#         response = (""  ,200)
#         form = auth.forms.LoginForm(request.form)
#         if request.method =='POST':
#             if form.validate():
#                 response = auth.serialiser.login(form.data['email'], form.data['password'])
#                 if response[1] == 200:
#                     token = response[0].get('token')
                    

#         user = getattr(g, 'current_user',None)
#         return self.render('admin/index.html', token=user, form = form, response = response[0])
