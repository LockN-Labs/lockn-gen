#!/usr/bin/env python3
"""Test voice cloning with shorter 15s sample."""
import base64
import requests

# Load the trimmed audio file
with open('/home/sean/.openclaw/workspace/sean-voice-15s.wav', 'rb') as f:
    ref_audio = base64.b64encode(f.read()).decode('utf-8')

# Test text
test_text = "Hello Sean, this is your cloned voice. LockN Score is ready!"

print(f"Reference audio size: {len(ref_audio)} bytes (base64)")
print(f"Test text: {test_text}")
print("\nSending X-Vector voice clone request...")

try:
    response = requests.post(
        "http://localhost:8880/v1/audio/voice-clone",
        json={
            "input": test_text,
            "ref_audio": ref_audio,
            "x_vector_only_mode": True,
            "response_format": "wav"
        },
        timeout=180
    )
    
    if response.status_code == 200:
        with open('/home/sean/.openclaw/workspace/sean-cloned.wav', 'wb') as f:
            f.write(response.content)
        print(f"\n✅ SUCCESS! Saved to sean-cloned.wav ({len(response.content)} bytes)")
    else:
        print(f"\n❌ Error {response.status_code}:")
        print(response.text[:500])
except Exception as e:
    print(f"\n❌ Exception: {e}")
