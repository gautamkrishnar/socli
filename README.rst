SoCLI |PyPI version| |Build Status| |Collaborizm| |Join the chat at https://gitter.im/socli-community/Lobby|
============================================================================================================

Stack Overflow command line written in python. Using SoCLI you can
search and browse Stack Overflow without leaving the terminal. Just use
the **socli** command:

.. figure:: https://cloud.githubusercontent.com/assets/8397274/24831468/86c290aa-1cb7-11e7-8161-2665d0c02e4b.gif
   :alt: SoCLI in action

   SoCLI in action

Installation
------------

Supported platforms
~~~~~~~~~~~~~~~~~~~

-  Linux
-  Windows
-  Mac

Requirements
~~~~~~~~~~~~

-  Python 3.5 or higher

For Linux
~~~~~~~~~

Install **python** and just use **pip** command to install **socli**:

.. code:: bash

   sudo apt-get install python python-pip
   pip install socli

For Windows
~~~~~~~~~~~

`Download and install Python <https://www.python.org/downloads/>`__.
Don’t forget to check the option “Add to path”.

Open a command prompt with administrative privileges and use **pip**
command to install **socli**:

.. code:: bash

   pip install socli

Use **easy_install** if your python path has a space in it. `Read more:
“Failed to create
process” <https://github.com/gautamkrishnar/socli/issues/6>`__:

::

   easy_install socli

For Mac (via homebrew)
~~~~~~~~~~~~~~~~~~~~~~

Install **python** and **socli**:

.. code:: bash

   brew install python
   easy_install pip
   pip install socli

Updating
--------

Use the command below to update your existing version of **socli** to
the newest version so that you won’t miss any features:

.. code:: bash

   pip install --upgrade socli

Usage
-----

Quick Search
~~~~~~~~~~~~

Use the **socli** command followed by the search query:

.. code:: bash

   socli for loop in python syntax

The above command will search for the query “*for loop in python
syntax*” and displays the first most voted question in Stack Overflow
with its most voted answer. Pretty quick, right?

Interactive Search
~~~~~~~~~~~~~~~~~~

You can search Stack Overflow interactively by using the command below:

.. code:: sh

   socli -iq html error 404

This will display a list of questions from Stack Overflow for the query
“*html error 404*” and it will allow you to choose any of the questions
you like interactively. When you choose a question, it will display the
complete description of the chosen question with its most voted answer.
You can also browse through the other answers to that question using the
up and down arrow keys as well as go back to the list of questions using
the left arrow key.

Manual Search
~~~~~~~~~~~~~

This will allow you to specify a requested question number for your
query. For example, consider the following command:

.. code:: sh

   socli -r 2 -q javascript prototype function

This command searches for “*javascript prototype function*” in Stack
Overflow and displays the second question that contains it.

Topic-Based Search
~~~~~~~~~~~~~~~~~~

Stack Overflow supports topic by using tags. **socli** allows you to
query Stack Overflow based on specific tags. Just specify the tag via
the following command:

.. code:: sh

   socli -t javascript -q window.open

You can also specify multiple tags, Just separate them with a comma:

.. code:: sh

   socli -t javascript,node.js -q window.open

See the complete list of tags `here <http://stackoverflow.com/tags>`__.

User Profile Browsing
~~~~~~~~~~~~~~~~~~~~~

Just use the command below to set your `user
ID <http://meta.stackexchange.com/a/111130>`__ in socli. When you
execute the command next time, it will automaticially fetch the data.

.. code:: sh

   socli -u

if your are an extensive user of StackOverflow, **socli** allows you to
set your own API key to overcome the `StackOverflow API
Limitations <http://stackapps.com/a/3057/41332>`__. Just use the command
below:

.. code:: sh

   socli --api

You can get an API Key
`here <http://stackapps.com/apps/oauth/register>`__ by registering as a
new app. Please don’t use SoCLI as app name.

Posting a New Question
~~~~~~~~~~~~~~~~~~~~~~

If you can’t find an answer for your question in Stack Overflow,
**socli** allows you to create a new question via the web browser. Just
type the command below and **socli** will open the new question page of
Stack Overflow in the web browser for you:

.. code:: sh

   socli -n

Syntax:
-------

**socli** has the following syntax

::

   Usage: socli [ Arguments] < Search Query >

Arguments (optional)
~~~~~~~~~~~~~~~~~~~~

