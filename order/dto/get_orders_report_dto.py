from dataclasses import dataclass
from datetime import date
from utils.base_dto import BaseDto


@dataclass
class GetOrdersReportDTO(BaseDto):
    start_date: date = None
    end_date: date = None
