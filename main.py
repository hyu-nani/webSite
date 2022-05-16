#pip install flask
#pip install flask-login
#pip install flask-sqlalchemy
#pip install waitress
developMode = True
from website import create_app

app = create_app()

if __name__ == '__main__':
    if developMode:
        app.run(debug=True, host="0.0.0.0")
    else:
        from waitress import serve
        serve(app, host="0.0.0.0")
