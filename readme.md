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
## Postgres Install
- https://www.postgresql.org/download/
- https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
## Database Schema & Tables
- ![](https://storage.googleapis.com/zenn-user-upload/bd8dce626179-20230604.png)
## Managing Postgres with PgAdmin GUI
- pgAdmin4というアプリを起動
  - GUIアプリ
    - Postgresを扱いやすくしてくれるが，中身ではSQLを発行しているだけ
- PgAdmin4のパスワード
  - PostgreSQLをインストールするときに設定するパスワードとは別物
  - PgAdmin4を使用してPostgreSQLに接続する場合、その接続の設定にはPostgreSQLのスーパーユーザーパスワード（または他のデータベースユーザーのパスワード）が必要になる
- サーバインスタンスの作成
  - 接続設定
    - ホストのIPアドレス・ドメイン
      - localhost
      - AWSなどのクラウドプロバイダーが提供しているドメイン
    - ポート番号
    - 管理DB
      - デフォルトは`postgres`という名前のDB
    - 管理DBのユーザー名とPW
- NOT NULLだが，Default値を持たないカラムを追加する場合
  - 既存のデータに矛盾が生じてしまう
    - 解決策
      - デフォルト値を設定する
## SQL Operators
- `!=`と`<>`は同じ意味
- insertが成功したときの`INSERT 0 1`の意味
  - `INSERT oid count`の形式になっている
    - oid
      - object IDの略
        - 新しく挿入された行のオブジェクトIDを示している（PostgreSQLの初リリースで導入．v.8.1以降でデフォルトでは含まれなくなった）
        - しかし，現代の多くのテーブルではOIDsは使用されていないため、この値は通常0になる
    - count
      - 新しく挿入された行数
- oidが使用されなくなった理由
  - OIDは整数型であり、その範囲は有限（2^32の最大値）だから
    - したがって、大量の行を持つテーブルでは、一意のOIDを割り当てることができなくなるから
    - ただし、現在でも，特定の目的でそれが必要な場合、テーブル作成時に明示的にOIDを含めるよう指定することは可能
  - UUIDがOIDの問題を解消したから
    - UUID(Universally Unique Identifier)
    - 128 bit
      - 可能なUUIDの数は2の128乗（約3.4 x 10^38）
      - 同じUUIDが2回生成される確率は非常に低くなる
    - アルゴリズムのランダム性
    - 同じUUIDを生成する可能性が非常に低い
- `returning <column name you wanna return>, ...`
  - ex.)
    - `insert into posts(name) values("kevin") returning *;`
      - このコマンドによって挿入されたデータが返される
    - delete文とかでも使える
# Section 5: Python + Raw SQL
## Setup App Database
## Connecting to database w/ Python
- w/ = with
- https://www.psycopg.org/docs/usage.html
- `pip install psycopg2`
- venvの中で`WARNING: You are using pip version 22.0.4; however, version 23.1.2 is available.You should consider upgrading via the 'C:\Users\kuros\Documents\learn-python-api-development\venv\Scripts\python.exe -m pip install --upgrade pip' command.`の警告が表示された場合の対処法
  - `python -m pip install --upgrade pip`
- `conn = psycopg2.connect(..., cursor_factory=RealDictCursor)`は何をしているのか
  - データベースから取得する結果をPythonの辞書形式で取得するための設定
    - これにより、カラム名をキーとして結果を取得することが可能になる
- `cursor = conn.cursor()`は何をしているのか
  - カーソルを作成している
    - カーソルとは
      - データベースに対する操作（SQLクエリの実行など）を行うためのオブジェクト
- DB接続は接続されるまでループさせる
  - 接続成功した場合
    - `break`
  - 接続失敗した場合
    - 一定時間`sleep`させた後ループ
  - タイムリミットの設定
    - ずっと失敗し続けると無限ループになってしまう
    - 一定時間失敗し続けたらエラーを返す
## Creating Post
- SQLにパラメータを直接渡さない理由
  - SQLインジェクションを防ぐため
    - `cursor.execute`メソッドの第2引数として渡すことで，ユーザーの入力値がエスケープされ，SQLとして実行されることはなくなる
    - SQLインジェクションの例
      - `; DROP TABLE posts; --`
        - `--`（コメントの開始記号）を付ける意味
          - 攻撃者が意図しないSQLステートメントの残りの部分を無視させるため
            - ex.)
              - `SELECT * FROM users WHERE username = '[input]' AND password = '[input]'`に対して，`admin' --`という入力すると，`SELECT * FROM users WHERE username = 'admin' -- AND password = '[input]'`となり，コメント以降のWHERE句を無視してインジェクションを行えるから
                - ***WHEREなどで条件を指定しているからSQLインジェクションされないというのは誤解***
