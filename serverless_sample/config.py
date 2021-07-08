from typing import Literal

from pydantic import BaseSettings, Field


class DotEnvConfig(BaseSettings):
    """環境変数または.envから値を読み込む。両方定義されている場合は、〇〇が優先される"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class EnvConfig(DotEnvConfig):
    """
    本番かローカルを判断するための設定を読み込む
    """

    SERVERLESS_BLOG_CONFIG: Literal["default", "development", "production"] = "default"

    def get_config(self):
        if self.SERVERLESS_BLOG_CONFIG == "default":
            env = "development"
        else:
            env = self.SERVERLESS_BLOG_CONFIG

        if env == "development":
            return ProductionConfig(
                SERVERLESS_BLOG_CONFIG=env,
                DEBUG=True,
                SECRET_KEY="SECRET_KEY",
                AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID",
                AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY",
                DYNAMODB_ENDPOINT_URL="http://localhost:8000",
                USERNAME="john",
                PASSWORD="due123",
            )
        elif env == "production":
            return ProductionConfig(SERVERLESS_BLOG_CONFIG=env)

        else:
            raise Exception()

    def get_config_as_dict(self):
        return self.get_config().dict()


class ProductionConfig(DotEnvConfig):
    SERVERLESS_BLOG_CONFIG: str
    DYNAMODB_REGION: str = "ap-northeast-1"

    SESSION_TYPE: str = "dynamodb"  # 初回データベース起動時はコメントアウトする必要がある
    SESSION_DYNAMODB_TABLE: str = "serverless_blog_sessions"

    DEBUG: bool = False
    SECRET_KEY: str = Field(..., env="SERVERLESS_SECRET_KEY")
    AWS_ACCESS_KEY_ID: str = Field(..., env="IAM_DYNAMODB_SAMPLE_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="IAM_DYNAMODB_SAMPLE_SECRET_KEY")
    DYNAMODB_ENDPOINT_URL: str = None
    USERNAME: str = Field(..., env="SERVERLESS_USER_NAME")
    PASSWORD: str = Field(..., env="SERVERLESS_USER_PW")

    def dict(self, **kwargs):
        config = super().dict(**kwargs)
        config["SESSION_DYNAMODB_REGION"] = self.DYNAMODB_REGION
        config["SESSION_DYNAMODB_KEY_ID"] = self.AWS_ACCESS_KEY_ID
        config["SESSION_DYNAMODB_SECRET"] = self.AWS_SECRET_ACCESS_KEY
        config["SESSION_DYNAMODB_ENDPOINT_URL"] = self.DYNAMODB_ENDPOINT_URL
        return config


env = EnvConfig().get_config()


class DBMeta:
    # table_name = "serverless_blog_xxxxx"
    region = env.DYNAMODB_REGION
    aws_access_key_id = env.AWS_ACCESS_KEY_ID
    aws_secret_access_key = env.AWS_SECRET_ACCESS_KEY
    host = env.DYNAMODB_ENDPOINT_URL
