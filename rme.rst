SoCLI
=====

Stack overflow command line stack overflow client written in python.
Using SoCLI you can search and browse stack overflow without leaving the
terminal. Just use the **socli** command:

.. figure:: https://cloud.githubusercontent.com/assets/8397274/16255232/82d93dae-3865-11e6-9b0b-c4570adbda6e.gif
   :alt: socli in action

   socli in action

Installation
~~~~~~~~~~~~

Supported platforms
'''''''''''''''''''

-  Linux
-  Windows
-  Mac

Requirements
''''''''''''

-  python 3+ :

For Linux
'''''''''

Install **python3**:

::

    sudo apt-get install python3

Just use **pip** command to install **socli**:

.. code:: sh

    sudo pip3 install socli

For Windows
'''''''''''

`Download and install python 3`_. Dont forget to check the option “Add
to path”

Open a command prompt with administrative privileges and use **pip**
command to install **socli**:

::

    pip3 install socli

For Mac (via homebrew)
''''''''''''''''''''''

.. code:: sh

    brew install python3
    pip3 install socli

Usage
~~~~~

Quick search
''''''''''''

Just use **socli** command followed by the search query:

.. code:: sh

    socli for loop in python syntax

The above command will search for the query “*for loop in python
syntax*” and displays the first most voted question in stack overflow
with its most voted answer. Pretty quick, right?

Interactive search
''''''''''''''''''

You can search the stack overflow interactively by using the command
below:

.. code:: sh

    socli -iq html error 404

This will display a list of questions from stack overflow for the query
“*html error 404*” and it will allow you to choose any of the question
you like interactively. When you chose a question, it will display the
complete description of the chased question with its most voted answer.

Manual search
'''''''''''''

This will allow you to choose a question number for example:

.. code:: sh

    socli -r 2 -q javascript porotype function

Will search for “*javascript porotype function*” in stack overflow and
displays the second question that contains it.

Syntax:
~~~~~~~

**socli** has the following syntax

::

    Usage: socli [ Arguments] < Search Query >

Arguments (optional)
                    

+----------+----------+----------+----------+
| Short    | Long     | Descript | Example  |
|          |          | ion      |          |
+==========+==========+==========+==========+
| -q       | –query   | Used to  | socli -i |
|          |          | specify  | -q query |
|          |          | the      |          |
|          |          | query    |          |
|          |          | when     |          |
|          |          | argument |          |
|          |          | s        |          |
|          |          | are      |          |
|          |          | used. A  |          |
|          |          | query    |          |
|          |          | value    |          |
|          |          | must be  |          |
|          |          | passed   |          |
|          |          | to it.   |          |
|          |          | If it is |          |
|          |          | used     |          |
|          |          | alone    |          |
|          |          | (socli   |          |
|          |          | -q       |          |
|          |          | query)   |          |
|          |          | then it  |          |
|          |          | will     |          |
|          |          | display  |          |
|          |          | the same |          |
|          |          | result   |          |
|          |          | as       |          |
|          |          | “socli   |          |
|          |          | query”.  |          |
+----------+----------+----------+----------+
| -i       | –interac | Used to  | socli -i |
|          | tive     | search   | -q query |
|          |          | interact |          |
|          |          | ively.   |          |
|          |          | It       |          |
|          |          | doesnt   |          |
|          |          | take any |          |
|          |          | values.  |          |
|          |          | It must  |          |
|          |          | be       |          |
|          |          | followed |          |
|          |          | by a -q  |          |
|          |          | or       |          |
|          |          | –query   |          |
|          |          | after    |          |
|          |          | it.      |          |
+----------+----------+----------+----------+
| -r       | –res     | Used for | socli -r |
|          |          | manual   | 4 -q     |
|          |          | search.  | query    |
|          |          | It takes |          |
|          |          | the      |          |
|          |          | question |          |
|          |          | number   |          |
|          |          | as the   |          |
|          |          | argument |          |
|          |          | and it   |          |
|          |          | must be  |          |
|          |          | followed |          |
|          |          | by a -q  |          |
|          |          | or       |          |
|          |          | –query   |          |
|          |          | after    |          |
|          |          | it.      |          |
+----------+----------+----------+----------+
| -h       | –help    | Displays | socli    |
|          |          | the help | –help    |
|          |          | text.    |          |
+----------+----------+----------+----------+

Query
     

It refers to query to search in stack overflow.

Contributing
~~~~~~~~~~~~

If you are willing to contribute to SoCLI project, You are awesome! Just
follow the steps below:

1. Fork it!

.. _Download and install python 3: https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe

2. Make a local clone:
   ``sh   git clone https://github.com/{YOUR_USERNAME}/socli.git``

3. Switch to the directory: ``cd socli``
4. Create your new branch: ``git checkout -b feature name``
5. Make necessary changes to this source code
6. Add changes to git index by using ``git add --all .``
7. Commit your changes: ``git commit -am 'Added new feature'``
8. Push to the branch: ``git push``
9. Submit a `new pull request`_ 


Bugs
~~~~

If you are experiencing any bugs, don’t forget to open a `new issue`_.

Liked it?
~~~~~~~~~

Hope you liked this project, don’t forget to give it a `Star on GitHub`_

.. _new pull request: https://github.com/gautamkrishnar/socli/pull/new
.. _new issue: https://github.com/gautamkrishnar/socli/issues/new
.. _Star on GitHub: https://github.com/gautamkrishnar/socli/
