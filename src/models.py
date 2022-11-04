from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class GoodDetail:
    label: str
    unit_price: int
    count: int
    sum_price: int


@dataclass_json
@dataclass
class ReceiptMetadata:
    receipt_id: int
    retail_place: str
    total_sum: int
    date_time: str


@dataclass_json
@dataclass
class ReceiptInfo:
    metadata: ReceiptMetadata = None
    goods: List[GoodDetail] = None


@dataclass_json
@dataclass
class ReceiptResult:
    receipt: ReceiptInfo = None
    is_ok: bool = True
    errror_msg: str = ""
