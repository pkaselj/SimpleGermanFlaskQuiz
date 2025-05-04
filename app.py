import os
from glob import glob
from typing import Tuple
from flask import Flask, render_template
from data import Displayable, ParseFile
from error import DictionaryAppError
import random

GLOBAL_ITEM_STORE : Tuple[Displayable] = ()
GLOBAL_NR_OF_ITEMS_TO_SELECT = 10
GLOBAL_QUIZ_DATA_DIR = None

def LoadAppConfiguration(app : Flask):
    pass # TODO

def LoadModuleData(app : Flask):
    global GLOBAL_ITEM_STORE
    app.logger.info('Started loading intial app module data')

    if "QUIZ_DATA_DIR" not in app.config:
        app.logger.error('Could not find QUIZ_DATA_DIR configuration key!')
        exit(-1)

    root = app.config["QUIZ_DATA_DIR"]
    files = glob('*.csv', root_dir=root, recursive=True)
    app.logger.info('Found %d data files', len(files))

    files = [os.path.join(root, x) for x in files]

    for file in files:
        app.logger.info('Loading data from %s', file)
        try:
            items = ParseFile(file, warn_logger=lambda msg : app.logger.warning(msg))
            app.logger.info('Parsed %d items from %s', len(items), file)
            GLOBAL_ITEM_STORE = GLOBAL_ITEM_STORE + items
        except DictionaryAppError as ex:
            app.logger.warning('Error while parsing file "%s": "%s"', file, ex)
    app.logger.info('Finished loading intial app module data')

app = Flask(__name__)
app.config.from_prefixed_env()

LoadModuleData(app)

@app.route('/')
def hello():
    # app.logger.info(f'QUIZ_DATA_DIR = %s', app.config["QUIZ_DATA_DIR"])
    return 'Hello World!'

@app.route('/german')
def german():
    global GLOBAL_NR_OF_ITEMS_TO_SELECT
    global GLOBAL_ITEM_STORE

    def create_display_model(item : Displayable) -> dict:
        return {
            'question' : item.GetGerman(),
            'answer' : item.GetSolution()
        }

    data = random.sample(GLOBAL_ITEM_STORE, GLOBAL_NR_OF_ITEMS_TO_SELECT)
    display_data = [create_display_model(item) for item in data ]
    return render_template('quiz_page.html.jinja', quiz_data=display_data)

if __name__ == '__main__':
    app.run(debug=True) 