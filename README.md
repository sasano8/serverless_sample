# serverless_sample
AWSのlambdaとapigatewayを使ったWebアプリケーションのサンプルです。

# Serverlessとは
Serverlessとは、できるだけサーバの存在を意識せずにアプリケーションを構成するためのノウハウ。
ここではPythonアプリケーションに対するServerlessの話を中心とする。

# ツール集

## Serverless Frameworkとは
Node.js製のツール。各種クラウド（多分）へのサーバレスなアプリケーションビルドを支援する。
Pythonなど各種言語をサポートしている。

## zappa
Python版のServerless Framework。AWS限定。
flaskなどをwsgiアプリケーションをビルドできる（サーバレスは基本関数単位で使うが、Webアプリケーションも対応できる。zappaがつなぐ役割をしている）。
asgiは未対応。Mangumをプラグインすると対応できるようだが茨の道っぽい。

## boto
AWS SDK for Python。AWSにコンソール上から構成変更できるようになる。
デプロイ時はこのパッケージを含めておく必要があるようで、ないとアプリケーションと通信できない。

## troposphere
AWSの構成ファイルを検証するためのツールのようです。


# 開発ガイド
CONTRIBUTING.mdを参照ください。

