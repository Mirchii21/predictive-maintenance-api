from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TurbineReadingCreate(BaseModel):
    turbine_id:  str   = Field(..., example="turbine-01")
    temperature: float = Field(..., example=87.5)
    unit:        str   = Field(default="celsius", example="celsius")


class TurbineAlertOut(BaseModel):
    id:          int
    turbine_id:  str
    severity:    str
    temperature: float
    message:     str
    created_at:  datetime

    class Config:
        from_attributes = True


class TurbineReadingOut(BaseModel):
    id:           int
    turbine_id:   str
    temperature:  float
    unit:         str
    status:       str
    timestamp:    datetime
    alerts:       List[TurbineAlertOut] = []

    class Config:
        from_attributes = True


class ReadingResponse(BaseModel):
    id:            int
    turbine_id:    str
    temperature:   float
    status:        str
    alert_created: bool
    message:       str
    timestamp:     datetime
