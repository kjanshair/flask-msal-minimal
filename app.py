from flask import Flask, render_template
from ms_identity_web.adapters import FlaskContextAdapter # STEP 1
from ms_identity_web.configuration import AADConfig # STEP 2
from ms_identity_web import IdentityWebPython # STEP 3
from werkzeug.middleware.proxy_fix import ProxyFix # STEP 4
import app_config # STEP 5
from flask_session import Session # STEP 5

#########################################################################################
# STEP 5: ENABLE FLASK CONFIGURATION TO READ FROM app_config.py AND SERVER-SIDE SESSIONS
#########################################################################################
app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

#########################################################################################
# STEP 1: USE THE ADAPTOR TO ENABLE enable IdentityWebPython TO WORK WITHIN THE FLASK
#########################################################################################
adapter = FlaskContextAdapter(app)

#########################################################################################
# STEP 2: PARSE AAD JSON CONFIG
#########################################################################################
aad_configuration = AADConfig.parse_json('aad.config.json')
AADConfig.sanity_check_configs(aad_configuration)

#########################################################################################
# STEP 3: INSTANTIATE THE MS IDENTITY FOR PYTHON
#########################################################################################
ms_identity_web = IdentityWebPython(aad_configuration, adapter)

#########################################################################################
# STEP 4: THIS SECTION IS REQUIRED IF THE APP IS RUNNING BEHIND A PROXY
#########################################################################################
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()