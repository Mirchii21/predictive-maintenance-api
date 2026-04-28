from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db, engine, Base
from app import models, schemas
from app.logic import check_temperature, build_alert_message, should_create_alert

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Turbine Predictive Maintenance API",
    description="REST API til overvågning af turbinetemperatur for Intelligent IoT Solutions A/S",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "Turbine Predictive Maintenance API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/turbine-readings", response_model=schemas.ReadingResponse, status_code=201)
def create_reading(data: schemas.TurbineReadingCreate, db: Session = Depends(get_db)):
    """
    Modtag en temperaturmåling fra en turbine.
    Checker automatisk om temperaturen overskrider 80°C grænsen.
    Opretter alarm hvis nødvendigt.
    """
    status = check_temperature(data.temperature)

    reading = models.TurbineReading(
        turbine_id  = data.turbine_id,
        temperature = data.temperature,
        unit        = data.unit,
        status      = status,
        timestamp   = datetime.now()
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    alert_created = False
    if should_create_alert(status):
        message = build_alert_message(data.turbine_id, data.temperature, status)
        alert = models.TurbineAlert(
            reading_id  = reading.id,
            turbine_id  = data.turbine_id,
            severity    = status,
            temperature = data.temperature,
            message     = message,
            created_at  = datetime.now()
        )
        db.add(alert)
        db.commit()
        alert_created = True
    else:
        message = f"Turbine {data.turbine_id}: temperatur {data.temperature}°C er normal."

    return schemas.ReadingResponse(
        id            = reading.id,
        turbine_id    = data.turbine_id,
        temperature   = data.temperature,
        status        = status,
        alert_created = alert_created,
        message       = message,
        timestamp     = reading.timestamp
    )


@app.get("/turbine-readings", response_model=List[schemas.TurbineReadingOut])
def get_readings(db: Session = Depends(get_db)):
    """Hent alle temperaturmålinger fra alle turbiner."""
    return db.query(models.TurbineReading).order_by(
        models.TurbineReading.timestamp.desc()
    ).all()


@app.get("/turbine-readings/{turbine_id}", response_model=List[schemas.TurbineReadingOut])
def get_readings_by_turbine(turbine_id: str, db: Session = Depends(get_db)):
    """Hent alle målinger for en specifik turbine."""
    readings = db.query(models.TurbineReading).filter(
        models.TurbineReading.turbine_id == turbine_id
    ).order_by(models.TurbineReading.timestamp.desc()).all()

    if not readings:
        raise HTTPException(status_code=404, detail=f"Ingen målinger fundet for turbine {turbine_id}")
    return readings


@app.get("/alerts", response_model=List[schemas.TurbineAlertOut])
def get_alerts(db: Session = Depends(get_db)):
    """Hent alle alarmer — kun målinger der overskred 80°C grænsen."""
    return db.query(models.TurbineAlert).order_by(
        models.TurbineAlert.created_at.desc()
    ).all()


@app.get("/alerts/{turbine_id}", response_model=List[schemas.TurbineAlertOut])
def get_alerts_by_turbine(turbine_id: str, db: Session = Depends(get_db)):
    """Hent alle alarmer for en specifik turbine."""
    alerts = db.query(models.TurbineAlert).filter(
        models.TurbineAlert.turbine_id == turbine_id
    ).order_by(models.TurbineAlert.created_at.desc()).all()

    if not alerts:
        raise HTTPException(status_code=404, detail=f"Ingen alarmer fundet for turbine {turbine_id}")
    return alerts