+-----------------+-----------------+-----------------+-----------------+
| Short           | Long            | Description     | Example         |
+=================+=================+=================+=================+
| -q              | –query          | Used to specify | **socli -q      |
|                 |                 | the query when  | query**         |
|                 |                 | arguments are   |                 |
|                 |                 | used. A query   |                 |
|                 |                 | value must be   |                 |
|                 |                 | passed to it.   |                 |
|                 |                 | If it is used   |                 |
|                 |                 | alone (socli -q |                 |
|                 |                 | query) then it  |                 |
|                 |                 | will display    |                 |
|                 |                 | the same result |                 |
|                 |                 | as **socli      |                 |
|                 |                 | query**.        |                 |
+-----------------+-----------------+-----------------+-----------------+
| -i              | –interactive    | Used to search  | **socli -i -q   |
|                 |                 | interactively.  | query**         |
|                 |                 | It doesn’t take |                 |
|                 |                 | any values. It  |                 |
|                 |                 | must be         |                 |
|                 |                 | followed by a   |                 |
|                 |                 | -q or –query    |                 |
|                 |                 | after it.       |                 |
+-----------------+-----------------+-----------------+-----------------+
| -r              | –res            | Used for manual | **socli -r 4 -q |
|                 |                 | search. It      | query**         |
|                 |                 | takes the       |                 |
|                 |                 | question number |                 |
|                 |                 | as the argument |                 |
|                 |                 | and it must be  |                 |
|                 |                 | followed by a   |                 |
|                 |                 | -q or –query    |                 |
|                 |                 | after it.       |                 |
+-----------------+-----------------+-----------------+-----------------+
| -t              | –tag            | Specifies the   | **socli -t js   |
|                 |                 | tag to search   | -q query**      |
|                 |                 | for the query   |                 |
|                 |                 | on Stack        |                 |
|                 |                 | Overflow. It    |                 |
|                 |                 | must be         |                 |
|                 |                 | followed by a   |                 |
|                 |                 | -q or –query    |                 |
|                 |                 | after it.       |                 |
+-----------------+-----------------+-----------------+-----------------+
| -n              | –new            | Opens the web   | **socli –new**  |
|                 |                 | browser to      |                 |
|                 |                 | create a new    |                 |
|                 |                 | question on     |                 |
|                 |                 | Stack Overflow. |                 |
+-----------------+-----------------+-----------------+-----------------+
| -u              | –user           | Displays the    | **socli -u      |
|                 |                 | user profile    | 22656**         |
|                 |                 | informations.   |                 |
|                 |                 | If no argument  |                 |
|                 |                 | is given, it    |                 |
|                 |                 | will display    |                 |
|                 |                 | your profile.   |                 |
+-----------------+-----------------+-----------------+-----------------+
| -a              | –api            | Sets a custom   | **socli –api**  |
|                 |                 | API key.        |                 |
+-----------------+-----------------+-----------------+-----------------+
| -d              | –del            | Deletes the     | **socli -d**    |
|                 |                 | configuration   |                 |
|                 |                 | file generated  |                 |
|                 |                 | by socli -u     |                 |
|                 |                 | manually.       |                 |
+-----------------+-----------------+-----------------+-----------------+
| -s              | –sosearch       | SoCLI uses      | **socli -s -q   |
|                 |                 | Google search   | for loop        |
|                 |                 | by default to   | python**        |
|                 |                 | search for      |                 |
|                 |                 | questions. To   |                 |
|                 |                 | override this   |                 |
|                 |                 | and use         |                 |
|                 |                 | stackoverflow’s |                 |
|                 |                 | default search  |                 |
|                 |                 | instead.        |                 |
+-----------------+-----------------+-----------------+-----------------+
| -h              | –help           | Displays the    | **socli –help** |
|                 |                 | help text.      |                 |
+-----------------+-----------------+-----------------+-----------------+

Query
~~~~~

This term refers to what you’re searching for in Stack Overflow.

Features
--------

These are the amazing features of SoCLI: \* Manual Search \*
Interactively browse Stack Overflow using the interactive mode \*
Coloured interface \* Question stats view \* Tag support \* Can open the
page in a browser \* Can view user profiles \* Can create a new question
via the web browser

To Do
-----

Command line interface for: - [ ] Stack Overflow authentication - [ ]
Posting to Stack Overflow - [ ] Upvote answer - [ ] Comment on an answer
- [ ] Browsing stackoverflow home page

Please check out the list of
`issues <https://github.com/gautamkrishnar/socli/issues>`__.

Testing
-------

Automated tests are setup by using
`pytest <https://docs.pytest.org/en/latest/contents.html>`__, the tests
can be run locally by invoking a ``python setup.py test``.

All tests are in the ``/tests/`` subdirectory of this repository.

TravisCI is supposed to run the test-suite on build.

Contributing
------------

If you are willing to contribute to SoCLI project, you are awesome! Just
follow the steps below:

1. Fork it!
2. Make a local clone:

.. code:: sh

   git clone https://github.com/{YOUR_USERNAME}/socli.git

3. Switch to the directory: ``cd socli``
4. Create your new branch: ``git checkout -b feature name``
5. Make necessary changes to the source code
6. Add changes to git index by using ``git add --all .``
7. Commit your changes: ``git commit -am 'Added new feature'``
8. Push to the branch: ``git push``
9. Submit a `new pull
   request <https://github.com/gautamkrishnar/socli/pull/new>`__ :smile:

Maintainers
-----------

Please reach out to any of the following people if you have any queries:

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Gautam krishna R💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Hedy Li💻

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Contributors ✨
--------------

Thanks goes to these wonderful people (`emoji
key <https://allcontributors.org/docs/en/emoji-key>`__):

.. raw:: html

   <!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->

.. raw:: html

   <!-- prettier-ignore-start -->

.. raw:: html

   <!-- markdownlint-disable -->

