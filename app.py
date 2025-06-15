from flask import Flask
from backend.routes import bp as main_routes
from backend.code_to_pseudo import code_to_pseudo_api
from backend.pseudo_to_code import pseudo_to_code_api
from backend.existing_creations import existing_creations_api
from backend.generate_pseudo import generate_pseudo_api

app = Flask(__name__)
app.secret_key = '9c3dba8f7e014eb39d3846a5df24e6fc'
app.config["DEBUG"] = True

app.register_blueprint(main_routes)
app.register_blueprint(code_to_pseudo_api)
app.register_blueprint(pseudo_to_code_api)
app.register_blueprint(existing_creations_api)
app.register_blueprint(generate_pseudo_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
