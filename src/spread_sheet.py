from typing import List
import gspread
import config

def add_rows(values: List[List[str | int]]):
    gc = gspread.service_account()

    sh = gc.open_by_key(config.SPREADSHEET_KEY)
    sh.sheet1.append_rows(values)


if __name__ == "__main__":
    add_rows(["A", "B", 3], ["C", "D", 4]) 
