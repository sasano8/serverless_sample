from datetime import datetime

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from ..app import app
from ..config import DBMeta


class Session(Model):
    class Meta(DBMeta):
        table_name = "serverless_blog_sessions"

    SessionId = UnicodeAttribute(hash_key=True, null=False)
    Session = UnicodeAttribute(null=False)