- `cursor.execute`メソッドでINSERT文を実行し，`cursot.fetchone`メソッドを実行してもDBに変更が反映されない理由
  - 原因
    - Pythonのデータベース接続ライブラリは、デフォルトでトランザクションを自動的に開始するから
      - cursor.execute()を呼び出すと、新しいトランザクションが開始される
  - 解決策
    - `conn.commit()`の追加
```diff
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        insert
        into
            posts
            (title, content, published)
        values
            (%s, %s, %s) returning *
        """,
        (post.title, post.content, post.published)
    )
    result = cursor.fetchone()
+   conn.commit()
    return {"data": result}
```
## Get One Post
- `TypeError: 'int' object does not support indexing`
  - 状況
    - `cursor.execute("""select * from posts where id = %s""",(id))`を実行
    - `TypeError: 'int' object does not support indexing`が発生
  - 原因
    - 第2引数がタプルまたはリストであることが期待されるものの、単なる括弧`(id)`が渡されていたから
  - 解決策
    - 第2引数をタプル形式にする
```diff
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """
        select 
            * 
        from 
            posts
        where
            id = %s
        """,
-       (id)
+       (id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": result}
```
- タプルとリストの違い
  - 変更可能性（Mutability）
    - リスト
      - 変更可能
    - タプル
      - 変更不可能
  - 用途
    - リスト
      - 要素の追加、削除、変更が頻繁に行われる場合
      - リストは順序を持つため、順序が重要な情報を保持する場合
    - タプル
      - 一度設定されたら変更されることのないデータを保持する場合
      - 辞書のキーとしての使用
        - `coordinates_dict = {(37.7749, -122.4194): 'San Francisco'}`
      - 異なる種類のデータを安全にグループ化する
        - `person = ("John Doe", 30, "johndoe@example.com")`
          - タプルは変更できないので，このようなデータ構造を安全に使用できる
# Section 6: ORMs
## ORM intro
- object relational mapper
  - ![](https://storage.googleapis.com/zenn-user-upload/a3ef72792140-20230605.png)
  - Pythonのモデルでテーブルを定義できる
  - Pythonのコードでクエリできる
## SQLALCHEMY setup
- スタンドアローンなORMライブラリ
  - 他のライブラリに依存せずにすべての機能を提供しているライブラリ
- 最新版の確認
  - https://docs.sqlalchemy.org
- インストール
  - https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#install-sqlalchemy
- `pip install sqlalchemy`
- インポート
  - https://fastapi.tiangolo.com/ja/tutorial/sql-databases/#import-the-sqlalchemy-parts
- `engine`
  - SQLAlchemyがクエリを実行するために必要なデータベースAPIへのゲートウェイとして機能する
- `SessionLocal`
  - セッションのライフサイクルを管理する
- `Base`
  - 作成するすべてのモデルクラスの基底クラス
- FastAPIの依存関係
  - 特定の関数やクラスが他の何か（一般的には関数）を必要とするという概念
    - ex.)
      - `get_db`
        - データベースセッションを提供し，リクエスト処理が完了したらリソースを開放する
  - FastAPIの依存関係はHTTPリクエストのライフサイクルと結びついている
- デフォルト値がDBに反映されない問題
  - 状況
    - `published = Column(Boolean, default=True)`としてもDBにデフォルト値が反映されない
  - 原因
    - Pythonレベルで操作していない（つまりSQLAlchemyのSessionを通じてデータを挿入していない）から
  - 解決策
    - DBに直接文字列を追加する`server_default`を使用する
```diff
- published = Column(Boolean, default=True)
+ published = Column(Boolean, server_default='TRUE')
```
- モデルの修正が反映されない理由
  - SQLAlchemyのモデルは定義されているテーブル名と同じテーブルが作成されていれば，その中身は見ずに変更も反映しないから
  - これを解決するのがマイグレーション
## Get All Posts
- ORMを実行するときは，DBセッションをメソッドの引数に渡す必要がある
## Create Posts
- `**post.dict()`
  - Pythonの辞書（dictオブジェクト）をキーワード引数として展開する構文
