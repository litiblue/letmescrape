import scrapy
import pytest
from scrapy.exceptions import DropItem

from letmescrape.pipelines import RequiredFieldsPipeline


def test_required_field_pipeline():
    class Item(scrapy.Item):
        required_field = scrapy.Field(required=True)

    missing_field_item = Item()
    normal_item = Item(required_field='value')

    pipeline = RequiredFieldsPipeline()

    assert pipeline.process_item(normal_item) is normal_item

    with pytest.raises(DropItem) as exc_info:
        pipeline.process_item(missing_field_item)
    assert 'required_field' in str(exc_info.value)