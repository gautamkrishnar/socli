# SoCLI [![PyPI](https://img.shields.io/pypi/v/socli?color=brightgreen) ![PyPI Downloads](https://img.shields.io/pypi/dm/socli)](https://pypi.org/project/socli/) [![Build Status](https://travis-ci.com/gautamkrishnar/socli.svg?branch=master)](https://travis-ci.com/gautamkrishnar/socli) [![Collaborizm](https://img.shields.io/badge/Collaborizm-Join%20Project-brightgreen.svg)](https://www.collaborizm.com/project/S1cbUui6) [![Gitter Chat](https://badges.gitter.im/socli-community/Lobby.svg)](https://gitter.im/socli-community/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Stack Overflow command line written in python. Using SoCLI you can search and browse Stack Overflow without leaving the terminal. Just use the **socli** command:


![SoCLI in action](https://cloud.githubusercontent.com/assets/8397274/24831468/86c290aa-1cb7-11e7-8161-2665d0c02e4b.gif)

### Installation

##### Supported platforms
* Linux
* Windows
* Mac

##### Requirements
* Python 3.5 or higher

##### For Linux
Install **python** and just use **pip** command to install **socli**:
```bash
sudo apt-get install python3 python3-pip
pip install socli
```
##### For Windows
[Download and install Python](https://www.python.org/downloads/). Don't forget to check the option "Add to path".

Open a command prompt with administrative privileges and use **pip** command to install **socli**:
```bash
pip install socli
```
Use **easy_install** if your python path has a space in it. [Read more: "Failed to create process"](https://github.com/gautamkrishnar/socli/issues/6):
```
easy_install socli
```

##### For Mac/Linux (via [homebrew](https://brew.sh/))
Install **socli**:
```bash
brew tap gautamkrishnar/socli
brew install socli
```

##### Enabling the shell autocompletion
If you installed socli vis pyPi you may need to enable the shell autocompletion. Add the following to your `.bashrc` file to enable it:
```bash
socli --register
```

### Updating
Use the command below to update your existing version of **socli** to the newest version so that you won't miss any features:
```bash
pip install --upgrade socli
```

If you installed via homebrew:
```bash
brew upgrade socli
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
You can also specify multiple tags, Just separate them with a comma:
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

##### Opening a url directly
If you have the url of the Stack Overflow post then you can pass it using `--open-url` or `-o`.
For example
``` socli --open-url https://stackoverflow.com/questions/20639180/explanation-of-how-nested-list-comprehension-works```

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
| -s | --sosearch | SoCLI uses Google search by default to search for questions. To override this and use stackoverflow's default search instead. | **socli -s -q for loop python** |
| -h | --help | Displays the help text. | **socli --help** |
| -o | --open-url | Displays the given url in socli if possible if not opens in browser. | **socli -o https://stackoverflow.com/questions/20639180/explanation-of-how-nested-list-comprehension-works** |
| -j | --json-output | Gives output to stdout as json | **socli -jq for loop python** |
| -g | --register | Registers socli's shell autocompletion | socli -g |
| -v | --version | Displays the version of socli. | **socli -v** |

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
* Can open a Stack Overflow page on the terminal directly from a url

### To Do
Command line interface for:
- [ ] Stack Overflow authentication
- [ ] Posting to Stack Overflow
- [ ] Upvote answer
- [ ] Comment on an answer
- [ ] Browsing stackoverflow home page

Please check out the list of [issues](https://github.com/gautamkrishnar/socli/issues).

### Testing
Automated tests are setup by using
[pytest](https://docs.pytest.org/en/latest/contents.html), the tests can be run
locally by invoking a `python setup.py test`.

All tests are in the `socli/tests/` subdirectory of this repository.

TravisCI is supposed to run the test-suite on build.

### 💥 How to Contribute ?
If you are willing to contribute to SoCLI project, you are awesome! 
Just follow the steps given in [CONTRIBUTING.md](https://github.com/gautamkrishnar/socli/blob/master/CONTRIBUTING.md) 😃

## Maintainers

Please reach out to any of the following people if you have any queries:
<table>
  <tr>
    <td align="center"><a href="https://github.com/gautamkrishnar"><img src="https://avatars2.githubusercontent.com/u/8397274?v=4" width="100px;" alt=""/><br /><sub><b>Gautam krishna R</b></sub></a><br /><a href="https://github.com/gautamkrishnar/SoCLI/commits?author=gautamkrishnar" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/hedythedev"><img src="https://avatars0.githubusercontent.com/u/50042066?v=4" width="100px;" alt=""/><br /><sub><b>Hedy Li</b></sub></a><br /><a href="https://github.com/gautamkrishnar/SoCLI/commits?author=hedythedev" title="Code">💻</a></td>
  </tr>
</table>

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/aaxu"><img src="https://avatars2.githubusercontent.com/u/19481525?v=4?s=100" width="100px;" alt=""/><br /><sub><b>aaxu</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=aaxu" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/kilbee"><img src="https://avatars1.githubusercontent.com/u/2181891?v=4?s=100" width="100px;" alt=""/><br /><sub><b>kilbee</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=kilbee" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/deanWombourne"><img src="https://avatars1.githubusercontent.com/u/7887119?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sam Dean</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=deanWombourne" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/mwwynne"><img src="https://avatars1.githubusercontent.com/u/3174043?v=4?s=100" width="100px;" alt=""/><br /><sub><b>mwwynne</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=mwwynne" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/cpu82"><img src="https://avatars2.githubusercontent.com/u/4080230?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos J. Puga Medina</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/issues?q=author%3Acpu82" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://jlericson.com/"><img src="https://avatars1.githubusercontent.com/u/1520759?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jon Ericson</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=jericson" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/kumarankit0411"><img src="https://avatars2.githubusercontent.com/u/19763730?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ankit Kr. Singh</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=kumarankit0411" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://alvaharsha.com/"><img src="https://avatars2.githubusercontent.com/u/11926689?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Harsha Alva</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=aharshac" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/piamancini"><img src="https://avatars2.githubusercontent.com/u/3671070?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pia Mancini</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=piamancini" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/adityatandon007"><img src="https://avatars2.githubusercontent.com/u/25108385?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aditya Tandon</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/issues?q=author%3Aadityatandon007" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/Aksh77"><img src="https://avatars0.githubusercontent.com/u/12583292?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Akshatha Nayak</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=Aksh77" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/liamhawkins"><img src="https://avatars3.githubusercontent.com/u/22647996?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Liam Hawkins</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=liamhawkins" title="Code">💻</a></td>
    <td align="center"><a href="http://arount.info/"><img src="https://avatars3.githubusercontent.com/u/4593141?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Arount</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=arount" title="Code">💻</a></td>
    <td align="center"><a href="https://breakpoint.purrfect.fr/"><img src="https://avatars3.githubusercontent.com/u/4958985?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Cédric Picard</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/issues?q=author%3Acym13" title="Bug reports">🐛</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/amartyaamp"><img src="https://avatars1.githubusercontent.com/u/7647235?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Amartya Chaudhuri</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=amartyaamp" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/elliott-beach"><img src="https://avatars1.githubusercontent.com/u/13651458?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Elliott Beach</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=elliott-beach" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/prashantchahal26"><img src="https://avatars3.githubusercontent.com/u/14841072?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Prashant Chahal</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=prashantchahal26" title="Code">💻</a></td>
    <td align="center"><a href="https://insiyaa.github.io/"><img src="https://avatars2.githubusercontent.com/u/29259374?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Insiyah Hajoori</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=Insiyaa" title="Code">💻</a></td>
    <td align="center"><a href="https://thevirtuoso1973.github.io/"><img src="https://avatars2.githubusercontent.com/u/46009390?v=4?s=100" width="100px;" alt=""/><br /><sub><b>C</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=thevirtuoso1973" title="Code">💻</a></td>
    <td align="center"><a href="https://liambyrne.nz/"><img src="https://avatars2.githubusercontent.com/u/18452094?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Liam Byrne</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=liambyrnenz" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/tranchikhang"><img src="https://avatars3.githubusercontent.com/u/16659747?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tran Chi Khang</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=tranchikhang" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/AlexPoulsen"><img src="https://avatars1.githubusercontent.com/u/9259671?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alix Poulsen</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=AlexPoulsen" title="Documentation">📖</a></td>
    <td align="center"><a href="https://gitlab.com/albalitz"><img src="https://avatars1.githubusercontent.com/u/9308749?v=4?s=100" width="100px;" alt=""/><br /><sub><b>albalitz</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=albalitz" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/anirudnits"><img src="https://avatars3.githubusercontent.com/u/25305301?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Aniruddha Bhattacharjee</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=anirudnits" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/dstjacques"><img src="https://avatars0.githubusercontent.com/u/735244?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Daniel St.Jacques</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=dstjacques" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/donnell794"><img src="https://avatars2.githubusercontent.com/u/11854190?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Donnell Muse</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=donnell794" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/jm66"><img src="https://avatars2.githubusercontent.com/u/2047620?v=4?s=100" width="100px;" alt=""/><br /><sub><b>JM Lopez</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=jm66" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/jophab"><img src="https://avatars3.githubusercontent.com/u/13940974?v=4?s=100" width="100px;" alt=""/><br /><sub><b>JOBIN PHILIP ABRAHAM</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=jophab" title="Documentation">📖</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/jkukul"><img src="https://avatars2.githubusercontent.com/u/7057316?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jakub Kukul</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=jkukul" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/LuckyPigeon"><img src="https://avatars0.githubusercontent.com/u/32315294?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pigeon</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=LuckyPigeon" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/therajdeepbiswas"><img src="https://avatars2.githubusercontent.com/u/32306614?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Rajdeep Biswas</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=therajdeepbiswas" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/sk364"><img src="https://avatars1.githubusercontent.com/u/15685616?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sachin Kukreja</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=sk364" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/simon3270"><img src="https://avatars3.githubusercontent.com/u/1138498?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Simon Reap</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=simon3270" title="Code">💻</a></td>
    <td align="center"><a href="https://stackoverflow.com/users/8709791/srig?tab=profile"><img src="https://avatars1.githubusercontent.com/u/32685230?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Srisaila</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=srigalibe" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/agarwalnishtha"><img src="https://avatars0.githubusercontent.com/u/35678934?v=4?s=100" width="100px;" alt=""/><br /><sub><b>agarwalnishtha</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=agarwalnishtha" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/fredkozlowski"><img src="https://avatars0.githubusercontent.com/u/15177661?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Frederick Kozlowski</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=fredkozlowski" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/elath03"><img src="https://avatars2.githubusercontent.com/u/20517890?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Esha Lath</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=elath03" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/thumpri"><img src="https://avatars2.githubusercontent.com/u/30461824?v=4?s=100" width="100px;" alt=""/><br /><sub><b>thumpri</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=thumpri" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/adamjyz"><img src="https://avatars1.githubusercontent.com/u/55098065?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adam Zhang</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=adamjyz" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/prathampowar2001"><img src="https://avatars0.githubusercontent.com/u/30765406?v=4?s=100" width="100px;" alt=""/><br /><sub><b>prathampowar2001</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=prathampowar2001" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/suvhotta"><img src="https://avatars0.githubusercontent.com/u/16841978?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Subhankar Hotta</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=suvhotta" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/ankushduacodes"><img src="https://avatars3.githubusercontent.com/u/61025943?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ankushduacodes</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=ankushduacodes" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/artorias111"><img src="https://avatars2.githubusercontent.com/u/48955393?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Shriram Bhat</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=artorias111" title="Code">💻</a></td>
    <td align="center"><a href="http://vjspranav.stag-os.org"><img src="https://avatars0.githubusercontent.com/u/17949836?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Vjs Pranav</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=vjspranav" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/Saif807380"><img src="https://avatars2.githubusercontent.com/u/50794619?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Saif Kazi</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=Saif807380" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/pstreff"><img src="https://avatars3.githubusercontent.com/u/32448748?v=4?s=100" width="100px;" alt=""/><br /><sub><b>pstreff</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=pstreff" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/anshik1998"><img src="https://avatars0.githubusercontent.com/u/54910667?v=4?s=100" width="100px;" alt=""/><br /><sub><b>anshik1998</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=anshik1998" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/abstanton"><img src="https://avatars1.githubusercontent.com/u/23246639?v=4?s=100" width="100px;" alt=""/><br /><sub><b>abstanton</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=abstanton" title="Code">💻</a></td>
    <td align="center"><a href="http://ssyd.pw"><img src="https://avatars3.githubusercontent.com/u/28098330?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sabu Siyad</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=ssiyad" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/pspiagicw"><img src="https://avatars0.githubusercontent.com/u/30765406?v=4?s=100" width="100px;" alt=""/><br /><sub><b>pspiagicw</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=pspiagicw" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/hertzrp"><img src="https://avatars1.githubusercontent.com/u/37788702?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ryan Hertz</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=hertzrp" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/tharunc"><img src="https://avatars3.githubusercontent.com/u/68283386?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tharunc</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=tharunc" title="Documentation">📖</a></td>
    <td align="center"><a href="https://akrish4.github.io/online-portfolio/"><img src="https://avatars0.githubusercontent.com/u/61831021?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ananthakrishnan Nair RS</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=akrish4" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/muthuannamalai12"><img src="https://avatars2.githubusercontent.com/u/64524822?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Muthu Annamalai.V</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=muthuannamalai12" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/chetak123"><img src="https://avatars1.githubusercontent.com/u/53306550?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ayushman</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=chetak123" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/tusharnankani"><img src="https://avatars1.githubusercontent.com/u/61280281?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tushar Nankani</b></sub></a><br /><a href="https://github.com/gautamkrishnar/socli/commits?author=tusharnankani" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

### Bugs
If you are experiencing any bugs, don’t forget to open a [new issue](https://github.com/gautamkrishnar/socli/issues/new).

### Error Solving
If you encounter "AttributeError: 'module' object has no attribute 'SSL ST INIT'
```
sudo pip uninstall pyopenssl
sudo pip install pyopenssl or sudo easy_install pyopenssl
```

### Thanks
* Thanks to all the existing users of SoCLI.
* Thanks to all upvoters and followers on reddit.
* [impress that girl in the Starbucks by browsing SO with your CLI app XD XD](https://www.reddit.com/r/programmingcirclejerk/comments/4pwil4/impress_that_girl_in_the_starbucks_by_browsing_so/) by [insane0hflex](https://www.reddit.com/user/insane0hflex). Thanks for the post 😉
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
* Thanks to my favourite IDE JetBrains PyCharm ❤️ 😄

<img src="https://cloud.githubusercontent.com/assets/8397274/16355101/edb3b98a-3aca-11e6-8db5-5f54cd4b9969.png" width=80px>

### Sponsors
Sponsor SoCLI on [Collaborizm](https://www.collaborizm.com/project/S1cbUui6) or on [Open Collective](https://opencollective.com/socli):

* Thanks [Steven Reubenstone](https://www.collaborizm.com/profile/1) for contributing $5 for the issue [#22](https://github.com/gautamkrishnar/socli/issues/22)

### Liked it?
Hope you liked this project, don't forget to give it a star ⭐
