
from flask import Flask, render_template
from data import Displayable
import random
from globals import GlobalContext
from logic import LoadAppConfiguration, LoadModuleData

GLOBALS = GlobalContext()
app = Flask(__name__)

LoadAppConfiguration(app, GLOBALS)
LoadModuleData(app, GLOBALS)

@app.route('/')
def hello():
    # app.logger.info(f'QUIZ_DATA_DIR = %s', app.config["QUIZ_DATA_DIR"])
    return 'Hello World!'

@app.route('/german')
def german():
    global GLOBALS

    def create_display_model(item : Displayable) -> dict:
        return {
            'question' : item.GetGerman(),
            'answer' : item.GetSolution()
        }

    data = random.sample(GLOBALS.ITEM_STORE, GLOBALS.NR_OF_ITEMS_TO_SELECT)
    display_data = [create_display_model(item) for item in data ]
    return render_template('quiz_page.html.jinja', quiz_data=display_data)

@app.route('/croatian')
def croatian():
    global GLOBALS

    def create_display_model(item : Displayable) -> dict:
        return {
            'question' : item.GetCroatian(),
            'answer' : item.GetSolution()
        }

    data = random.sample(GLOBALS.ITEM_STORE, GLOBALS.NR_OF_ITEMS_TO_SELECT)
    display_data = [create_display_model(item) for item in data ]
    return render_template('quiz_page.html.jinja', quiz_data=display_data)

if __name__ == '__main__':
    app.run(debug=True) 