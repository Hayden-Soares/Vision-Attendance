from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import dotenv_values
from supabase import create_client

app = Flask(__name__)

config_file = dotenv_values('.env')


app.config["SQLALCHEMY_DATABASE_URI"] = config_file['SUPABASE_URI']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)#We need only one app instance, so direct use is fine

supabase = create_client(config_file["SUPABASE_URL"], config_file["SUPABASE_KEY"])