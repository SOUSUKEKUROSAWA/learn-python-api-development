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
    - powershellの場合
      - `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process`
        - ポリシーを一時的に変更し，スクリプトの実行を許可
      - `. venv/Scripts/activate`
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
- スキーマの役割
  - スキーマ
    - DB全体構造の記述であり，DBソフトウェアがDBを保守するのに使用する
    - セキュリティのために，ユーザーごとにDB中の情報へのアクセスを制御する必要があり，その役割を担っているのがスキーマ
  - サブスキーマ
    - 特定のユーザにとって必要な部分だけの記述
      - ex.｜大学のDBには学生の個人情報も教授の個人情報も含まれているが，教務課はサブスキーマによって，個人情報以外の部分しか見れないようになっている．逆に給与課のサブスキーマは教授の職歴は見れるが，学生と教授との連結情報は見れないようになっている．
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
- `response_model=schemas.PostResponse`とした時にエラーが発生する理由
  - 状況
    - `response_model=schemas.PostResponse`としてcreate_postメソッドを実行した時にエラーが発生
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
    - `db.query(models.Post).all()`から返される結果がPostオブジェクトのリストにもかかわらず，`response_model=schemas.PostResponse`と指定していたから
  - 解決策
```diff
- @app.get("/posts", response_model=schemas.PostResponse)
+ @app.get("/posts", response_model=List[schemas.PostResponse])
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
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserRequest, db: Session = Depends(get_db)):
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
- verify_access_tokenメソッドをtry,exeptionで囲う理由
    - tokenが不正または期限切れである可能性があるため
      - decodeプロセスは外部入力に依存するのでエラーハンドリングを書いておくのがベター
      - 外部に依存するもの（＝コード上でバグを修正できないもの）は何でもエラーハンドリングするべき
## Fixing Bugs
- now vs utcnow
  - utcnow｜協定世界時
  - now｜ローカルシステム時刻
  - サーバがアメリカで稼働していて、ユーザがヨーロッパからアクセスした場合、それぞれの地域の時間を使用してしまうと時間のずれが発生します。そのため、すべての時間計算はUTCを基準に行われることが多い
## Protecting Routes
- 現状誰でもリクエスト送れてしまう
  - Dependsで認証ユーザーを設定すると，未認証ユーザーははじかれるようになる
- 認証済みユーザーとしてリクエストするには
  - リクエストヘッダーに以下を追加
    - `Authorization: <token type> <access token>`
## Postman advanced Features
- 環境ごとに変数を設定できる
  - Environmentから変数を作成
  - `{{variable}}`という方法で記述できる
  - 動的に設定することも可能
    - ![](https://storage.googleapis.com/zenn-user-upload/119cb89bf6bb-20230708.png)
    - 何かのアクションのレスポンスを変数に設定するとかもできる
# Section 9: Relationships
## Postgres Foreign Keys
- `TRUNCATE <table name> RESTART IDENTITY;`
  - テーブル内のデータを全削除
    - DELETEよりも高速で、シーケンスもリセットする
    - ※ロールバックできないため注意
- **外部キーの参照先のテーブルが削除された時の挙動**
  - RESTRICT｜エラー発生（削除不可）
    - 関連するデータが存在する限り、主要な行を削除できないことを保証したい時に使用する
  - CASCADE｜関連するすべての外部キーの行も削除
    - 親子関係（親が削除されると子も削除されるなど）を表したい時に使用する
  - SET NULL|参照している行の外部キー値をNULLに設定
    - 関連性がオプショナル（必須ではない）である場合に使用する
      - 例
        - 従業員とマネージャーの関係で、マネージャーが辞任（削除）した場合、従業員のマネージャーフィールドをNULLに設定する
  - SET DEFAULT｜参照している行の外部キー値をその列のデフォルト値に設定
    - デフォルトのバックアップ値がある場合に使用する
      - 例
        - 商品と供給業者の関係で、ある供給業者が倒産した場合、その商品の供給業者をデフォルトの供給業者に設定できる
## SQLAlchemy Foreign Keys
- models.pyでカラムを新たに追加してもDBに反映されない問題
  - 状況
    - models.pyでカラムを新たに追加してもDBに反映されない
  - 原因
    - テーブルが既に作成されている場合，models.pyは読み込まれないから
      - カラムが更新されていることに気づけない
  - 解決策
    - マイグレーションファイルでテーブル定義を管理する
    - 既存のテーブルを削除する
      - 既存のテーブルのデータが特に必要ない場合はこちらでOK
      - 開発環境とか
## Sqlalchemy Relationships
- postオブジェクトから直接紐づくuserオブジェクトが取得できるようになる
## Cleanup our main.py file
- DB接続のコードの省略
  - SQLAlchemyのcreate_engineメソッドによって，最初のクエリが実行された段階で自動でDBへ接続されるようになるため，以下のコードは削除してOK
  - また，SQLAlchemyは接続プールを管理する
    - これにより、接続が必要なときには既存の接続を再利用し、必要なくなったときには自動的に閉じるため，接続や切断を手動で管理する必要がない
```python
while True:
    if datetime.now() > end_time:
        raise Exception("Could not connect to the database within 30 seconds")
    try:
        conn = psycopg2.connect(host=os.getenv("DB_HOST"), database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print(error)
        time.sleep(2)
```
## Environment Variables
- Settingsクラスを定義して環境変数の型を定義することもできる
# Section 10: Vote/Like System
## Vote/Like Theory
- ユーザーは投稿にいいねできる
- いいねは1投稿につき１回のみ
- 各投稿は、いいねの総数も取得する必要がある。
## Votes Table
- post_idとuser_idのペアが必要
  - 誰がどの投稿にいいねしたかを記録する必要がある
  - 複合主キー
- ![](https://storage.googleapis.com/zenn-user-upload/b1330d165538-20230709.png)
## SQL Joins
- ![](https://storage.googleapis.com/zenn-user-upload/3a9be524e513-20230709.png)
- https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-joins/
# Section 11: Database Migration w/ Alembic
## What is a database migration tool
- マイグレーションを使用する目的
  - データベースのテーブル構造をGitで簡単に変更を追跡したり，ロールバックしたりできる
    - インクリメンタルに変更を追跡するため，過去のどの時点でもロールバックできる
- マイグレーションを実現するのに必要なもの
  - データベース接続情報
    - データベースへ接続するためには接続情報が必要です。これは接続文字列や認証情報（ユーザー名、パスワード等）を含むことが多いです。
  - マイグレーションスクリプト
    - データベースのスキーマを変更するためのマイグレーションスクリプトが必要です。マイグレーションスクリプトには、新しいデータベースのバージョンへ移行するためのupgrade()メソッドと、既存のバージョンへ戻るためのdowngrade()メソッドが含まれます。
  - マイグレーションの順序
    - マイグレーションは特定の順序で行われるべきで、これを追跡するためにrevision identifiersが使われます。各マイグレーションには一意のrevision IDが付与され、revisesフィールドで前のマイグレーションを指定します。
  - マイグレーションの自動生成
    - SQLAlchemyモデルのメタデータを使用して、Alembicは新しいマイグレーションを自動的に生成することができます。しかし、自動生成されたマイグレーションは常に手動でレビューするべきで、特に複雑なスキーマ変更やデータの移行が関与する場合には注意が必要です。
  - マイグレーション環境
    - マイグレーションを行う環境（オフラインモードやオンラインモード）を定義する必要があります。
- Alembic
  - https://alembic.sqlalchemy.org/en/latest/
  - DBモデルをSQLAlchemyから自動でプルしてきて，テーブルを生成することができる
  - `pip install alembic`
  - `alembic --help`
  - `alembic init <directory name>`
    - 初期化．alembicディレクトリが作成される
## Alembic Setup
- wondowsでのbashの起動方法
  - Powershellもしくはコマンドプロンプトで`bash`と入力するとbashに切り替わる
- 各ファイルの役割
  - alembic.ini
    - Alembicの設定ファイルです。ここにはデータベースの接続情報、マイグレーションスクリプトの位置、ロギングの設定などが含まれます。
  - env.py
    - マイグレーションの実行環境を定義します。ここでは、SQLAlchemyのモデルのメタデータをAlembicに提供し、それをもとにマイグレーションスクリプトの自動生成を行うことができます。また、データベースの接続設定やオフラインモード、オンラインモードでのマイグレーション実行方法を定義します。
      - オンラインモード
        - オンラインモードでは、マイグレーションは直接データベースに対して実行されます。これは、マイグレーションスクリプトが実行時にデータベースに接続し、その場でSQLコマンドを発行するという意味です。このモードは通常の運用環境や開発環境でよく使用されます。
      - オフラインモード
        - オフラインモードでは、マイグレーションコマンドはSQLスクリプトとして出力され、後で実行するために保存されます。このモードは、マイグレーションが行われる前にSQLコマンドをレビューしたり、データベース接続が利用できない環境（たとえば、プロダクション環境への直接的な接続が制限されている場合）で使用されます。
  - script.py.mako
    - マイグレーションスクリプトのテンプレートです。新しいマイグレーションを作成する際には、このテンプレートが使用されます。テンプレートの中身は、マイグレーションのメタデータ（revision ID、revisesなど）、アップグレードとダウングレードの方法を定義する関数から成ります。アップグレード関数はデータベースを新しいバージョンに更新し、ダウングレード関数はそれを元のバージョンに戻します。
## Alembic First Revision
- `alembic revision -m "create posts table"`
- https://alembic.sqlalchemy.org/en/latest/api/ddl.html#ddl-internals
- `alembic current`
  - 現在のデータベースがどのマイグレーションバージョンに適用されているかを示します。
- `alembic upgrade <revision id（ここで指定したバージョンまで進む）｜進みたいリビジョン数>｜head`
  - ex.｜`alembic upgrade b8ae9a96eb07`｜`alembic upgrade +1`｜`alembic upgrade head`
- alembic_vresionテーブル
  - version_numカラムに実行された最新のrevision idを保持する
  - バージョン管理を行うテーブル
## Alembic Rollback database Schema
- `alembic revision -m "add content column to posts table"`
- `alembic heads`
  - 未実施のマイグレーションも含めた最新リビジョンの表示
- `alembic upgrade head`
  - 最新のリビジョンまでマイグレーションを実施
- `alembic downgrade <revision id（ここで指定したバージョンまで戻す）｜戻したいリビジョン数>`
  - ex.｜`alembic downgrade b8ae9a96eb07`｜`alembic downgrade -1`
## Alembic finishing up the rest of the schema
- `alembic revision -m "create users table"`
- `alembic upgrade head`
- `alembic revision -m "add foreign-key to posts table"`
- `alembic revision -m "add last few columns to posts table"`
- `alembic upgrade +1`
- `alembic revision --autogenerate -m "auto-vote"`
  - 現在のデータベーススキーマとモデルクラスの定義を比較し、データベーススキーマに反映させるべき変更を自動的に検出して新しいマイグレーションスクリプトを生成します。
    - 仕組み
      - `target_metadata = Base.metadata`で、Alembicに対象のデータベースモデルを通知しています。Base.metadataはSQLAlchemy ORMで使用されるすべてのモデルクラスのメタデータ（テーブル名、カラム名、データ型等）を含んでいます。
      - `alembic revision --autogenerate`コマンドが実行されると、Alembicは現在のデータベーススキーマを検査し、モデルクラス（Base.metadata）で定義されたスキーマと比較します。
      - 差分が見つかった場合、その差分を解消するためのSQL文を生成し、新しいマイグレーションスクリプトとして保存します。
# Section 12: Pre Deployment Checklist
## What is CORS?????
- https://fastapi.tiangolo.com/ja/tutorial/cors/
- ブラウザの検証モードでのfetchリクエスト
  - `fetch('http://localhost:8000/').then(res => res.json()).then(console.log)`
  - CORSエラーが発生する
```
Access to fetch at 'http://localhost:8000/' from origin 'https://zenn.dev' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
```
- postmanからの`http://localhost:8000/`へのGETリクエスト
  - 正常にレスポンスが返ってくる
- CORSとは
  - Cross Origin Resource Sharing
  - 特定のドメインのWebブラウザから異なるドメインのサーバへのリクエストを許可する仕組み
    - サーバ側で設定を行う必要あり
      - 通常はレスポンスヘッダにAccess-Control-Allow-Originというヘッダを設定し、どのオリジンからのアクセスを許可するかを指定する
  - デフォルトでは，APIは同一ドメインからのリクエストしか許可しないようになっている
- fetchでアクセスするとCORSエラーが発生して，ブラウザにURLを入力する形でアクセスすると正常にアクセスできる理由
  - ブラウザのURL入力欄からアクセスする場合と、JavaScriptのfetch関数を使ってアクセスする場合とで、同一オリジンポリシーの適用が異なるため
    - ブラウザのURL入力欄からアクセスする場合は、ユーザーが直接操作しているため、セキュリティの制限は緩和される
    - 一方、JavaScriptのfetch関数を使ってプログラムからアクセスする場合は、同一オリジンポリシーが適用されます。したがって、異なるオリジン（google.com）からのリクエストは、通常はブロックされる
- APIを一般に公開するような場合のCORS
  - すべてのオリジンからのアクセスを許可する
  - APIキーによる認証を行う
    - APIを利用するクライアントがそのAPIキーをリクエストに含めることで、APIのサーバー側がそのリクエストが許可されたクライアントからのものであることを確認し、適切にリクエストに応答する仕組み
      - この仕組みにより，特定ユーザーへのアクセス制限やリクエスト数に応じた課金などもできるようになる
## Git PreReqs
- .gitignore
  - `pip freeze > requirements.txt`
    - インストールしたパッケージはrequirements.txtで管理する
      - `pip install -r requirements.txt`
        - requirements.txtに書かれているパッケージをすべてインストール
## Github
- `git branch -M main`
  - 現在のブランチの名前を強制的（Mオプション）にmainに変更
- `git remote add origin https://github.com/~~/~~.git`
  - 新たにリモートリポジトリを設定
- `git config --global user.email ~~~`と`git config --global user.name ~~~`
  - コミットに必要な情報である作成者の名前とメールアドレスのグローバル（マシン上の全てのリポジトリに適用される）登録
# Section 13: Deployment Heroku
## Heroku intro
## Create Heroku App
- herokuにログインしてHerokuアプリを作成すると`git heroku`コマンドが使用できるようになる
  - `git heroku main`でコードをHeroku上にプッシュできる
## Heroku procfile
- ただコードをHerokuに反映しただけではアプリは動作しない
  - Heroku側はサーバの起動方法を知らない
    - procfileに設定を記述することで，実行コマンドなどをHerokuに伝える
- Procfileというファイルをローカルで作成して，以下を追記する
  - `<process type>: <command>`
    - `web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}`
- アプリがうまく起動しない場合（リロードが全然終わらない場合など）
  - ログ出力して調べる
    - `heroku logs --help`
## Adding a Postgres database
- Procfileまで作成してもまだアプリは動かない
  - 接続するDBがないから
    - Herokuサーバ上にDBMSをインストールする必要がある
      - `heroku addons:docs heroku-postgresql:hobby-dev`
        - Herokuのアドオンは、Herokuアプリケーションに追加機能を提供するもの
        - heroku-postgresqlはPostgreSQLデータベースを提供するアドオンで、hobby-devはその中の無料の開発プランを指している
## Environment Variables in Heroku
- 最後に環境変数をHerokuのダッシュボードに設定する
- APIへのアクセスが行えるようになった
## Alembic migrations on Heroku Postgres instance
- ただ，環境変数まで設定してもGETリクエストしかできない
  - 他のメソッドは500 Internal Server Errorになってしまう
    - 原因｜データベース内にテーブルが作成されていないから
- `heroku run "alembic upgrade head"`
  - herokuインスタンス上でマイグレーションを実行
## Pushing changed to production
- `git push origin main`&`git push heroku main`
- データベーススキーマに変更を加えたい場合
  - `heroku run alembic upgrade head`
# Section 14: Deployment Ubuntu
## Create an Ubuntu VM
- Digital Oceanでアプリケーションをホスティングする
  - 月5ドルで最安値だから
- VMが作成され，IPが割り当てられる
## Update packages
- VMにはSSHで接続する
  - `ssh root@<ip of ubuntu VM>`
- なぜVM新規作成後にパッケージをアップデートするのか
  - セキュリティを維持し，最新の機能を利用するため
- `apt update && apt upgrade`
  - python3.8以上がインストールされていることを確認する
  - pipのインストールを実行
  - virtualenvのインストール
  - postgresqlのインストール
## Create new user and setup python environment
- `git clone https://~~ .`
  - VM内でPythonの仮想環境を作成し，そこにGitHub上のコードをクローンする
- `pip install -r requirements.txt`
  - requirements.txtをもとにパッケージをインストール
- `uvicorn app.main:app`
  - サーバーを起動
## Environment Variables
- `export ENV=var`
  - `printenv`
    - 設定されている環境変数の出力
  - `unset ENV`
    - 環境変数の設定を削除
- `vi .env`
- `set -o allexport; source <path to .env>; set +o allexport`
  - このやり方でも環境変数を設定できる
- ただ，ここまでの設定方法だとサーバーを再起動すると設定した環境変数は消えてしまう
  - 起動時に実行されるスクリプト`.profile`に環境変数を設定するコマンドを登録しておく
## Alembic migrations on production database
- マイグレーションファイルは既にクローンしているので，単にマイグレーションコマンドを実行するだけでいい
  - `alembic upgrade head`
- `uvicorn --host 0.0.0.0 app.main:app`
  - すべてのIPアドレスからの接続を受け入れる
- ただ，このままでは自動でリスタートしたりはできない
  - 一旦処理が停止したら再度手動で起動しないといけない状態
    - Gunicornというプロセスマネージャーを利用する
## Gunicorn
- PythonのHTTPサーバーの一つ
  - HTTPリクエストを処理できる
  - Uvicornは単一のワーカープロセスしか起動できないのに対し，Gunicornは複数のワーカープロセスを管理できる
  - 実体は単一のサーバー上で複数のプロセスを並行で扱えるようにマルチプロセスアーキテクチャで設計され，Pythonで実装されたHTTPサーバー
    - マルチプロセスアーキテクチャ
      - 並行処理を可能にするアーキテクチャ
      - 単一のCPUでそれぞれのプロセスに割り当てるCPU時間をコントロールすることで，あたかも同時に複数プロセスを処理しているように見せる技術
        - それに対して並列処理は複数のCPUでプロセスを実際に同時進行させる
- `pip install gunicorn`
  - エラーが発生する場合
    - `pip install httptools`と`pip install uvtool`で大抵解消する
- `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:800`
- Gunicornとは
  - Pythonで書かれたWSGIサーバ
    - WSGI（Web Server Gateway Interface）はPythonにおけるWebサーバーとWebアプリケーションの間の標準的なインターフェース
  - 各ワーカープロセスが独自のアプリケーションインスタンスをホスト
    - 一つのサーバ何で複数のプロセスを並列させる
    - 入ってくるリクエストを並列に処理
      - ワーカーの数は通常、サーバーのCPUコア数に依存する
      - このようにワーカープロセスを使うことで、1つのサーバー上でリソースをより効率的に利用し、性能を向上させることが可能になります。
    - 親プロセスが一つあり，そこがリクエストをさばいてる
## Creating a Systemd service
- gunicorn.service
- systemd
  - Linuxオペレーティングシステムのためのシステムとサービスマネージャ
    - システムの初期化（ブートアップ）を担当し、システム起動時に必要なバックグラウンドサービス（デーモン）の起動や管理を行う
- systemdを利用する理由
  - システムの起動時に自動的にGunicorn（とそれによりホストされるアプリケーション）が起動するように設定できるから
  - 何らかの理由でGunicornプロセスが終了した場合でも、systemdが自動的にそれを再起動する
  - アプリケーションのダウンタイムを最小限に抑えられる
## NGINX
- ![](https://storage.googleapis.com/zenn-user-upload/d2e70c1a1b4f-20230729.png)
- オープンソースのWebサーバ、リバースプロキシサーバ、ロードバランサー、メールプロキシサーバー、そして一般的なTCP/UDPプロキシサーバーとして機能するソフトウェア
- 特に同時接続数が多いウェブサイトに対して高いパフォーマンスを発揮し、メモリ使用量を最小限に抑える設計がされている
- `sudo apt install nginx -y`
- `cat /etc/nginx/sites-available/default`
  - 設定ファイル
    - root
      - ここ設定されているパスがNGINXがデフォルトで見に行っているパス
    - server_name
      - アプリケーションのドメイン名が入る
    - location
      - `location / { ... }`
        - ルートパス配下（すべてのリクエスト）に対する設定
        - proxy_pass
          - 受け取ったリクエストをどのアドレスに送信するかを定義
- まだHTTPSを導入する必要がある
## Setting up Domain name
- ドメイン登録までの流れ
  - ドメイン名を購入する
    - ドメイン名はインターネット上のあなたのアドレスです。これは各種ドメイン登録業者から購入することができます。ドメイン名は一般的に年間契約で、更新料が必要です。
  - DNS設定を行う
    - 購入したドメイン名をあなたのサーバーにリンクさせるために、DNS（Domain Name System）の設定を行う必要があります。これは、ドメイン登録業者のダッシュボード上で行います。
  - サーバーにドメインを設定する
    - あなたのサーバーが新しいドメイン名を認識できるように設定する必要があります。これはサーバーの種類によりますが、一般的にはサーバーの設定ファイルにドメイン名を追加します。
  - SSL証明書を取得する（推奨）
    - HTTPS接続を有効にするためにはSSL証明書が必要です。これはユーザーに安全な接続を提供します。証明書は信頼された認証局から購入することも、Let's Encryptのようなサービスを使って無料で取得することも可能です。
  - ウェブサーバーにSSL証明書を設定する
    - 最後に、SSL証明書をウェブサーバーに設定する必要があります。これにより、ウェブサーバーは安全なHTTPS接続を提供できます。
## SSL/HTTPS
- certbot
  - Certbotは、Let's Encryptという無料のSSL/TLS証明書を発行するサービスと組み合わせて使用するためのツールです。
  - Let's Encryptは自動化されたオープンソースの証明書認証局(CA)で、ウェブサイトの安全な接続を維持するために必要なSSL/TLS証明書を発行します。
  - Certbotはこのプロセスを自動化し、ウェブサーバーの設定を行い、証明書を自動的に更新する機能を提供します。
- certbotのガイドラインに則ってコマンドを実行していくと，SSL証明書の発行とウェブサーバーへのSSL証明書の設定を自動で行ってくれる
  - `/etc/nginx/sites-available/default`を自動で修正してくれる
    - HTTPSへのリダイレクトの設定など
      - HTTPでアクセスしてもHTTPSにリダイレクトとする設定
  - https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal
## NGINX enable
- `systemctl status nginx`
  - NGINXの自動起動が有効になっているか確認
- `systemctl enable nginx`
  - 自動起動の有効化
## Firewall
- Firewall，NGINX，Gunicornの関係性
  - Firewallは最前線（最も低レベルなレイヤーで）でシステムを外部からの不適切なアクセスから保護
    - すべてのインバウンドおよびアウトバウンドトラフィックを管理
    - システム全体のセキュリティポリシーを管理し、不正なトラフィックや攻撃を防ぐ役割を果たす
  - NGINXは入ってきたリクエストを適切にルーティング
    - アクセス制御なども行えるが，それはHTTPレベルでのもので，PレベルやTCP/UDPレベルでの通信を管理することはできない
  - GunicornはPythonアプリケーションと通信を行う
- ufw
  - "Uncomplicated Firewall"の略で、Linuxにおけるファイアウォールの設定を容易に行うためのコマンドラインベースのツール
- `sudo ufw status`
  - active/inactiveの確認
- `sudo ufw allow http`｜`sudo ufw allow https`｜`sudo ufw allow ssh`｜`sudo ufw allow 5432`（ポート5432へのトラフィックの許可．Postgresのトラフィックのこと）
  - それぞれのトラフィックの許可
    - IPアドレスはネットワーク上のコンピュータを識別し，ポート番号はコンピュータ内のソケットを識別する
- `sudo ufw enable`
  - ファイアウォールを有効化
- `sudo ufw status`
  - activeになっていることの確認
- `sudo ufw delete allow http`
  - httpのトラフィックの許可の設定を削除する
## Pushing code changes to Production
- 変更したコードを反映させる方法
  - ローカル開発環境
    - `git push origin main`
  - プロダクションサーバ
    - `cd app/src/`
      - アプリケーションコードがあるディレクトリに移動
    - `git pull`
      - GitHubから最新コードをプル
    - `pip install -r requirements.txt`
      - 新しいパッケージを導入した場合
    - `sudo systemctl restart api`
      - システムの最起動
- 理想はこれらのプロセスがCI/CDパイプラインで自動化されていること
# Section 15: Docker
## Dockerfile
- pythonのベースイメージから始める
- WORKDIR
  - 後続のRUN、CMD、ENTRYPOINT、COPY、ADD命令がここで指定したディレクトリで実行される
- requirements.txtを他のファイルより先にコピーする理由
  - Dockerfileに書かれた処理は，実行時に1行ずつキャッシュされていく
  - パッケージへの変更とアプリケーションコードの変更を分離させておいた方が効率的なキャッシュの利用ができるから先にrequirements.txtをコピーして依存関係のインストールをしている
    - `COPY requirements.txt ./`の代わりに`COPY . .`を依存関係のインストールより前に実行してしまうとアプリケーションコードに変更があるたびに依存関係のインストールも再実行されてしまう
      - 依存関係のインストールは時間のかかる作業だから無駄に実行したくない
- `docker build -t fastapi <directory path of Dockerfile>`
  - ex.｜`docker build -t fastapi .`
## Docker Compose
- Dockerfileから作成したイメージを実行する際のコマンドなどの各種設定を記述するファイル
- services
  - 1サービス，1コンテナのイメージ
- ports
  - ホストマシンとコンテナのポートマッピングの設定
```yml
ports:
  - <port on localhost>:<port on container>
```
- `docker compose up -d`
## Postgres Container
- ボリュームを定義することでデータの永続化ができる理由
  - ボリュームはDockerホスト上のファイルシステムに存在するため，コンテナのライフサイクルから独立している（コンテナが削除されても残り続ける）から
    - コンテナが再作成されるたびにComposeファイルからボリュームが読み込まれてコンテナ内の指定されたディレクトリにマッピングされるからコンテナのライフサイクルに関わらず同じデータを使い続けられる
- コンテナ間の依存関係を定義して，コンテナの起動順序を定義する
  - ![](https://storage.googleapis.com/zenn-user-upload/a5f0038c3e1c-20230813.png)
## Bind Mounts
- デフォルトではアプリケーションコードのコピーはコンテナ起動時にDockerfileが読み込まれてCOPYコマンドが実行された際にのみ実行される
  - 開発環境ではアプリケーションコードが頻繁に変更されるのでその度にコンテナを再起動するのは面倒
    - バインドマウントを利用する
      - `./:/usr/src/app:ro`の意味
        - ホストのカレントディレクトリ（`./`）をコンテナの`/usr/src/app`に同期させる．`ro`はread onlyの略で，コンテナはホストのコードに対して読み取りしか行えない用にする設定
          - コンテナ側でコードを変更してもホストには同期されない
- バインドマウントの設定をしたにもかかわらずコードの変更がリアルタイムで反映されない問題
  - 状況
    - Composeファイルにバインドマウントの設定を追加．コンテナ再起動したところ，コンテナ上のコードは確かにホストのコードと同期してリアルタイムに更新されることが確認できるにもかかわらず，/docsでAPIをたたいてみてもその変更が反映されていない．
  - 原因
    - Dockerfile内でuvicornコマンドにreloadオプションがついていなかったため
      - デフォルトではuvicornはコードの変更を起動時にのみ読みこむ
  - 解決策
    - Dockerfileのuvicornコマンドにreloadオプションを追加して，`docker compose build`で再ビルド
      - ただ，Dockerfileに本番環境では必要のないreloadオプションが残ってしまう
        - 解決策
          - コマンドの実行をComposeファイルで上書きする
            - Composeファイルは環境ごとに作り分けることができる
              - Dockerfileでも`Dockerfile.dev`を作成して，`docker-compose -f docker-compose-dev.yml up --build`のように使用することもできる
                - ただ，Dockerfileは基本亭なイメージの構造を定義するものであるので，環境ごとに大きく変わることが少なく，使い分けるメリットがあまりないためComposeファイルで使い分けるのが一般的
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
