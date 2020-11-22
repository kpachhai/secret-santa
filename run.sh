#!/usr/bin/env bash

virtualenv -p `which python3` .venv
source .venv/bin/activate
pip install --upgrade pip

case `uname` in
Linux )
    pip install -r requirements.txt
    ;;
Darwin )
    pip install --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" -r requirements.txt
    ;;
*)
    exit 1
    ;;
esac

python main.py