## Get Post by ID
- `.first()`と`.all()`の違い
  - `db.query(models.Post).filter(models.Post.id == id).all()`としても`db.query(models.Post).filter(models.Post.id == id).first()`としても結果は一緒だが，allの方は1件見つかった後もすべてのデータを検索するので多くのメモリを消費してしまう．firstの方は1件見つかったらそこで検索を止める
## Delete Post
- `synchronize_session=False`
  - DBとセッションの同期を行わないことで，パフォーマンスを向上させるオプション
    - DBからはすぐに削除されるが，セッションが終了するまでPythonのオブジェクトは削除されない
# Section 7: Pydantic Models
## Pydantic vs ORM Models
- Schema/Pydanticモデル
  - リクエスト＆レスポンスの構造を定義するもの
- ORM Models
  - DB内のテーブルを定義する
## Response Model
- メソッドのレスポンスの形式を定義する
- `response_model=schemas.Post`とした時にエラーが発生する理由
  - 状況
    - `response_model=schemas.Post`としてcreate_postメソッドを実行した時にエラーが発生
      - `value is not a valid dict (type=type_error.dict)`
  - 原因
    - レスポンスがSQLAlchemyモデルであるため，Pythonの辞書に変換（シリアライズ）できないこと
      - 戻り値の型を指定しなければFastAPIは戻り値をそのままれす本にするが，今回のようにresponse_modelを指定した場合，レスポンスを生成する前に戻り値を指定されたresponse_modelに変換しようとする．その際にエラーが発生した
  - 解決策
    - PydanticにSQLAlchemyモデルを直接扱うように設定する
```diff
class Post(BaseModel):
    title: str
    content: str
    published: bool
+   class Config:
+       orm_mode = True
```
- 他のモデルを継承できるのが便利
- get_postsメソッドでエラーが発生する理由
  - 状況
    - get_postsメソッドを実行すると，ValidationErrorが発生
  - 原因
    - `db.query(models.Post).all()`から返される結果がPostオブジェクトのリストにもかかわらず，`response_model=schemas.Post`と指定していたから
  - 解決策
```diff
- @app.get("/posts", response_model=schemas.Post)
+ @app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Post).all()
    return result
```
# Section 8: Authentication & Users
## User Registration Path Operation
- レスポンスにパスワードを含めたくない
## Hashing User Passwords
- 誰でも読める形でパスワードをDBに保存しておくのは危険
- https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/#_1
- `pip install passlib[bcrypt]`
- printメソッドでターミナルに値を出力できない問題
  - 状況
    - print()で変数を出力しようとしても表示されない
  - 原因
    - uvicornの仕様で一部のコード（特に初期化や設定のコード）が起動時に一度だけ読み込まれ、その後のコードの変更がリアルタイムに反映されないためだと思われる
  - 解決策
    - uvicornの再起動
- パスワードが正常にハッシュ化されない問題
  - 状況
    - create_userメソッドを実行してもパスワードのハッシュ化が行われない
  - 原因
    - userオブジェクトが関数引数で受け取ったimmutableなPydanticモデルのため
  - 解決策
```diff
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
+   user_dict = user.dict()
    # hash the password - user.password
    hashed_password = pwd_context.hash(user.password)
-   user.password = hashed_password
+   user_dict['password'] = hashed_password
    
-   result = models.User(**user.dict())
+   result = models.User(**user_dict)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
```
## FastAPI Routers
- ルーティングを別ファイルに分離させる
- FastAPI()とAPIRouter()の違い
  - APIRouter
    - エンドポイントのグループ化や大規模なアプリケーションの構造化を可能にする
    - そのエンドポイントを持つFastAPIアプリケーションに組み込むことができる
  - FastAPI
    - 単一のアプリケーション全体を表します
    - 単体で完全なアプリケーションを形成します
## Router Prefix
- 同じパス（`/posts`）などを何度も書くのは少し面倒
## Router Tags
- APIドキュメント状でグルーピング出来る
## JWT Token Basics
- JWT
  - https://developer.mamezou-tech.com/blogs/2022/12/08/jwt-auth/
  - JSON Web Token
  - JSON形式を使って、情報（クレームと呼ばれる）を暗号化して安全に転送する手段を提供する
    - ![](https://storage.googleapis.com/zenn-user-upload/4ff142376cb9-20230702.png)
    - ヘッダ（Header）
      - トークンのタイプと使用されている暗号化アルゴリズムを定義します。
    - ペイロード（Payload）
      - トークンに含めるさまざまな情報（クレーム）が含まれます。
    - シグネチャ（Signature）
      - ヘッダとペイロードを結合し、秘密キーで暗号化して作成されます。
  - 以上3つの要素はそれぞれBase64Urlでエンコードされ、ドット（.）で連結されて一つの文字列となります。
  - ![](https://storage.googleapis.com/zenn-user-upload/a3464bd350e1-20230702.png)
- JWTによる認証の流れ
  - ![](https://storage.googleapis.com/zenn-user-upload/b3b59d449623-20230702.png)
  - ログイン
    - ユーザーがユーザー名とパスワードでログインします。
  - 認証
    - サーバーがユーザーの認証情報を検証し、その結果が正しい場合、サーバーはJWTを生成してクライアント（ユーザー）に返します
  - JWTの保存
    - クライアントはそのJWTを保存し、次回からそのJWTをヘッダに含めてリクエストを送ります。
  - 再度アクセス時の認証
    - JWTが含まれるリクエストを受け取ったサーバーは、JWTの署名を確認し、署名が正しい（改ざんされていない）場合、リクエストを処理します。
    - ![](https://storage.googleapis.com/zenn-user-upload/c076e5f1fcd3-20230702.png)
    - ![](https://storage.googleapis.com/zenn-user-upload/f9d44f46830d-20230702.png)
      - ペイロードの内容を改ざんしたものの，シグネチャを変えることはできないため，検証ではじかれる仕組みになっている
- JWTの特徴
  - JWTによる認証はステートレスなのが特徴で、サーバーはユーザーのセッション情報を保存する必要がない
    - これはスケーラビリティが高いと言えます。
      - 新たなサーバーインスタンスを追加した場合でも、そのインスタンスはJWTを解釈するためのロジック（暗号化／復号化するための秘密鍵も必要）さえ持っていれば、すぐにリクエストの処理を開始できるから
        - セッション情報をサーバーが管理しているステートフルなシステムでは、各サーバーは共有のセッションストアを参照するか、あるいはセッション情報を持つ特定のサーバーにリクエストをルーティングする必要があります。これは、新しいサーバーの追加や負荷分散のための設定が複雑になる原因となります。
  - しかし、一度発行されたJWTは無効化が難しく、有効期限が切れるまで有効なままなので、セキュリティの観点から注意が必要です。
    - JWTはシグネチャにより改ざんできないようにはなっているが，JWTが漏洩した場合，ペイロードを閲覧すること自体はできてしまう
  - また，JWTによる認証には，HMAC（共有秘密鍵）方式と公開鍵方式の2種類があり，HMACの方は鍵漏洩のリスクがある一方で，公開鍵方式では，秘密鍵が署名を作成し，公開鍵が署名を検証（復号化）するので，鍵漏洩のリスクがないという特徴がある．
- セッションを用いた認証処理の流れ
  - ログイン
    - ユーザーがログイン画面でユーザー名とパスワードを入力します。その情報はサーバーに送られます。
  - 認証
    - サーバーは送られてきたユーザー名とパスワードを確認し、正しいものであれば認証成功とします。その際にサーバーはセッションを作成し、セッションIDを生成します。
  - セッション情報の保存
    - サーバーはセッションIDと、そのセッションに関連する情報（例えばユーザーIDなど）をセッションストア（メモリ、データベース、ファイルなど）に保存します。
  - セッションIDの返送
    - サーバーはセッションIDをクライアント（ユーザー）に返します。このセッションIDは通常、Cookieとしてブラウザに保存されます。
  - 再度アクセス時の認証
    - ユーザーが再度サーバーにアクセスするとき、ブラウザは自動的にそのCookie（セッションID）をリクエストに含めてサーバーに送ります。サーバーはそのセッションIDを受け取り、セッションストアで対応するセッション情報を見つけます。そのセッションが有効であれば、ユーザーは既に認証されていると見なされ、リクエストは処理されます。
  - セッションを用いた認証は非常に一般的で、その実装は各言語やフレームワークで提供されていることが多いです。しかし、セッション情報をサーバー側で管理する必要があり、大規模なシステムやマイクロサービス環境では、セッション情報の同期やセッションストアの管理など、扱いが複雑になることがあります。そのような場合、JWTのようなステートレスな認証方法が適してくると言えます。
## Login Process
- ハッシュ化の特徴は一方向性（ハッシュされた文字列は複合できない）
- ![](https://storage.googleapis.com/zenn-user-upload/6393cbaec011-20230702.png)
- ハッシュ関数とは
  - 以下の特性を持つもの
    - 事前像抵抗性（Pre-Image Resistance）
      - 与えられたハッシュ値 h から元のメッセージ m を計算することは計算的に不可能です。つまり、ハッシュ値から元のパスワードを推測することは非常に困難です。
    - 二次事前像抵抗性（Second Pre-Image Resistance）
      - 与えられたメッセージ m1 に対し、同じハッシュ値 h を持つ別のメッセージ m2 を見つけることは計算的に不可能です。
    - 衝突抵抗性（Collision Resistance）
      - 任意の二つの異なるメッセージ m1 と m2 に対し、同じハッシュ値 h を持つものを見つけることは計算的に不可能です。
  - ハッシュ関数が事前像抵抗性を持つことができる理由
    - 単方向性と情報の損失があるから
      - ハッシュ関数はデータを非常に特殊な方法で処理し、その結果の情報量を大幅に減少させるためです。
        - たとえば、SHA-256のようなハッシュ関数を使用すると、どんな大きさのデータも256ビットのハッシュ値に変換されます。このプロセスでは、元のデータの詳細な情報が失われます。そのため、ハッシュ値から元のデータを完全に再現することは不可能です。
      - さらに、ハッシュ関数は非常に微小な入力の違いでも全く異なるハッシュ値を生成します（これを「エイバランシェ効果」と呼びます）。したがって、元のデータが何であったかをハッシュ値から推測することは困難を極めます。
  - bcryptによるパスワード検証の仕組み
    - bcryptはハッシュ時にソルト（ランダムな文字列）をハッシュ値に組み込むことで，異なるユーザーが同じパスワードを使用しても異なるハッシュ値が生成される
      - ソルトはユーザー固有でハッシュ化されたパスワードとセットで保存されているので，同じユーザーがログインすれば，同じハッシュ値が使用される
## Creating a Token
- ログイン認証時のレスポンスステータスコード
  - 404　OR　403
    - 403が意味としては妥当で一般的だが，セキュリティ上の観点から認証に失敗した場合は全て404として具体的な情報を隠すというアプローチをとるシステムもある
- https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/?h=bcry#python-jose
- `pip install python-jose[cryptography]`
- `openssl rand -hex 32`
  - 安全なランダム秘密鍵の生成
- Bearerトークンとは
  - このトークンは、クライアントがその後のリクエストで使用することができ、そのリクエストが認証され、リソースにアクセスできることを意味します。
- https://jwt.io/
## OAuth2 PasswordRequestForm
- OAuth2PasswordRequestFormクラス
  - ![](https://storage.googleapis.com/zenn-user-upload/00873fe3fad0-20230702.png)
  - FastAPIが提供する依存性ツールの1つで、ユーザーのログイン情報（通常はユーザー名とパスワード）をリクエストから取得するために使用されています。
    - username
      - ユーザー名（ここでは、それはメールアドレスとして扱われている）
    - password
      - ユーザーのパスワード
    - scope
      - オプションの認証スコープ
    - grant_type
      - オプションのグラントタイプ
## Verify user is Logged In
- Dependsとは
  - FastAPIの依存性注入システムの一部
  - 依存性注入
    - コードの柔軟性とテストのしやすさを向上させるソフトウェアデザインパターンの1つ
    - オブジェクトや関数が他のコード（「依存関係」）に依存する方法を制御
      - ある関数が別の関数に依存している場合、その関数はDependsを使用してその依存関係を宣言します。
  - メリット
    - ETC（変更容易性が高まる）
      - メソッド内にコードを書かなくてよくなるから
    - テスト中に実際の依存関係（例えば、実際のデータベース接続や実際の認証システム）をモック（偽の）オブジェクトで置き換えることが容易になります。
    - 自動エラーハンドリング
      - 依存関係が問題を引き起こす場合（例えば、データベース接続に問題がある場合や、認証トークンが無効な場合など）、FastAPIの依存性システムはこれらの問題を自動的にハンドリングします。
## Fixing Bugs
- now vs utcnow
  - utcnow｜協定世界時
  - now｜ローカルシステム時刻
  - サーバがアメリカで稼働していて、ユーザがヨーロッパからアクセスした場合、それぞれの地域の時間を使用してしまうと時間のずれが発生します。そのため、すべての時間計算はUTCを基準に行われることが多い
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
