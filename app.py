# import necessary libraries
import os
from sqlalchemy.ext.automap import automap_base
from flask import (
    Flask,
    render_template,
    jsonify)
from flask_sqlalchemy import SQLAlchemy

### Initialise app
app = Flask(__name__)

#####################################
# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///HDI_db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create an engine
engine = db.get_engine()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Countries = Base.classes.countries
Cities = Base.classes.cities
########################################

#Landing page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/api/v1/countries')
def api_country():
    with db.session_scope() as session:
        country_table = session.query(Countries).all()
        result = [row.__dict__ for row in country_table]
    
        for item in result:
            item.pop('_sa_instance_state', None)
        
    return jsonify(result)

@app.route('/api/v1/cities')
def api_city():
    with db.session_scope() as session:
        city_table = session.query(Cities).all()
        result = [row.__dict__ for row in city_table]
    
        for item in result:
            item.pop('_sa_instance_state', None)
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
