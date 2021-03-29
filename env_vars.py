
MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_DBNAME = "acme"
MONGO_URI = "mongodb://{host}:{port}/{db_name}".format(
    host=MONGO_HOST,
    port=MONGO_PORT,
    db_name=MONGO_DBNAME
)

ALLOWED_EXTENSIONS = ['json']
UPLOAD_FOLDER = 'uploads'
