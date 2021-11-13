from pydantic import BaseModel
# 2. Class which describes Bank Notes measurements


class San(BaseModel):
    ticket_id: int
    description: str
