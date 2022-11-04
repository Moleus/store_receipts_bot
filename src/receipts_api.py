from enum import Enum
from io import TextIOWrapper
from typing import Any, Dict
import requests
import config

from models import GoodDetail, ReceiptInfo, ReceiptMetadata, ReceiptResult


class StatusCodes(Enum):
    SUCCESS = 1
    TOO_MANY_REQUESTS = 3


def request_receipt_details(qr_file_data: TextIOWrapper) -> ReceiptResult:
    url = 'https://proverkacheka.com/api/v1/check/get'
    data = {'token': config.PROVERKA_CHECKA_TOKEN}
    files = {'qrfile': qr_file_data}
    response = requests.post(
        url, data=data, files=files)  # send request to API
    parsed_data = response.json()
    list_of_items = []
    if (response.status_code == 200):
        if (parsed_data["code"] != StatusCodes.SUCCESS.value):
            return ReceiptResult(is_ok=False, errror_msg=str(parsed_data["data"]))

        receipt_info = parsed_data["data"]['json']
        metadata = get_metadata(receipt_info)

        for k in receipt_info['items']:
            unit_price = round(k['price']/100) if is_countable(k) else to_rub_per_kg(k['price'], k['quantity'])
            list_of_items.append(GoodDetail(
                label=k['name'], unit_price=unit_price, count=k['quantity'], sum_price=k['price']/100))
        return ReceiptResult(ReceiptInfo(goods=list_of_items, metadata=metadata))
    else:
        return ReceiptResult(is_ok=False, errror_msg="Response status code is " + response.status_code)


def get_metadata(receipt_info: Dict[str, Any]) -> ReceiptMetadata:
    return ReceiptMetadata(
        receipt_id=receipt_info.get("metadata", {}).get("id", -1),
        retail_place=receipt_info.get("retailPlace", ""),
        total_sum=receipt_info.get("totalSum", 0)/100,
        date_time=receipt_info.get("dateTime", "")
    )


def is_countable(item):
    return isinstance(item['quantity'], int)


def to_rub_per_kg(total_price: float, quantity: float) -> int:
    return round(float('{:.2f}'.format(total_price / 100 * quantity)))