.. raw:: html

   <table>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

aaxu💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

kilbee💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Sam Dean📖

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

mwwynne💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Carlos J. Puga Medina🐛

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Jon Ericson💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Ankit Kr. Singh💻

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Harsha Alva💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Pia Mancini📖

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Aditya Tandon🐛

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Akshatha Nayak💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Liam Hawkins💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Arount💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Cédric Picard🐛

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Amartya Chaudhuri💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Elliott Beach💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Prashant Chahal💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Insiyah Hajoori💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

C💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Liam Byrne💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Tran Chi Khang💻

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Alix Poulsen📖

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

albalitz💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Aniruddha Bhattacharjee💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Daniel St.Jacques💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Donnell Muse💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

JM Lopez💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

JOBIN PHILIP ABRAHAM📖

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Jakub Kukul💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Pigeon📖

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Rajdeep Biswas💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Sachin Kukreja💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Simon Reap💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Srisaila💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

agarwalnishtha💻

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

.. raw:: html

   <td align="center">

Frederick Kozlowski💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

Esha Lath💻

.. raw:: html

   </td>

.. raw:: html

   <td align="center">

thumpri💻

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

.. raw:: html

   <!-- markdownlint-enable -->

.. raw:: html

   <!-- prettier-ignore-end -->

.. raw:: html

   <!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the
`all-contributors <https://github.com/all-contributors/all-contributors>`__
specification. Contributions of any kind welcome!

Bugs
~~~~

If you are experiencing any bugs, don’t forget to open a `new
issue <https://github.com/gautamkrishnar/socli/issues/new>`__.

Error Solving
~~~~~~~~~~~~~

If you encounter "AttributeError: ‘module’ object has no attribute ‘SSL
ST INIT’

::

   sudo pip uninstall pyopenssl
   sudo pip install pyopenssl or sudo easy_install pyopenssl

Thanks
~~~~~~

-  Thanks to all the existing users of SoCLI.
-  Thanks to all upvoters and followers on reddit.
-  `impress that girl in the Starbucks by browsing SO with your CLI app
   XD
   XD <https://www.reddit.com/r/programmingcirclejerk/comments/4pwil4/impress_that_girl_in_the_starbucks_by_browsing_so/>`__
   by `insane0hflex <https://www.reddit.com/user/insane0hflex>`__.
   Thanks for the post :wink:
-  Special thanks to people who wrote about SoCLI on their blogs and
   websites:

   -  `wykop.pl <http://www.wykop.pl/wpis/18286681/python-stackoverflow-interfejs-bo-sciaga-musi-byc-/>`__
   -  `memect.com <http://forum.memect.com/blog/thread/py-2016-06-26/>`__
   -  `pseudoscripter <https://pseudoscripter.wordpress.com/2016/06/28/socli-stack-overflow-command-line-client/>`__
   -  `b.hatena.ne.jp <http://b.hatena.ne.jp/entry/s/github.com/gautamkrishnar/socli>`__
   -  `jericson.github.io <http://jericson.github.io/2016/08/25/long_tail_docs.html>`__
   -  `The really big list of really interesting Open Source
      projects <https://medium.com/@likid.geimfari/the-list-of-interesting-open-source-projects-2daaa2153f7c#.6qm1v3ioa>`__
   -  `Ostechnix <http://www.ostechnix.com/search-browse-stack-overflow-website-commandline/>`__
   -  `lamiradadelreplicante.com <lamiradadelreplicante.com/2017/04/17/socli-navegando-por-stack-overflow-sin-salir-de-la-terminal>`__
   -  `dou.ua <https://dou.ua/lenta/digests/python-digest-13/>`__

-  Tweets:

   -  [@cyb3rops](https://twitter.com/cyb3rops/status/747380776350650368)
   -  [@pythontrending](https://twitter.com/pythontrending/status/745635512803819521)

-  Thanks to my favourite IDE JetBrains PyCharm :heart: :smile:

Sponsors
~~~~~~~~

Sponsor SoCLI on
`Collaborizm <https://www.collaborizm.com/project/S1cbUui6>`__ or on
`Open Collective <https://opencollective.com/socli>`__:

-  Thanks `Steven Reubenstone <https://www.collaborizm.com/profile/1>`__
   for contributing $5 for the issue
   `#22 <https://github.com/gautamkrishnar/socli/issues/22>`__

Liked it?
~~~~~~~~~

Hope you liked this project, don’t forget to give it a star :star:

.. |PyPI version| image:: https://badge.fury.io/py/socli.svg
   :target: https://badge.fury.io/py/socli
.. |Build Status| image:: https://travis-ci.org/gautamkrishnar/socli.svg?branch=master
   :target: https://travis-ci.org/gautamkrishnar/socli
.. |Collaborizm| image:: https://img.shields.io/badge/Collaborizm-Join%20Project-brightgreen.svg
   :target: https://www.collaborizm.com/project/S1cbUui6
.. |Join the chat at https://gitter.im/socli-community/Lobby| image:: https://badges.gitter.im/socli-community/Lobby.svg
   :target: https://gitter.im/socli-community/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
