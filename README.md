# english-dictionary
An extensible (offline) English Dictionary.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python version: 3.8 | 3.9](https://img.shields.io/badge/Python%20version-3.8%20%7C%203.9-green)


## Table of contents

- [Project description](#english-dictionary)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the app](#running-the-app)
  - [How to use the app](#how-to-use-the-app)
- [Key Features](#key-features)
- [Bugs?](#bugs)
- [Contributing](#contributing)


## Installation

**Note: The app requires python3.8 or higher.**

1. There are a number of ways to get the source code. You can:
   - [Download the latest release](https://github.com/king-phyte/english-dictionary/releases/latest) (english-dictionary-x.y.z.tar.gz) for linux releases and extract it.

   - Clone the repository
     ```
        $ git clone https://github.com/king-phyte/english-dictionary.git
      ```
   
   - [Download the zip](https://github.com/king-phyte/english-dictionary/archive/main.zip) and extract it


2. Create an isolated virtual environment inside the directory and activate it
   ```
   $ python3 -m venv .
   $ source ./bin/activate
   ```
   Notice the dot (.) in first the command

3. If you used the latest release. Install the application with
   ```
   $ python setup.py install
   ```
   
4. Otherwise, install the requirements:
   ```
   $ pip install -r requirements.txt
   ```
   Some users might need to replace ``pip`` with ``./bin/pip``.

## Usage

**Note:** To use the app, it is advised that you have a __virtual environment__ active.
If you do not have a virtual environment, find out from the [installation section](#installation) above.


### Running the app
- If you used setup.py to install the app, you can start it with:
   ```
   $ eng-dict
   ```
- If you cloned or used the zip. You should use:
   ```
   $ python english-dictionary/run.py
   ```
   Or optionally,
   ```
    $ python main.py
   ```

### How to use the app
- Click the plus button near the search bar to add a word. __(Note: currently, the fields are limited).__
- If the word you searched for is not in the dictionary, click the search button or press enter for "fetch from internet" dialog.
- To edit a word, click the edit button. __(Note: currently, the fields are limited, and you might lose a few fields)__
- To delete a word, use the delete button
  

- **Enjoy! 😁**

## Extending the app
The backend was rewritten with extensibility in mind. To use another data source, simply write a class to conform to the Base API
and replace all occurrences of the current data source API (called FreeDictionaryAPI) to yours. Done. Easy!

Your class should simply parse your data source into the JSON format as shown below:
```json
[
   {
        "name": "str",
        "etymology": "str",
        "pronunciations": [
            {
                "text": "str",
                "audio": "str"
            }
        ],
        "meanings": [
            {
                "part_of_speech": "str",
                "definitions": [
                    {
                        "definition": "str",
                        "example": "str",
                        "related_words": [
                            {
                                "relationship_type": "str",
                                "words": "list[str]"
                            }
                        ]
                    }
                ]
            }
        ]
 }
]
```
Keys with their values as lists scan contain more than one item.

__Feel free to share any ideas you may have or improvements you make.__

## Key Features
- Extensible backend
- Real-time filtering as you search for words
- Add words
- Delete words
- Edit words
- Fetch words from the internet if not found in the program.

## Bugs?
If you find a bug, feel free to open an issue or [message me directly on Telegram](https://t.me/king-phyte). 
There are known bugs that are being worked on, and new bugs found will be fixed ASAP.


## Contributing
All contributions are welcome. Open a pull request. Please format your code with black before the pull request.
