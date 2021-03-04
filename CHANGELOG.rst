SoCLI Changelog
================

Release 6.3
---------------------------
* Minor fixes

Release 6.2
---------------------------
* Migrated to GitHub actions

Release 6.1
---------------------------
* Migrated to GitHub actions

Release 6.0
---------------------------
* Added accepted answer highlighting

Release 5.9
---------------------------
* Added `-j` or `--json-output` for providing json output
* Added manpage for socli
* Added option to return to original question after visiting duplicate one

Release 5.8
---------------------------
* Added sentry for error logging
* Fixed google search class change

Release 5.7
---------------------------
* Fixing issues with `-iq` argument

Release 5.6
---------------------------
* Added `-v` or `--version` argument for displaying the current version

Release 5.5
---------------------------
* Added toggle to view comments (for answers)
* Improved google search querying to get better results

Release 5.4
---------------------------
* fix for 404 not handled while opening url with -o argument

Release 5.3
---------------------------
* Made code pep8 compliant
* Fixed 404 page crashing issue

Release 5.2
---------------------------
* Fixed bug caused due to StackOverflow class changes #202

Release 5.1
---------------------------
* Using no-cache on pypi to get the latest version

Release 5.0
---------------------------
* Formula generation bug fixes

Release 4.9
---------------------------
* Formula generation bug fixes

Release 4.8
---------------------------
* Improved brew formula generation

Release 4.7
---------------------------
* Fixed duplicate question display in interactive mode #195
* Improved tests
* Typo fixes
* Always use chrome useragent to prevent inconsistencies in results

Release 4.6
---------------------------
* Brew formula final version added

Release 4.5
---------------------------
* Brew formula initial version release

Release 4.4
---------------------------
* Added ``-o`` or ``--open`` option to browse stack overflow pages directly from url #193
* Added classifiers in setup.py

Release 4.3
---------------------------
* Improved ``--user`` option: fixed displaying wrong output when user has 0 total questions
* Improved ``--user`` option: fixed KeyboardInterrupt error when using ``^C`` to abort set api key prompt
* Also added Python version support and license classifiers to setup.py for PyPI


Release 4.2
---------------------------

* Improved regex implementation to lower in search.py (get_questions_for_query_google) #186
* Improved fetching question stats logic #188


Release 4.1
---------------------------

* Fixed:  Question stats not working #179

Release 4.0
---------------------------

* Drop support for python <= 3.5
* Fixing some issues related to searching

Release 3.9
---------------------------

* Bug fixes

Release 3.8
---------------------------

* Bug fixes

Release 3.7
---------------------------

* Fixed functional issues

Release 3.6
---------------------------

* Implemented usage of Google search instead of stackoverflow's default search
* Added code to test captcha checks
* Many bugs fixed

Release 3.5
---------------------------

* Added code to prevent unwanted captcha checks
* Made SoCLI more interactive
* Minor bugfixes

Release 3.4
---------------------------

* Bugfix release

Release 3.3
---------------------------

* Minor bugfix

Release 3.2
---------------------------

* Added user profiles

Release 3.1
---------------------------

* Bugfix release

Release 3.0
---------------------------

* Fixed almost all windows encoding and color bugs

Release 2.9
---------------------------

* Many minor bug fixes

Release 2.8
---------------------------

* Fixed Windows encoding problem

Release 2.7
---------------------------

* Fixed some minor bugs

Release 2.6
---------------------------

* Fixed some minor typos
* Added windows binary release

Release 2.5
---------------------------

* Fixed some bugs due to latest windows cmd update
* Added sorting of question based on number of votes

Release 2.4
---------------------------

* Added StackOverflow attribution

Release 2.3
---------------------------

* Fixed minor bugs

Release 2.2
---------------------------

* Added tag based search

Release 2.1
---------------------------

* Fixed encoding bug

Release 2.0
---------------------------

* Fixed bugs on python 2

Release 1.9
---------------------------

* Added URL support to answers
* Added debugger module

Release 1.8
---------------------------

* Added support to python 2

Release 1.7
---------------------------

* Added new question feature
* Fixed windows color problem on windows 10

Release 1.6
---------------------------

* Intelligent colors

Release 1.5
---------------------------

* Added open in browser feature

Release 1.4
---------------------------

* Added interactive mode feature

Release 1.3
---------------------------

* Added colors

Release 1.2
---------------------------

* First stable release on PyPI

Release 1.1
---------------------------

* Pre Release

Release 1.0
---------------------------

* Beta version
