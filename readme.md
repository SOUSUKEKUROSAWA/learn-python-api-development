- Part1
  - https://youtu.be/ToXOb-lpipM
- Part2
  - https://youtu.be/1N0nhahVdqs
# Section 1: Intro
## Course Project
- source code
  - https://github.com/Sanjeev-Thiyagarajan/fastapi-course
## Course Intro
- FastAPI
  - https://fastapi.tiangolo.com/ja
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
- ポート8000にリクエストを送っているはずが，8000以外のポートにリクエストが送られている理由
  - 状況
    - デフォルトでは`127.0.0.1:8000`をリッスンしているはずが，ログでは`127.0.0.1:62218`や` 127.0.0.1:62225`などにリクエストが送られている
  - 原因
    - OSが自動でソースポートを割り当てているから
      - ソースポート
        - ソースポートと宛先ポート（この場合は8000）の組み合わせ、さらには送信元と宛先のIPアドレスと組み合わせることで、インターネット上の各通信が一意に識別される仕組み
        - クライアント（今回の場合はPostman）がサーバーに接続するとき、通信を一意に識別するためにソースポートと呼ばれる一時的なポートを自動的に割り当てる
          - 例）
            - 同じクライアントが同じHTTPメソッドで同じパスのリクエストを複数回送信した場合に，ポートが同じだと識別しづらいため，ポートを分けて識別しやすくしている
            - これによって，サーバは各レスポンスをどのリクエストに対応付ければいいかを判断している
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
- postmanでCollectionを作成
## Retrieve One Post
- 指定したIDのPostが見つからない問題
  - 状況
    - `/posts/1`にGETリクエストを送っても`{"result": null}`が返ってくる
  - 原因
    - idが文字列形式で渡されていたから
      - パスパラメータで渡されるものは全て文字列として渡される
  - 解決策
    - 整数型で受け取る
      - 引数の時点で制限することで関数内で変換処理を書く必要がなくなる
```diff
@app.get("/posts/{id}")
- def get_post(id):
+ def get_post(id: int):
    post = find_post(id)
    return {"result": post}
```
## Changing response Status Codes
- 現状，存在しないIDのPostを取得しようとしてもnullを返すだけ（Statusは`200 OK`を返してしまっている）
  - これだと，フロント側で何が起こったのかを把握できない
- エラーコードやエラーメッセージを毎回ハードコーディングするのはあまりよくない
  - HTTPExeptionライブラリを使用するとよりシンプルに記述できる
- リクエストが成功した際のステータスコード
  - デフォルトは`200 OK`
  - 変更したい場合は，デコレータの第2引数で指定する
## Deleting Posts
- 削除は成功するもののレスポンスメッセージが表示されない問題
  - 状況
    - ID指定の削除は成功し，ステータスコードも`204 No Content`を正常に返しているものの，設定したレスポンスメッセージだけ表示されない
  - 原因
    - FastAPIでは、HTTPステータスコード204（No Content）を指定した場合、ボディにコンテンツが含まれていてはならないとされているから
      - これはHTTPのスペックに従った挙動で、204応答は「リクエストは成功し、それ以上の情報を返す必要はない」という意味を持つ
  - 解決策
    - レスポンスステータスを200（OK）に変更する　OR　レスポンスボディを返さないようにする
```diff
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.remove(post)
-   return {"result": "success"}
+   return
```
## Updating Posts
- 返り値となる変数には`result`と命名する
  - 返り値がどのように加工されたかが追いやすいから
## Automatic Documentation
- `/docs`
  - 組み込みのAPIドキュメントが表示される
    - SwaggerUIを使用して作成されている
- Curlとは？
  - コマンドラインからHTTPリクエストを送信するためのツール
    - FastAPIの組み込みSwagger UIに表示されているCurl
      - Swagger UIから実行したPOSTリクエストを同じCurlコマンドで再現するためのもの
        - そのAPIエンドポイントに対するリクエストをCurlでどのように行うかを示しています。
        - これにより、開発者はAPIのテストやデバッグを容易に行うことができます。
- SwaggerUIの`Successful Response`の部分が`"string"`となってしまっている問題
  - 状況
    - SwaggerUIの`create_post`メソッドの`Successful Response`の部分が`"string"`となってしまっている
      - 実際には`{data: [post]}`のような形式のレスポンスになるはず
  - 原因
    - コード内のデコレータの部分で`response_model`を定義していないから
  - 解決策
    - デコレータの部分で`response_model`を定義する
```diff
+ from typing import List

+ class PostResponse(BaseModel):
+    data: List[Post]

- @app.post("/posts", status_code=status.HTTP_201_CREATED)
+ @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: Post):
    result = post.dict()
    result["id"] = len(posts) + 1
    posts.append(result)
    return {"data": result}
```
- 実装した404エラーのレスポンスをドキュメント化する方法
  - `response`パラメータをデコレータに追加する
```diff
+ class ErrorResponse(BaseModel):
+     detail: str

- @app.get("/posts/{id}")
+ @app.get("/posts/{id}", responses={404: {"model": ErrorResponse, "description": "Post not found"}})
def get_post(id: int):
    result = find_post(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}
```
- `/redoc`
  - リクエストボディのスキーマをより詳細に見れる
  - APIのエンドポイントを試す機能はない
## Python packages
- Pythonパッケージ
  - 一連のPythonファイルを組織化する方法
  - パッケージは通常、特定のディレクトリにグループ化され、そのディレクトリには`__init__.py`という特別なファイルが含まれる
- `__init__.py`
  - そのディレクトリがPythonパッケージであることを示す役割
  - 通常空ですが、パッケージの初期化コードを含むこともある
- appディレクトの中にmain.pyを移動させたので，uvicornのコマンドも変更する必要がある
  - `uvicorn app.main:app --reload`
# Section 4: Databases
## Database Intro
- DBとダイレクトにインタラクトするのは大変
  - DBMSをDBとの間に配置し，簡単にインタラクトを実現する
    - ミドルウェアと呼ばれる所以
    - ![](https://storage.googleapis.com/zenn-user-upload/bc2b8fd5da22-20230604.png)
- Postgres
  - ![](https://storage.googleapis.com/zenn-user-upload/371badd62819-20230604.png)
  - インストール時に作成される`postgres`という名前のDBについて
    - PostgreSQLシステム自体の動作に必要な情報を格納するためのもの．管理用のデータベース
      - 新しいデータベースが作成されるときのテンプレートとしても機能する
      - システムユーザーがPostgreSQLサーバーに接続するためのデフォルトの接続ポイントとしても機能する
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
