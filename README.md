# SoCLI [![PyPI version](https://badge.fury.io/py/socli.svg)](https://badge.fury.io/py/socli) [![Build Status](https://travis-ci.org/gautamkrishnar/socli.svg?branch=master)](https://travis-ci.org/gautamkrishnar/socli) 
Stack overflow command line written in python. Using SoCLI you can search and browse stack overflow without leaving the terminal. Just use the **socli** command:

![SoCLI in action](https://cloud.githubusercontent.com/assets/8397274/16355211/ae134c66-3acd-11e6-807f-adb8f3bbcf44.gif)

### Installation

##### Supported platforms
* Linux
* Windows
* Mac

##### Requirements
* python 2+

##### For Linux
Install **python** and just use **pip** command to install **socli**:
```bash
sudo apt-get install python python-pip
sudo pip install socli
```
##### For Windows
###### Method 1 (Using Installer)
Download and install the latest release of [SoCLI-Setup.exe](https://github.com/gautamkrishnar/socli/releases/latest/) for windows. It is a self contained package with all the required dependencies.
Add SoCLI directory to windows path. See [this page](http://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/) for more info. Add `C:\Program Files (x86)\SoCLI` to the path. This method doesn't support the command line updating of SoCLI, you must manually uninstall the program and reinstall the new versions.

###### Method 2 (Using PIP)
[Download and install python](https://www.python.org/downloads/). Dont forget to check the option "Add to path".

Open a command prompt with administrative privileges and use **pip** command to install **socli**:
```bash
pip install socli
```
Use **easy_install** if your python path have a space in it [Read more:"Failed to create process"](https://github.com/gautamkrishnar/socli/issues/6):
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
Use the command below to update your existing version of **socli** to the newest version, so that you won't miss any features:
```bash
sudo pip install --upgrade socli
```

### Usage
##### Quick search
Just use **socli** command followed by the search query:
```bash
socli for loop in python syntax

```

The above command will search for the query "*for loop in python syntax*" and displays the first most voted question in stack overflow with its most voted answer. Pretty quick, right?

##### Interactive search
You can search the stack overflow interactively by using the command below:
```sh
socli -iq html error 404
```

This will display a list of questions from stack overflow for the query "*html error 404*" and it will allow you to choose any of the question you like interactively. When you chose a question, it will display the complete description of the chosed question with its most voted answer. Now you can browse through all the answers of that questions on stack overflow interactively.

##### Manual search
This will allow you to choose a question number for example:
```sh
socli -r 2 -q javascript porotype function
```
Will search for "*javascript porotype function*" in stack overflow and displays the second question that contains it.

##### Topic based search
Stack overflow supports topic by using tags. **socli** allows you to query stack overflow based on specific tags.  Just specify the tag via the following command:
```sh
socli -t javascript -q window.open
```
You can also specify multiple tags, Just seporate them with a comma:
```sh
socli -t javascript,node.js -q window.open
```
See the complete list of tags [here](http://stackoverflow.com/tags).


##### New question
If you can't find an answer for your question in stack overflow, **socli** allows you to creata a new question via the web browswer. Just type the command below and **socli** will open the new question page of stack overflow in the web browser for you:
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
| -q | --query | Used to specify the query when arguments are used. A query value must be passed to it. If it is used alone (socli -q query) then it will display the same result as "socli query". | socli -i -q query |
| -i | --interactive |  Used to search interactively. It doesnt take any values. It must be followed by a -q or --query after it. | socli -i -q query |
| -r | --res | Used for manual search. It takes the question number as the argument and it must be followed by a  -q or --query after it. | socli -r 4 -q query |
| -t | --tag | Specifies the tag to search for the query on stack overflow. It must be followed by a  -q or --query after it. | socli -t js -q query |
| -n | --new | Opens the web browser to create a new question on stack overflow. | socli --new |
| -h | --help | Displays the help text. | socli --help |

###### Query
It refers to query to search in stack overflow.

### Features
These are the amazing features of **socli**:
* Manual Search
* Interactively browse stack overflow using the interactive mode
* Coloured interface
* Question stats view
* Tag support
* Can open the page in a browser
* Can create a new question via the web browser

### To Do
Command line interface for:
- [ ] Stack overflow authentication
- [ ] Posting to stack overflow
- [ ] Upvote answer
- [ ] Comment on an answer

### Contributing
If you are willing to contribute to SoCLI project, You are awesome! Just follow the steps below:

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
* [@Killbee](https://github.com/kilbee) for making SoCLI colorful 
* [Sam Dean](https://github.com/deanWombourne) for adding Macintosh SoCLI installation instructions
* [Plinio89s](https://github.com/Plinio89s) for adding the check for color support
* [nagracks](https://github.com/nagracks) for improving readability of the
* [mwwynne](https://github.com/mwwynne) for adding links to the SoCLI
* [Carlos J. Puga Medina](https://github.com/cpu82) for finding the bug [#11](https://github.com/gautamkrishnar/socli/issues/14) on SoCLI python2 version and for making [SoCLI freshports port](https://www.freshports.org/misc/py-socli/)
* [Jon Ericson](https://github.com/jericson) (*Community Manager, Stack Overflow*) for the PR [#18](https://github.com/gautamkrishnar/socli/pull/18) and letting me know about the Stack overflow attribution policy. Thanks for the [blog post](http://jericson.github.io/2016/08/25/long_tail_docs.html)
* [Ankit Kr. Singh](https://github.com/kumarankit0411) for fixing some typos PR [#21](https://github.com/gautamkrishnar/socli/pull/21) [#23](https://github.com/gautamkrishnar/socli/pull/23).
* [Harsha Alva](https://github.com/aharshac) for fixing windows encoding problem PR [#24](https://github.com/gautamkrishnar/socli/pull/21).

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
* Tweets:
 	* [@cyb3rops](https://twitter.com/cyb3rops/status/747380776350650368)
 	* [@pythontrending](https://twitter.com/pythontrending/status/745635512803819521)
* Thanks to my favourite IDE JetBrains PyCharm :heart: :smile:

<img src="https://cloud.githubusercontent.com/assets/8397274/16355101/edb3b98a-3aca-11e6-8db5-5f54cd4b9969.png" width=80px>

### Liked it?
Hope you liked this project, don't forget to give it a star :star:
