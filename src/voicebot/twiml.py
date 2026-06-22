from __future__ import annotations

import xml.etree.ElementTree as ET

from .config import Settings
from .scenarios import Scenario


def build_twiml(settings: Settings, scenario: Scenario, run_id: str) -> str:
    response = ET.Element("Response")
    connect = ET.SubElement(response, "Connect")
    stream = ET.SubElement(
        connect,
        "Stream",
        {
            "url": settings.stream_url,
            "name": f"voicebot-{scenario.id[:32]}",
            "statusCallback": settings.stream_status_url,
            "statusCallbackMethod": "POST",
        },
    )
    ET.SubElement(stream, "Parameter", {"name": "scenario_id", "value": scenario.id})
    ET.SubElement(stream, "Parameter", {"name": "run_id", "value": run_id})
    ET.SubElement(stream, "Parameter", {"name": "patient_name", "value": scenario.patient_name})
    xml = ET.tostring(response, encoding="unicode", short_empty_elements=True)
    return f'<?xml version="1.0" encoding="UTF-8"?>{xml}'
