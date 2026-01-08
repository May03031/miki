from pydantic import BaseModel

class LimitRecord(BaseModel):
    limit: int = 5   # số dòng muốn lấy
    offset: int = 0   # bắt đầu từ dòng thứ mấy