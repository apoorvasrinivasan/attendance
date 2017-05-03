def register_blueprints(app):
    # Prevents circular imports
    from students.views import students
    app.register_blueprint(students, url_prefix='/api')
