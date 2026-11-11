# WeatherSeal

**Local-first weather, delay, site condition, and force majeure evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1 and the Operator Pages suite.

## Why WeatherSeal?

Weather delays, differing site conditions, and force majeure events are among the most common (and expensive) sources of construction disputes. Without contemporaneous, verifiable records of conditions, rainfall, temperature, wind, site access, or productivity impact, claims for time extensions or extra costs often fail.

WeatherSeal captures structured weather and condition records (observations, measurements, impacts, crew effects, media hashes) and seals them into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients, owners, or auditors verify with free QuantumGuard verifier (`qg verify`).
- Deterministic: same inputs → same sealed pack.
- Pairs with DailySeal, TimeSeal, ChangeOrderSeal, and the rest of the Operator Pages suite.

## Quick Start

```bash
pip install cryptography

python3 src/weatherseal.py --demo
python3 src/weatherseal.py --json samples/weather-001.json --out sealed-weather.json
```

Verify:
```bash
qg verify sealed-weather.json
```
Expected: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $59   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $169  | + batch mode + CSV/HTML export + reseller rights |
| Agency    | $449  | + white-label + multi-site key management |

**Buy Operator Pack:** Contact danpennic@gmail.com or use Stripe checkout for live link.  
Repo: https://github.com/danpennic-sys/weatherseal

Source free under Apache-2.0 OR MIT. Commercial packs sold separately.

## License

Apache-2.0 OR MIT
