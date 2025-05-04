
from flask import Flask, render_template
import logging
from data import Displayable
import random
from globals import GlobalContext
from logic import LoadAppConfiguration, LoadModuleData

GLOBALS = GlobalContext()
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

LoadAppConfiguration(app, GLOBALS)
LoadModuleData(app, GLOBALS)

@app.route('/')
def hello():
    choices = [
        {
            'text' : 'Cards - German Questions',
            'destination': '/german'
        },
        {
            'text' : 'Cards - Croatian Questions',
            'destination': '/croatian'
        },
    ]
    return render_template('home_page.html.jinja', choices=choices)

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
else:
    app