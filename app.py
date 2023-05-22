from website import create_app, db
from website.models import User, Chat
from config import TestingConfig, ProductionConfig
import sys

app = create_app(ProductionConfig)

if __name__ == "__main__":
    if "--testing" in sys.argv:
        app = create_app(TestingConfig)
        print("------------------------------------------")
        print("Website running in Testing Environment")
        print("------------------------------------------")

    else:
        app = create_app()
        print("------------------------------------------")
        print("Website running in Development Environment")
        print("------------------------------------------")
    app.run(debug=False)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Chat": Chat}
