# 環境構築

gitリポジトリをクローン後、次のコマンドを入力します。

``` shell
poetry install
poetry run pre-commit install
```

## データベース・アプリケーション設定

環境変数か`.env`ファイルをプロジェクトルートに作成し、値を定義する。
ローカル開発には、特に指定は不要（アプリケーションにハードコーディング）です。

本番環境にデータベースを作成するため、事前にDynamoDBの構成変更権限を持ったIAMユーザーを作成し、値を指定する。
設定は、後述の`zappa_settings.json`の`environment_variables`と同等となる。

```
SERVERLESS_BLOG_CONFIG=production
IAM_DYNAMODB_SAMPLE_ACCESS_KEY_ID=<dynamodbのaccess_key>
IAM_DYNAMODB_SAMPLE_SECRET_KEY=<dynamodbのsecret>
SERVERLESS_SECRET_KEY=<任意のアプリケーション用のシークレット>
SERVERLESS_USER_NAME=<任意のアプリケーション用のユーザー名>
SERVERLESS_USER_PW=<任意のアプリケーション用のユーザー名>
```

## データベース起動

ローカルでアプリケーションを動作させるにはローカル用のデータベース（ローカル用のdynamodb）が必要です。
次のコマンドでデータベースを起動します。

``` shell
docker-compose up -d
```

## データベース作成

環境変数で指定された`SERVERLESS_BLOG_CONFIG`向けにデータベースを作成する。
指定がない場合は、ローカル用のデータベースに接続となる。

データベース初回作成時は`serverless_sample/config.py`の次の箇所をコメントアウトする。
セッションマネージャーが、まだデータベースが存在していないのに参照しようとしてエラーになってしまう。
いけてねぇ〜。

``` python
class ProductionConfig(DotEnvConfig):
    # SESSION_TYPE: str = "dynamodb"
```

次のコマンドを実行する。

``` shell
python -m serverless_sample db init
```

コメントアウトした箇所を元に戻す。

## ローカルでアプリケーションの起動

次のコマンドを入力する。
アプリケーションが起動しログイン画面を表示可能。

``` shell
python -m serverless_sample run
```

ログインは次の通り。

- user: john
- pass: due123

## データベース削除

データベースが不要になったら次のコマンドでデータベースを削除できる。

``` shell
python -m serverless_sample db remove
```

# 本番環境へデプロイするには

## データベースの作成
前章のデータベース・アプリケーション設定を参考にし、本番環境向けに環境変数を設定します。
本番環境にデータベースを作成済みの場合は不要です。

## AWSのクレデンシャルの設定

`~/.aws/credentials`にクレデンシャルを置くことでzappa（boto）がその情報を用いてAWSにアクセスを試みます。
デプロイのため事前に、`apigateway` `cloudformation` `lambda`などの操作権限を持ったIAMユーザーを作成し、設定します。

```
[application_name]
aws_access_key_id = XXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXX
```

## zappa_settings.jsonの設定
プロジェクトルートに`zappa_settings.json`を置くことで、zappaはAWSへアプリケーションをデプロイするためのプロフィールとして認識します。

`zappa_settings.json`には、AWSの構成情報や環境変数などを設定できます。
`environment_variables`には、データベース・アプリケーション設定で設定した本番用環境変数と同等にします。

``` json
{
  "production": {
    // flaskインスタンスなどwsgiのエントリポイントを指定する
    "app_function": "server.app",
    "aws_region": "ap-northeast-1",
    "profile_name": "xxxxx",
    "project_name": "xxxxx",
    "runtime": "python3.8",
    "s3_bucket": "xxxxxxxx",
    // 任意の環境変数を指定できる
    "environment_variables": {
      "SERVERLESS_BLOG_CONFIG": "production",
      "IAM_DYNAMODB_SAMPLE_ACCESS_KEY_ID": "xxxxx",
      "IAM_DYNAMODB_SAMPLE_SECRET_KEY":"xxxxx",
      "SERVERLESS_SECRET_KEY":"xxxxx",
      "SERVERLESS_USER_NAME":"xxxxx",
      "SERVERLESS_USER_PW":"xxxxx",
    },
    // サイズが大きい場合は次の設定をする
    "slim_handler": true,
    // 不要なファイルは除去する。
    "exclude": [
      "setuptools",
      "virtualenv",
      "mypy",
      "isort",
      "flake8",
      "black",
      "pytest",
      "_pytest",
      ".pytest_cache",
      ".mypy_cache",
      "sphinx",
      "sphinx_rtd_theme",
      "markupsafe"
    ]
  }
}
```

## デプロイする
次のコマンドでアプリケーションをデプロイする。
デプロイに成功すれば、エンドポイントが発行され、アプリケーションと通信を行える。

なお、本アプリケーションは事前にデータベースを作成しておく必要があり、次章で説明する（データベース作成前はデプロイに失敗する）。

``` shell
zappa deploy prodction
```

次のコマンドでデプロイされたアプリケーションを削除する。
デプロイ失敗時は、ゴミがAWS上に残っていることがあるため、アンデプロイしておく。

``` shell
zappa undeploy prodction
```

zappaがデプロイで行っている処理は主に次の通り。

1. 指定された任意の環境の設定を`zappa_settings.json`から読み込む
2. アプリケーションをパッケージングする（パッケージングのアルゴリズムやチューニングはよく分からない）
3. パッケージングされたアプリケーションをAWS（`lambda`）へ配置する
4. `apigateway`を構成し、`lambda`関数とつなげる
5. アプリケーションルートに通信を試み、疎通確認を行う

# サーバレスアプリケーションをデプロイして得られた知見

- テンプレ化すればガンガンアプリケーションを公開できそうだ
- パッケージングするサイズは上限が250MBのため、多くのライブラリを使うと上限に達するため大規模は無理そうだ
- mypy_cacheなど不要なフォルダ・ディレクトリが同梱されるため、excludeの設定が必要だ（スマートな除外方法はないのだろうか）
- zappa_settings.jsonは本場環境情報のため、リポジトリに含められない。管理が面倒だ

# サーバレスアプリケーションのデプロイにおける改善点

- GitHub actionとプライベート領域に環境変数を設定して、`zappa_settings.json`を生成したい
- `.env`と`zappa_settings.json`に同じ設定をするのは冗長なのでどうにかしたい