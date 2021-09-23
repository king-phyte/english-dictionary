# english-dictionary
A school project to build an English dictionary.


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python version: 3.8 | 3.9](https://img.shields.io/badge/Python%20version-3.8%20%7C%203.9-green)


**This app is in beta phase. It has known issues.**


## Table of contents

- [Project description](#english-dictionary)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Key Features](#key-features)
- [Bugs?](#bugs)
- [Contributing](#contributing)


## Installation

**Note: The app requires python3.8 or higher.**

1. Clone the repository 
    - ```
      $ git clone https://github.com/king-phyte/english-dictionary.git
      ```
  
    - Optionally, [download the zip](https://github.com/king-phyte/english-dictionary/archive/main.zip) and extract it

2. Move into the directory
   ```
   $ cd english-dictionary
   ```

3. Create a virtual environment  and activate it
    ```
    $ virtualenv -p python3 .
    $ source ./bin/activate
    ```
   - Notice the dot (.) in the first command

4. Install the requirements
    ```
    $ pip install -r requirements.txt
   ```
   - Some users might need to replace ``pip`` with ``./bin/pip``.

## Usage

**Note:** To use the app, make sure you have a __virtual environment__ active.
Activate the virtual environment with ``. ./bin/activate`` or ``source ./bin/activate`` or find how it is done for your target machine.
If you do not have it installed, find out from the [installation section](#installation) above.

- Click the plus button near the search bar to add a word. __(Note: currently, the fields are limited).__
- If the word you searched for is not in the dictionary, click the search button or press enter for "fetch from internet" dialog. __(Note: the parser might sometimes fail)__
- To edit a word, click the edit button. __(Note: currently, the fields are limited, and you might lose a few fields)__
- To delete a word, use the delete button
  
### Running the app
- In your terminal, move into the root directory (english-dictionary) and type ``python main.py`` or ``python3 main.py``.
  
 
- **Enjoy! 😁**


## Key Features
- Real-time filtering as you search for words
- Add words
- Delete words
- Edit words
- Fetch words from the internet if not found in the program.

## Bugs?
If you find a bug, feel free to open an issue or [message me directly on Telegram](https://t.me/king-phyte). 
There are known bugs that are being worked on, and new bugs found will be fixed ASAP.


## Contributing
All pull requests are welcome. Please make sure you format your code with black before the pull request.

### Big ups to Suyash458/WiktionaryParser