from server import app

##takes the app from server and runs it
if __name__ == '__main__':
    app.run(host= '0.0.0.0',use_reloader=False,debug=True)
