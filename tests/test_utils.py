import dateutil.parser
import requests
from requests import HTTPError
import requests_mock
import pytest
import datetime
from eve_invoice.utils import downloadIfNewer

url = "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/fsd.zip.checksum"

@pytest.fixture
def checksumMock(requests_mock: requests_mock.Mocker):
    requests_mock.head(
        url,
        headers={
            "x-amz-id-2": "CLY0J3sTDgJmmTh0EnS+lqYuxjvmbvTxEe0qPSGIvQqmii/+t9c1Q26xtCwmU8zvCS3SMismEDozKDLhthxUJoqVw/G2WvnJ",
            "x-amz-request-id": "PE9FN81NZSJADC5P",
            "Date": "Sat, 19 Jul 2025 09:03:31 GMT",
            "last-modified": "Mon, 07 Jul 2025 13:41:33 GMT",
            "ETag": '"90209121f928a294a5959f45bfdf7aaa"',
            "x-amz-server-side-encryption": "AES256",
            "Accept-Ranges": "bytes",
            "Content-Type": "binary/octet-stream",
            "Content-Length": "32",
            "Server": "AmazonS3",
        },
    ) 
    # return requests_mock

def test_get_employee(checksumMock):
 
    etag, dt  = downloadIfNewer(url)
    assert dt == datetime.datetime(2025, 7, 7, 13, 41, 33, tzinfo= datetime.UTC)
     
