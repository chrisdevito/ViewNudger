============
Installation
============

Get ViewNudger for Maya
========================

Using the MEL setup script
---------------------------
- Download the package from the github repo http://github.com/chrisdevito/ViewNudger.git and click Download Zip.
- After extraction, drag and drop the setup.mel (found in the ViewNudger directory) into any open maya window.
- This will install it into your maya/scripts directory.

Using Pip
----------
::

    $ pip install ViewNudger

Git
-----
::

    $ git clone https://github.com/chrisdevito/ViewNudger
    $ cd ViewNudger
    $ python setup.py install

Manual
-------
- Download the package from the github repo http://github.com/chrisdevito/ViewNudger.git and click Download Zip.

- Copy the ViewNudger folder into your maya/scripts path.

How to Run
===========
Drop this code as a button or run from the maya python script editor.

.. code-block:: python
    :name: viewNudgerUI.py

from ViewNudger import ui

if __name__ == '__main__':
    global win

    try:
        win.close()
    except:
        pass

    win = ui.UI()
    win.create()
