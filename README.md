# SoCLI [![PyPI version](https://badge.fury.io/py/socli.svg)](https://badge.fury.io/py/socli) [![Build Status](https://travis-ci.org/gautamkrishnar/socli.svg?branch=master)](https://travis-ci.org/gautamkrishnar/socli) [![Collaborizm](https://img.shields.io/badge/Collaborizm-Join%20Project-brightgreen.svg)](https://www.collaborizm.com/project/S1cbUui6) 
Stack Overflow command line written in python. Using SoCLI you can search and browse Stack Overflow without leaving the terminal. Just use the **socli** command:

![SoCLI in action](https://cloud.githubusercontent.com/assets/8397274/24831468/86c290aa-1cb7-11e7-8161-2665d0c02e4b.gif)

### Installation

##### Supported platforms
* Linux
* Windows
* Mac

##### Requirements
* Python 2.0 or higher

##### For Linux
Install **python** and just use **pip** command to install **socli**:
```bash
sudo apt-get install python python-pip
sudo pip install socli
```
##### For Windows
[Download and install Python](https://www.python.org/downloads/). Don't forget to check the option "Add to path".

Open a command prompt with administrative privileges and use **pip** command to install **socli**:
```bash
pip install socli
```
Use **easy_install** if your python path have a space in it. [Read more: "Failed to create process"](https://github.com/gautamkrishnar/socli/issues/6):
```
easy_install socli
```

##### For Mac (via homebrew)
Install **python** and **socli**:
```bash
brew install python
easy_install pip
pip install socli
```
### Updating
Use the command below to update your existing version of **socli** to the newest version so that you won't miss any features:
```bash
sudo pip install --upgrade socli
```

### Usage
##### Quick Search
Use the **socli** command followed by the search query:
```bash
socli for loop in python syntax

```

The above command will search for the query "*for loop in python syntax*" and displays the first most voted question in Stack Overflow with its most voted answer. Pretty quick, right?

##### Interactive Search
You can search Stack Overflow interactively by using the command below:
```sh
socli -iq html error 404
```

This will display a list of questions from Stack Overflow for the query "*html error 404*" and it will allow you to choose any of the questions you like interactively. When you choose a question, it will display the complete description of the chosen question with its most voted answer. You can also browse through the other answers to that question using the up and down arrow keys as well as go back to the list of questions using the left arrow key.

##### Manual Search
This will allow you to specify a requested question number for your query. For example, consider the following command:
```sh
socli -r 2 -q javascript prototype function
```
This command searches for "*javascript prototype function*" in Stack Overflow and displays the second question that contains it.

##### Topic-Based Search
Stack Overflow supports topic by using tags. **socli** allows you to query Stack Overflow based on specific tags.  Just specify the tag via the following command:
```sh
socli -t javascript -q window.open
```
You can also specify multiple tags, Just seporate them with a comma:
```sh
socli -t javascript,node.js -q window.open
```
See the complete list of tags [here](http://stackoverflow.com/tags).

##### User Profile Browsing
Just use the command below to set your [user ID]( http://meta.stackexchange.com/a/111130) in socli. When you execute the command next time, it will automaticially fetch the data.
```sh
socli -u
```
if your are an extensive user of StackOverflow, **socli** allows you to set your own API key to overcome the [StackOverflow API Limitations](http://stackapps.com/a/3057/41332). Just use the command below:
```sh
socli --api
```
You can get an API Key [here](http://stackapps.com/apps/oauth/register) by registering as a new app. Please don't use SoCLI as app name.

##### Posting a New Question
If you can't find an answer for your question in Stack Overflow, **socli** allows you to create a new question via the web browser. Just type the command below and **socli** will open the new question page of Stack Overflow in the web browser for you:
```sh
socli -n
```

### Syntax:
**socli** has the following syntax
```
Usage: socli [ Arguments] < Search Query >
```

###### Arguments (optional)
| Short | Long | Description | Example |
|--------|--------|--------|--------|
| -q | --query | Used to specify the query when arguments are used. A query value must be passed to it. If it is used alone (socli -q query) then it will display the same result as **socli query**. | **socli -q query** |
| -i | --interactive |  Used to search interactively. It doesn't take any values. It must be followed by a -q or --query after it. | **socli -i -q query** |
| -r | --res | Used for manual search. It takes the question number as the argument and it must be followed by a  -q or --query after it. | **socli -r 4 -q query** |
| -t | --tag | Specifies the tag to search for the query on Stack Overflow. It must be followed by a  -q or --query after it. | **socli -t js -q query** |
| -n | --new | Opens the web browser to create a new question on Stack Overflow. | **socli --new** |
| -u | --user | Displays the user profile informations. If no argument is given, it will display your profile. | **socli -u 22656** |
| -a | --api | Sets a custom API key. | **socli --api** |
| -d | --del | Deletes the configuration file generated by socli -u manually. | **socli -d** |
| -h | --help | Displays the help text. | **socli --help** |

###### Query
This term refers to what you're searching for in Stack Overflow.

### Features
These are the amazing features of SoCLI:
* Manual Search
* Interactively browse Stack Overflow using the interactive mode
* Coloured interface
* Question stats view
* Tag support
* Can open the page in a browser
* Can view user profiles
* Can create a new question via the web browser

### To Do
Command line interface for:
- [ ] Stack Overflow authentication
- [ ] Posting to Stack Overflow
- [ ] Upvote answer
- [ ] Comment on an answer
- [ ] Browsing stackoverflow home page

Please check out the list of [issues](https://github.com/gautamkrishnar/socli/issues).

### Contributing
If you are willing to contribute to SoCLI project, you are awesome! Just follow the steps below:

1. Fork it!
2. Make a local clone: 
  ```sh
  git clone https://github.com/{YOUR_USERNAME}/socli.git
  ```

3. Switch to the directory: `cd socli` 
4. Create your new branch: `git checkout -b feature name`
5. Make necessary changes to this source code
6. Add changes to git index by using `git add --all .`
7. Commit your changes: `git commit -am 'Added new feature'`
8. Push to the branch: `git push`
9. Submit a [new pull request](https://github.com/gautamkrishnar/socli/pull/new) :smile:

### Contributors
Special thanks to these superheroes:
* [Elliott Beach](https://github.com/e-beach) for improving color support by adding colorama [#29](https://github.com/gautamkrishnar/socli/pull/29), For making SoCLI more interactive [#35](https://github.com/gautamkrishnar/socli/pull/35). [36](https://github.com/gautamkrishnar/socli/pull/36) [#40](https://github.com/gautamkrishnar/socli/pull/40) You rocks...
* [Killbee](https://github.com/kilbee) for making SoCLI colorful [#3](https://github.com/gautamkrishnar/socli/pull/3)
* [Sam Dean](https://github.com/deanWombourne) for adding Macintosh SoCLI installation instructions [#1](https://github.com/gautamkrishnar/socli/pull/1)
* [Plinio89s](https://github.com/Plinio89s) for adding the check for color support [#8](https://github.com/gautamkrishnar/socli/pull/8)
* [nagracks](https://github.com/nagracks) for improving readability of the SoCLI code [#11](https://github.com/gautamkrishnar/socli/pull/11)
* [mwwynne](https://github.com/mwwynne) for adding links to the SoCLI [#13](https://github.com/gautamkrishnar/socli/pull/13)
* [Carlos J. Puga Medina](https://github.com/cpu82) for finding the bug [#11](https://github.com/gautamkrishnar/socli/issues/14) on SoCLI python2 version and for making [SoCLI freshports port](https://www.freshports.org/misc/py-socli/)
* [Jon Ericson](https://github.com/jericson) (*Community Manager, Stack Overflow*) for the PR [#18](https://github.com/gautamkrishnar/socli/pull/18) and letting me know about the Stack Overflow attribution policy. Thanks for the [blog post](http://jericson.github.io/2016/08/25/long_tail_docs.html)
* [Ankit Kr. Singh](https://github.com/kumarankit0411) for fixing some typos PR [#21](https://github.com/gautamkrishnar/socli/pull/21) [#23](https://github.com/gautamkrishnar/socli/pull/23)
* [Harsha Alva](https://github.com/aharshac) for fixing windows encoding problem PR [#24](https://github.com/gautamkrishnar/socli/pull/21)
* [Pia Mancini](https://github.com/piamancini) for adding SoCLI to OpenCollective [#27](https://github.com/gautamkrishnar/socli/pull/27)
* [Aditya Tandon](https://github.com/adityatandon007) for the issue [#30](https://github.com/gautamkrishnar/socli/issues/30)
* [Akshatha Nayak](https://github.com/Aksh77) for your first contribution to an open source project. PR [#31](https://github.com/gautamkrishnar/socli/issues/31)
* [Levi Sabah](https://github.com/levisabah) for PR [#43](https://github.com/gautamkrishnar/socli/pull/43)
* [liamhawkins](https://github.com/liamhawkins) for PR [#44](https://github.com/gautamkrishnar/socli/pull/44) and [#45](https://github.com/gautamkrishnar/socli/pull/45)
* [Arount](https://github.com/arount) for fixing issue [#48](https://github.com/gautamkrishnar/socli/issues/48) via PR [#47](https://github.com/gautamkrishnar/socli/pull/47)
* [Cédric Picard](https://github.com/cym13) for the issue [#42](https://github.com/gautamkrishnar/socli/issues/42)

### Bugs
If you are experiencing any bugs, don’t forget to open a [new issue](https://github.com/gautamkrishnar/socli/issues/new).

### Thanks
* Thanks to all the existing users of SoCLI.
* Thanks to all upvoters and followers on reddit.
* [impress that girl in the Starbucks by browsing SO with your CLI app XD XD](https://www.reddit.com/r/programmingcirclejerk/comments/4pwil4/impress_that_girl_in_the_starbucks_by_browsing_so/) by [insane0hflex](https://www.reddit.com/user/insane0hflex). Thanks for the post :wink:
* Special thanks to people who wrote about SoCLI on their blogs and websites:
	* [wykop.pl](http://www.wykop.pl/wpis/18286681/python-stackoverflow-interfejs-bo-sciaga-musi-byc-/)
	* [memect.com](http://forum.memect.com/blog/thread/py-2016-06-26/)
	* [pseudoscripter](https://pseudoscripter.wordpress.com/2016/06/28/socli-stack-overflow-command-line-client/)
	* [b.hatena.ne.jp](http://b.hatena.ne.jp/entry/s/github.com/gautamkrishnar/socli)
	* [jericson.github.io](http://jericson.github.io/2016/08/25/long_tail_docs.html)
	* [The really big list of really interesting Open Source projects](https://medium.com/@likid.geimfari/the-list-of-interesting-open-source-projects-2daaa2153f7c#.6qm1v3ioa)
	* [Ostechnix](http://www.ostechnix.com/search-browse-stack-overflow-website-commandline/)
	* [lamiradadelreplicante.com](lamiradadelreplicante.com/2017/04/17/socli-navegando-por-stack-overflow-sin-salir-de-la-terminal)
	* [dou.ua](https://dou.ua/lenta/digests/python-digest-13/)
* Tweets:
 	* [@cyb3rops](https://twitter.com/cyb3rops/status/747380776350650368)
 	* [@pythontrending](https://twitter.com/pythontrending/status/745635512803819521)
* Thanks to my favourite IDE JetBrains PyCharm :heart: :smile:

<img src="https://cloud.githubusercontent.com/assets/8397274/16355101/edb3b98a-3aca-11e6-8db5-5f54cd4b9969.png" width=80px>

### Backers
Support us with a monthly donation and help us continue our activities. [[Become a backer](https://opencollective.com/socli#backer)]

<a href="https://opencollective.com/socli/backer/0/website" target="_blank"><img src="https://opencollective.com/socli/backer/0/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/1/website" target="_blank"><img src="https://opencollective.com/socli/backer/1/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/2/website" target="_blank"><img src="https://opencollective.com/socli/backer/2/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/3/website" target="_blank"><img src="https://opencollective.com/socli/backer/3/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/4/website" target="_blank"><img src="https://opencollective.com/socli/backer/4/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/5/website" target="_blank"><img src="https://opencollective.com/socli/backer/5/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/6/website" target="_blank"><img src="https://opencollective.com/socli/backer/6/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/7/website" target="_blank"><img src="https://opencollective.com/socli/backer/7/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/8/website" target="_blank"><img src="https://opencollective.com/socli/backer/8/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/9/website" target="_blank"><img src="https://opencollective.com/socli/backer/9/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/10/website" target="_blank"><img src="https://opencollective.com/socli/backer/10/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/11/website" target="_blank"><img src="https://opencollective.com/socli/backer/11/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/12/website" target="_blank"><img src="https://opencollective.com/socli/backer/12/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/13/website" target="_blank"><img src="https://opencollective.com/socli/backer/13/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/14/website" target="_blank"><img src="https://opencollective.com/socli/backer/14/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/15/website" target="_blank"><img src="https://opencollective.com/socli/backer/15/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/16/website" target="_blank"><img src="https://opencollective.com/socli/backer/16/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/17/website" target="_blank"><img src="https://opencollective.com/socli/backer/17/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/18/website" target="_blank"><img src="https://opencollective.com/socli/backer/18/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/19/website" target="_blank"><img src="https://opencollective.com/socli/backer/19/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/20/website" target="_blank"><img src="https://opencollective.com/socli/backer/20/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/21/website" target="_blank"><img src="https://opencollective.com/socli/backer/21/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/22/website" target="_blank"><img src="https://opencollective.com/socli/backer/22/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/23/website" target="_blank"><img src="https://opencollective.com/socli/backer/23/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/24/website" target="_blank"><img src="https://opencollective.com/socli/backer/24/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/25/website" target="_blank"><img src="https://opencollective.com/socli/backer/25/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/26/website" target="_blank"><img src="https://opencollective.com/socli/backer/26/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/27/website" target="_blank"><img src="https://opencollective.com/socli/backer/27/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/28/website" target="_blank"><img src="https://opencollective.com/socli/backer/28/avatar.svg"></a>
<a href="https://opencollective.com/socli/backer/29/website" target="_blank"><img src="https://opencollective.com/socli/backer/29/avatar.svg"></a>

### Sponsors
Become a sponsor and get your logo on our README on Github with a link to your site. [[Become a sponsor](https://opencollective.com/socli#sponsor)]

<a href="https://opencollective.com/socli/sponsor/0/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/1/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/2/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/3/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/4/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/5/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/6/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/7/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/8/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/9/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/9/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/10/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/10/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/11/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/11/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/12/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/12/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/13/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/13/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/14/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/14/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/15/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/15/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/16/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/16/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/17/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/17/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/18/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/18/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/19/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/19/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/20/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/20/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/21/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/21/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/22/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/22/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/23/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/23/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/24/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/24/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/25/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/25/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/26/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/26/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/27/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/27/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/28/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/28/avatar.svg"></a>
<a href="https://opencollective.com/socli/sponsor/29/website" target="_blank"><img src="https://opencollective.com/socli/sponsor/29/avatar.svg"></a>

* Thanks [Steven Reubenstone](https://www.collaborizm.com/profile/1) for contributing $5 for the issue [#22](https://github.com/gautamkrishnar/socli/issues/22)

### Liked it?
Hope you liked this project, don't forget to give it a star :star:
