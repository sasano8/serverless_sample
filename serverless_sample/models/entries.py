from datetime import datetime

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from ..app import app
from ..config import DBMeta


class Entry(Model):
    class Meta(DBMeta):
        table_name = "serverless_blog_entries"

    id = NumberAttribute(hash_key=True, null=False)
    title = UnicodeAttribute(null=True)
    text = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=datetime.now)
