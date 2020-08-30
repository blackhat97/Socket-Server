# Socket-Server

대윤계기산업(주) TCP 소켓서버

## Requirements
To get started locally, follow these instructions:

1. sudo apt install python3-pip
1. pip3 install virtualenv virtualenvwrapper
1. virtualenv -p python3 venv
1. source venv/bin/activate

## 의존성 설치
1. pip3 install -r requirements.txt

## 설치
1. python setup.py install

## 설정

DB 패스워드 설정파일

```
[client]
host = localhost
port = 3306
user = myusername
password = mypassword

pymysql.connect(read_default_file='~/.my.cnf',)

```
또는

```
# dbsettings.py  
connection_properties = {
    'host': 'localhost',
    'port': 3306,
    'user': 'myusername',
    'password': 'mypassword'
    }

from dbsettings import connection_properties
conn = pymysql.connect(**connection_properties)
```


Link: [소켓설정](https://meetup.toast.com/posts/54)
Link: [서버부하테스트](https://artillery.io/docs/getting-started/)

## Changelog


