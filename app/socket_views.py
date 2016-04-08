from internalapi.api import GlobalApi
from app import app, db, socketio


@socketio.on('refresh', namespace='/test')
def test_message(message):
    iapi = GlobalApi()
    callbacks_list = iapi.get_all('callbacks')
    print callbacks_list
    emit('ticket list', callbacks_list)

@socketio.on('connect', namespace='/test')
def test_connect():
    iapi = GlobalApi()
    callbacks_list = iapi.get_all('callbacks')
    print callbacks_list
    emit('ticket list', callbacks_list)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    pass
