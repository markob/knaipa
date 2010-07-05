#!/bin/bash

APP_DIR=`pwd`/../../src

export PYTHONPATH=$APP_DIR:$PYTHONPATH

appcfg.py download_data --config_file=article_exim.py --filename=articles.csv --kind=Article $APP_DIR

rm -Rf bulkloader*