from dataclasses import dataclass
from enum import Enum
from typing import List
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import Decoded


@dataclass
class QrScanResult():
    data: str = None
    is_ok: bool = True


""" Unused """
class QrReader():
    def __init__(self):
        pass

    @staticmethod
    def read_qr(path: str) -> QrScanResult:
        qr_data: List[Decoded] = decode(
            Image.open(path), symbols=[ZBarSymbol.QRCODE])
        if (len(qr_data) == 0):
            return QrScanResult(is_ok=False)
        return QrScanResult(qr_data[0].data.decode())
