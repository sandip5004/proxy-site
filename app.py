from flask import Flask, render_template, make_response, send_from_directory, Blueprint, jsonify
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), 'templates'),
        static_url_path=os.path.join(os.getcwd(), 'static'),
    )
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    app.secret_key = 'd5c2ba7f-4926-4bc1-883a-9d74c8c246ea '
    app.config['SESSION_TYPE'] = 'redis'
    return app


app = create_app()

site_static_blueprint = Blueprint('static_files', __name__, static_url_path='/static', static_folder='static/')
app.register_blueprint(site_static_blueprint)

@app.route("/")
def home():
    return render_template("/lms-admin/dashboard.html",**{'module' : 'Dashboard'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)