"""
This file is the main file of the API, here we will define the endpoints and the logic of the API
"""
import re
import sqlite3

from flask import Flask, request, json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from logs.logger import logger

app = Flask(__name__)
app.config['RATELIMIT_HEADERS_ENABLED'] = True  # Habilita los encabezados de rate limit en las respuestas
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "50 per hour"],
    storage_uri="memory://",
)


def get_db_connection() -> sqlite3.Connection:
    """
    This function will return a connection to the database
    :return: sqlite3.Connection
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
@limiter.limit('1 per minute')
def index() -> str:
    """
    This function is the index of the API, it will return a simple message
    :return: str
    """
    return "Hello world!"


@app.route('/news', methods=['GET'])
def news():
    """
    This endpoint will return the news of the database
    :return:
    """
    conn = get_db_connection()
    if request.method == 'GET':
        cursor = conn.execute('select ID, Title, Url, Image_url, Summary, Category, Date '
                              'FROM NEWS ').fetchall()
        objects_list = {"NEWS": []}

        for row in cursor:
            d = {"ID": row[0], "Title": row[1], "Url": row[2], "Image_url": row[3], "Summary": row[4],
                 "Category": row[5], "Date": row[6]}
            objects_list["NEWS"].append(d)

        response = app.response_class(
            response=json.dumps(objects_list),
            mimetype='application/json'
        )
        conn.close()
        logger.info(request.host + " " + request.path + " " + request.method + " " + str(response.status_code))
        return response


@app.route('/save_new', methods=['POST'])
@limiter.exempt
def save_new():
    """
    This endpoint will save a new in the database
    :return:
    """
    conn = get_db_connection()
    if request.method == 'POST':  # Si el método es POST se añade la noticia a la base de datos
        new = request.get_json()
        try:
            # Expresion regular para eliminar los espacios al princio y al final de cada dato
            new['Title'] = re.sub(r"^\s+|\s+$", "", new['Title'])
            new['Category'] = re.sub(r"^\s+|\s+$", "", new['Category'])
            new['Summary'] = re.sub(r"^\s+|\s+$", "", new['Summary'])
            new['Date'] = re.sub(r"^\s+|\s+$", "", new['Date'])

            conn.execute('INSERT OR IGNORE INTO NEWS '
                         '(ID, Title, Url, Image_url, Summary, Category, Date) '
                         'VALUES (?,?,?,?,?,?,?)',
                         (new['ID'], new['Title'], new['Url'], new['Image_url'], new['Summary'],
                          new['Category'], new['Date']))
            conn.commit()
        except sqlite3.IntegrityError:
            logger.error("Error inserting new")
        conn.close()
        return new


if __name__ == '__main__':
    app.run(debug=True, port=5000)
