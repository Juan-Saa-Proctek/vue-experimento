import asyncio
from app.integrations.pch_connection import PCHConnection
import json

async def test():
    conn = PCHConnection(host="pchcloud", username="demo", password="password")
    await conn.login()
    
    recording_id   = "PCH1420-2020260162.2022-01-26 10_56_30.20260121031308"
    device_host_id = "SamsoeFerry.uuqphidi"
    device_id      = "PCH1420-2020260162"
    
    url = f"{conn.get_service_url('backend')}/timerecording/recording/channel/raw"
    response = await conn.client.get(
        url,
        params={
            "session_token": conn.session_token,
            "recordingId":   recording_id,
            "deviceHostId":  device_host_id,
            "deviceId":      device_id,
            "channel":       1,
        }
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    # Solo ver estructura, no los 24000 samples
    print(json.dumps({k: v for k, v in data.items() if k != "samples"}, indent=2))
    print(f"Samples: {len(data.get('samples', []))}")

asyncio.run(test())