# pylookup

Display the pylint message id for a given message name.

Installation
------------

To install, first choose whether you'd like to install the Bash shell version `pylookup` or the Python 3 version `pylookup.py` then run the following:

    sudo install pylookup /usr/local/bin
    sudo install -m 0644 pylookup-completion /etc/bash_completion.d/pylookup

To install scripts locally (assuming `~/.local/bin` is on your PATH and `~/.bash_completion.d` is properly sourced):

    install pylookup ~/.local/bin
    sudo install -m 0664 pylookup-completion ~/.bash_completion.d/pylookup


Requirements
------------

`pylookup` is written in Bash shell script and has no other dependencies.

`pylookup.py` is a clone written in Python 3.

Usage
-----

To output the following: `# pylint: disable=W0702`

    pylookup bare-except

To output the following: `W0702`

    pylookup -b bare-except

License
-------

Copyright (c) 2015 Six <brbsix@gmail.com>

Licensed under the GPLv3 license.
