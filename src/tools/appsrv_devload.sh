#!/bin/bash

APP_DIR=`pwd`/../../src

export PYTHONPATH=$APP_DIR:$PYTHONPATH

appcfg.py upload_data --config_file=article_exim.py --filename=articles.csv --kind=Article --url=http://localhost:8080/remote-admin $APP_DIR

rm -Rf bulkloader*