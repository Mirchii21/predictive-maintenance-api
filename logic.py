THRESHOLD_WARNING  = 80.0   # Alarm grænse — turbine overopheder
THRESHOLD_CRITICAL = 95.0   # Kritisk grænse — øjeblikkelig handling


def check_temperature(temperature: float) -> str:
    """
    Checker temperaturen mod tærskelværdier.
    Returnerer status: 'normal', 'warning' eller 'critical'
    """
    if temperature >= THRESHOLD_CRITICAL:
        return "critical"
    elif temperature >= THRESHOLD_WARNING:
        return "warning"
    return "normal"


def build_alert_message(turbine_id: str, temperature: float, severity: str) -> str:
    """
    Genererer en beskrivende alarm-besked baseret på alvorlighed.
    """
    if severity == "critical":
        return (
            f"KRITISK: Turbine {turbine_id} har nået {temperature}°C — "
            f"over kritisk grænse på {THRESHOLD_CRITICAL}°C. "
            f"Øjeblikkelig handling påkrævet!"
        )
    return (
        f"ADVARSEL: Turbine {turbine_id} har nået {temperature}°C — "
        f"over alarmgrænse på {THRESHOLD_WARNING}°C. "
        f"Overvågning anbefales."
    )


def should_create_alert(status: str) -> bool:
    """Returnerer True hvis der skal oprettes en alarm."""
    return status in ["warning", "critical"]
