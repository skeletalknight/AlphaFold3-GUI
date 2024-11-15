#!/usr/bin/env python

import os
import sys

def main():
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    streamlit_command = [
        'streamlit', 'run', app_path,
        '--server.fileWatcherType=none'
    ] + sys.argv[1:]
    os.execvp('streamlit', streamlit_command)

if __name__ == '__main__':
    main()
