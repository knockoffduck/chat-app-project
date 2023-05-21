from website import create_app, db
from website.models import User, Chat

app = create_app()

if __name__ == '__main__':
    app.run(debug= False)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Chat': Chat}