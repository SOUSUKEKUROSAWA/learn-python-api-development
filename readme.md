- Part1
  - https://youtu.be/ToXOb-lpipM
- Part2
  - https://youtu.be/1N0nhahVdqs
# Section 1: Intro
## Course Project
- source code
  - https://github.com/Sanjeev-Thiyagarajan/fastapi-course
## Course Intro
- FastAPIを採用した理由
  - API開発に特化したフレームワーク
  - 非常に高速な実行速度と開発速度
  - 自動ドキュメンテーション機能
# Section 2: Setup & installation
## VS Code install and setup
- pythonファイルを開くと自動でインタープリタが選択される
## Python virtual environment Basics
- https://chat.openai.com/share/4e11a886-4ee0-483b-acbf-d4f45df7ed28
## Virtual environment on bash
- bashを開く
- `python -m venv venv`
  - 仮想環境の作成
- Ctrl + Shift + p
- `select interpreter`
- `.\venv\Scripts\python.exe`
  - インタープリタの変更
- `source venv/Scripts/activate`
  - 仮想環境のアクティブ化
- `deactivate`
  - 仮想環境の非アクティブ化
# Section 3: FastAPI
- document
  - https://fastapi.tiangolo.com/ja/
## Install dependencies w/ pip
- `pip install fastapi[all]`
- `pip freeze`
  - インストールしたパッケージの一覧を表示
  - venv\Libにパッケージに関する情報が格納されている
## Starting Fast API
- `uvicorn <file name>:<application object name>`
  - APIの実行
    - localhost:8000をリッスンするサーバが立ち上がる
  - ex.)
    - `uvicorn main:app`
      - main.pyのappを実行
## Path operations
- pythonの辞書を返したとしてもFastAPIはそれをJSONに自動で変換する
- デコレータを使用してメソッドのエンドポイントを規定できる
- コードを書き換えてページをリロードしても変更が反映されない問題
  - 原因
    - `uvicorn main:app`コマンドはコードの変更を監視していないから
  - 解決策
    - `uvicorn main:app --reload`
## Path Operation Order(yes it matters)
- 同じパスがあった場合，上に書かれている方が読み取られて，それ以降のものは無視される
## HTTP Post Requests
- `Body(...)`
  - リクエストボディからデータを取得する
  - `...`
    - PythonのEllipsisオブジェクト
      - パラメータが必須であることを示す
      - ex.)
        - `def create_posts(payload: dict = Body(...)):`
        - このコードでは`create_posts`関数がリクエストを受け取るとき、リクエストボディから`payload`という名前の辞書型のデータを必須として要求する
        - リクエストボディが提供されない場合、FastAPIは自動的に`400 Bad Request`エラーを返す
      - `Body(...)`の代わりにデフォルト値を設定することも可能
        - ex.)
          - `Body(None)`
            - リクエストボディが提供されなかった場合でもエラーを返さず、`payload`の値は`None`になる
- `__pycache__`ディレクトリとは
  - Pythonがスクリプトを高速に実行するためのキャッシュが格納される
  - gitignoreに含めるべきもの
## Schema Validation with Pydantic
- Pydantic
  - リクエストボディのデータが特定の形式や条件を満たしていることを検証できる
    - データが正しい型であること、特定の範囲内の値であること、特定の形式（例えば、メールアドレスや日付）であることなど、様々な条件を指定できる
    - リクエストボディがPydanticモデルの条件を満たしていない場合、FastAPIは自動的に`400 Bad Request`エラーを返す
  - strで制限をかけると，1のような数字が送信されて生きても，自動で文字列に変換される
    - エラーはスローしない
- `Optional[int]`
  - Noneを許容するという意味
  - int型が入るが，NoneでもOKというカラムを定義する
