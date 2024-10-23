from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class DateRange:
    start_date: date
    end_date: date

    def split_to_chunks(self, interval: timedelta) -> list["DateRange"]:
        chunks = [DateRange(self.start_date, self.end_date)]
        while chunks[-1].end_date - chunks[-1].start_date > interval:
            cur = chunks[-1]
            cur_end_date = cur.start_date + interval
            new = DateRange(start_date=cur_end_date, end_date=cur.end_date)
            cur.end_date = cur_end_date
            chunks.append(new)
        return chunks
