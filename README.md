# TOC Project 2022: Shopping List Planner Line Bot

A Line bot to help you make a shopping list.

## Why is it necessary?

We have a lot of daily necessities. When we're shopping these necessities, the variety can be overwhelming and leave you feeling scattered. This often ends with you coming home either empty-handed or with the wrong items. 
Having a shopping list keeps you focused and productive when shopping. Without one, it’s easy to forget essential items or overspend on things you forgot you already had.

## User Guide

1. Enter start to start the bot.
2. Enter the budget.
3. Make your shopping list : adding or deleting item(s).
4. Add item(s) by inputing item name, price, and unit.
5. Then finally the bot will check if your budget is suffice. If not you will have to edit your shopping list again!
6. Enter restart to restart making the list.

## FSM
![fsm](https://user-images.githubusercontent.com/95698966/209289784-3089bc39-cf41-43d8-a2ed-3b8e1e6d8c97.png)

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)




#### Run Locally using Ngrok
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