## storing posts in Array
- 簡単のためにまずはメモリにデータを保存していく
## creating posts
## Postman Collections & saving requests
## Retrieve One Post
## Path order Matters
## Changing response Status Codes
## Deleting Posts
## Updating Posts
## Automatic Documentation
## Python packages
# Section 4: Databases
## Database Intro
## Postgres Windows Install
## Postgres Mac Install
## Database Schema & Tables
## Managing Postgres with PgAdmin GUI
## Your first SQL Query
## Filter results with "where" keyword
## SQL Operators
## IN Keyword
## Pattern matching with LIKE keyword
## Ordering Results
## LIMIT & OFFSET
## Inserting Data
## Deleting Data
## Updating Data
# Section 5: Python + Raw SQL
## Setup App Database
## Connecting to database w/ Python
## Retrieving Posts
## Creating Post
## Get One Post
## Delete Post
## Update Post
# Section 6: ORMs
## ORM intro
## SQLALCHEMY setup
## Adding CreatedAt Column
## Get All Posts
## Create Posts
## Get Post by ID
## Delete Post
## Update Post
# Section 7: Pydantic Models
## Pydantic vs ORM Models
## Pydantic Models Deep Dive
## Response Model
# Section 8: Authentication & Users
## Creating Users Table
## User Registration Path Operation
## Hashing User Passwords
## Refractor Hashing Logic
## Get User by ID
## FastAPI Routers
## Router Prefix
## Router Tags
## JWT Token Basics
## Login Process  
## Creating a Token
## OAuth2 PasswordRequestForm
## Verify user is Logged In
## Fixing Bugs
## Protecting Routes
## Test Expired Token
## Fetching User in Protected Routes
## Postman advanced Features
# Section 9: Relationships
## SQL Relationship Basics
## Postgres Foreign Keys
## SQLAlchemy Foreign Keys
## Update Post Schema to include User
## Assigning Owner id when creating new post
## Delete and Update only your own posts
## Only Retrieving Logged in User's posts
## Sqlalchemy Relationships
## Query Parameters
## Cleanup our main.py file
## Environment Variables
# Section 10: Vote/Like System
## Vote/Like Theory
## Votes Table
## Votes Sqlalchemy
## Votes Route
## SQL Joins
## Joins in SqlAlchemy
## Get One Post with Joins
# Section 11: Database Migration w/ Alembic
## What is a database migration tool
## Alembic Setup
## Alembic First Revision
## Alembic Rollback database Schema
## Alembic finishing up the rest of the schema
## Disable SqlAlchemy create Engine
# Section 12: Pre Deployment Checklist
## What is CORS?????
## Git PreReqs
## Git Install
## Github
# Section 13: Deployment Heroku
## Heroku intro
## Create Heroku App
## Heroku procfile
## Adding a Postgres database
## Environment Variables in Heroku
## Alembic migrations on Heroku Postgres instance
## Pushing changed to production
# Section 14: Deployment Ubuntu
## Create an Ubuntu VM
## Update packages
## Install Python
## Install Postgres & setup password
## Postgres Config
## Create new user and setup python environment
## Environment Variables
## Alembic migrations on production database
## Gunicorn
## Creating a Systemd service
## NGINX
## Setting up Domain name
## SSL/HTTPS
## NGINX enable
## Firewall
## Pushing code changes to Production
# Section 15: Docker
## Dockerfile
## Docker Compose
## Postgres Container
## Bind Mounts
## Dockerhub
## Production vs Development
# Section 16: Testing
## Testing Intro
## Writing your first test
## The -s & -v flags
## Testing more functions
## Parametrize
## Testing Classes
## Fixtures
## Combining Fixtures + Parametrize
## Testing Exceptions
## FastAPI TestClient
## Pytest flags
## Test create user
## Setup testing database
## Create & destroy database after each test
## More Fixtures to handle database interaction
## Trailing slashes in path
## Fixture scope
## Test user fixture
## Test/validate token
## Conftest.py
## Failed login test
## Get all posts test
## Posts fixture to create test posts
## Unauthorized Get Posts test
## Get one post test
## Create post test
## Delete post test
## Update post
## Voting tests
# Section 17: CI/CD pipeline
## CI/CD intro
## Github Actions
## Creating Jobs
## Setup python/dependencies/pytest
## Environment variables
## Github Secrets
## Testing database
## Building Docker images
## Deploy to Heroku
## Failing tests in pipeline
