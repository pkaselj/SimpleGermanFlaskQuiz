from dataclasses import dataclass
from glob import glob
import os
from typing import Any, Tuple
from flask import Flask

from data import ParseFile
from error import DictionaryAppError
from globals import GlobalContext

@dataclass
class CfgDescriptor:
    key : str
    required : bool
    default_value : Any = None

def _LoadCfg(app : Flask, g_ctx : GlobalContext, cfg_list : Tuple[CfgDescriptor]):
    for cfg in cfg_list:
        # First validate if GlobalContext has a matching field
        if not hasattr(g_ctx, cfg.key):
            if cfg.required:
                app.logger.error('Could not find REQUIRED config key %s in global context. terminating...', cfg.key)
                exit(-1)
            else:
                app.logger.warning('Could not find non-required config key %s in global context. skipping...', cfg.key)
                continue

        # Check if config found
        if cfg.key in app.config:
            setattr(g_ctx, cfg.key, app.config[cfg.key])
            app.logger.info('Found config value for key %s. Value = %s', cfg.key, getattr(g_ctx, cfg.key))
        else:
            if cfg.required:
                app.logger.error('Could not find REQUIRED config key %s in app configuration. terminating...', cfg.key)
                exit(-1)
            else:
                app.logger.warning('Could not find non-required config key %s in app configuration. Using default value %s.', cfg.key, repr(cfg.default_value))



def LoadAppConfiguration(app : Flask, g_ctx : GlobalContext):
    app.config.from_prefixed_env()
    _LoadCfg(app, g_ctx, [
        CfgDescriptor(key='QUIZ_DATA_DIR', required=True),
        CfgDescriptor(key='NR_OF_ITEMS_TO_SELECT', required=False, default_value=10)
    ])

def LoadModuleData(app : Flask, g_ctx : GlobalContext):
    app.logger.info('Started loading intial app module data')

    root = app.config["QUIZ_DATA_DIR"]
    files = glob('*.csv', root_dir=root, recursive=True)
    app.logger.info('Found %d data files', len(files))

    files = [os.path.join(root, x) for x in files]

    for file in files:
        app.logger.info('Loading data from %s', file)
        try:
            items = ParseFile(file, warn_logger=lambda msg : app.logger.warning(msg))
            app.logger.info('Parsed %d items from %s', len(items), file)
            g_ctx.ITEM_STORE = g_ctx.ITEM_STORE + items
        except DictionaryAppError as ex:
            app.logger.warning('Error while parsing file "%s": "%s"', file, ex)
    app.logger.info('Finished loading intial app module data')