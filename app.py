from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxx'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('location', namespace='/broadcast')
def location(message):
    emit('location', {'username': message['username'], 'coords': message['coords'], 'acc': message['acc']}, broadcast=True)
    print str({'username': message['username'], 'coords': message['coords'], 'acc': message['acc']})

@socketio.on('message', namespace='/broadcast')
def location(message):
    emit('message', {'username': message['username'], 'message': message['message']}, broadcast=True)
    print str({'username': message['username'], 'message': message['message']})

@socketio.on('server_connect', namespace='/broadcast')
def server_connect(message):
    session['username'] = message['username']
    emit('server_connect', {'username': message['username']}, broadcast=True)
    print 'User '+message['username']+' logged in.'

@socketio.on('disconnect', namespace='/broadcast')
def disconnect():
    emit('disconnect', {'username': session['username']}, broadcast=True)
    print 'User '+session['username']+' disconnected.'

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5005)
