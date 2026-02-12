#!/usr/bin/env python3
"""Test voice cloning with Sean's voice sample."""
import base64
import json
import requests

# Load the audio file
with open('/home/sean/.openclaw/workspace/sean-voice-sample.wav', 'rb') as f:
    ref_audio = base64.b64encode(f.read()).decode('utf-8')

# The transcript of what Sean read
ref_text = """She sees the bee by the sea. The cat sat on the flat mat. Father carved the car in the dark. Put the good book on the foot. Food rules — choose the cool blue moon. The bus must rush to cut the nut. Her first nurse works early. They play by the bay every day. I find time to write by night. The boy enjoyed the noisy toy. How now the brown cow found the town. Go slow over the road to home. Pat bought a big top pot. Two tall trees stood in the tent. Cold cake came from the kitchen. Five fine foxes found fresh fish. Think through three thick things. She showed her shiny shoes. Choose the cheese and catch the chief. My mother made muffins Monday. The king sang a long song. Red roses rarely grow right. Look at the little light on the lake."""

# Test text
test_text = "Hello Sean, this is your cloned voice speaking. LockN Score is ready to track your ping pong games!"

print(f"Reference audio size: {len(ref_audio)} bytes (base64)")
print(f"Reference text length: {len(ref_text)} chars")
print(f"Test text: {test_text}")
print("\nSending voice clone request...")

try:
    response = requests.post(
        "http://localhost:8880/v1/audio/voice-clone",
        json={
            "input": test_text,
            "ref_audio": ref_audio,
            "ref_text": ref_text,
            "x_vector_only_mode": False,
            "response_format": "wav"
        },
        timeout=120
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
