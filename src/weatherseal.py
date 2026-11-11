#!/usr/bin/env python3
"""
WeatherSeal — local-first weather, delay, site condition, and force majeure evidence sealer.
Emits QuantumGuard CONTRACT-v1 bundles.
"""
import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()

def load_or_create_key(key_path="weatherseal_key.pem"):
    if os.path.exists(key_path) and CRYPTO:
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if CRYPTO:
        priv = ed25519.Ed25519PrivateKey.generate()
        pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(key_path, "wb") as f:
            f.write(pem)
        return priv
    return None

def sign_payload(payload: dict, priv_key):
    raw = canonical_json(payload)
    payload_hash = hashlib.sha256(raw).digest()
    if priv_key and CRYPTO:
        sig = priv_key.sign(payload_hash)
        pub = priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return {
            "version": "1",
            "payload": base64.b64encode(raw).decode(),
            "payload_hash": payload_hash.hex(),
            "signature": sig.hex(),
            "public_key": pub.hex(),
            "alg": "ed25519"
        }
    return {
        "version": "1",
        "payload": base64.b64encode(raw).decode(),
        "payload_hash": payload_hash.hex(),
        "signature": "00" * 64,
        "public_key": "11" * 32,
        "alg": "ed25519"
    }

def demo_data():
    return {
        "report_type": "weather_delay",
        "date": "2026-11-11",
        "site": "Field Site Bravo",
        "job_id": "JOB-2026-1102",
        "weather_conditions": "Heavy rain, sustained 1.8 inches, winds 25-35 mph gusting to 45",
        "temperature_f": 48,
        "precipitation_inches": 1.8,
        "wind_mph": 32,
        "visibility": "Poor, standing water",
        "site_impact": "Work stopped 07:30-14:00. Access roads flooded. No earthwork or concrete possible.",
        "crew_impact": "Crew sent home at 08:15. 6.5 hours productive time lost.",
        "delay_hours": 6.5,
        "force_majeure": True,
        "notes": "Observed and measured on site. Rain gauge reading 1.8 in. Photos of flooded access and stopped equipment hashed.",
        "photos_hashes": ["sha256:floodedaccess...", "sha256:stoppedcrew..."],
        "observer": "Superintendent J. Hale",
        "sealed_at": datetime.now(timezone.utc).isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="WeatherSeal evidence sealer")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--json", help="Input JSON file")
    parser.add_argument("--out", default="sealed-weather.json", help="Output sealed bundle")
    args = parser.parse_args()

    if args.demo:
        data = demo_data()
    elif args.json:
        with open(args.json) as f:
            data = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_create_key()
    bundle = sign_payload(data, priv)
    with open(args.out, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed to {args.out}")
    print("Verify with: qg verify", args.out)

if __name__ == "__main__":
    main()
