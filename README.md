# SoCLI [![PyPI version](https://badge.fury.io/py/socli.png)](https://badge.fury.io/py/socli) [![Build status](https://circleci.com/gh/gautamkrishnar/socli.svg?style=svg)](https://circleci.com/gh/gautamkrishnar/socli) 
Stack overflow command line stack overflow client written in python. Using SoCLI you can search and browse stack overflow without leaving the terminal. Just use the **socli** command:

![SoCLI in action](https://cloud.githubusercontent.com/assets/8397274/16355211/ae134c66-3acd-11e6-807f-adb8f3bbcf44.gif)

### Installation

##### Supported platforms
* Linux
* Windows
* Mac

##### Requirements
* python 3+ :

##### For Linux
Install **python3** and just use **pip** command to install **socli**:
```bash
sudo apt-get install python3 python3-pip
sudo pip3 install socli
```
##### For Windows
[Download and install python 3](https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe). Dont forget to check the option "Add to path".

Open a command prompt with administrative privileges and use **pip** command to install **socli**:
```bash
pip3 install socli
```
Use **easy_install** if your python path have a space in it [Read more:"Failed to create process"](https://github.com/gautamkrishnar/socli/issues/6):
```
easy_install socli
```

##### For Mac (via homebrew)
Install **python3** and **socli**:
```bash
brew install python3 python3-pip
pip3 install socli
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

##### New question
If you can't find an answer for your question in stack overflow, **socli** allows you to creata a new question via the web browswer. Just type the command below and **socli** will open the web browser for you to post the question:
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
* Can open the page in a browser
* Can create a new question via the web browser

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

### Bugs
If you are experiencing any bugs, don’t forget to open a [new issue](https://github.com/gautamkrishnar/socli/issues/new).

### Thanks
* Thanks to all the existing users of SoCLI.
* Special thanks to people who wrote about SoCLI on their blogs and websites:
	* [wykop.pl](http://www.wykop.pl/wpis/18286681/python-stackoverflow-interfejs-bo-sciaga-musi-byc-/)
* Thanks to my favourite IDE JetBrains PyCharm :heart: :smile:

<img src="https://cloud.githubusercontent.com/assets/8397274/16355101/edb3b98a-3aca-11e6-8db5-5f54cd4b9969.png" width=80px>

### Liked it?
Hope you liked this project, don't forget to give it a star :star:
