import sys
import re

# Regex patterns
pacc1_re = re.compile(r"pacc1\s*=\s*([0-9.]+)")
p0loss_re = re.compile(r"p0loss\s*=\s*([0-9.]+)")
p1loss_re = re.compile(r"p1loss\s*=\s*([0-9.]+)")
nsamp_re = re.compile(r"nsamp\s*=\s*([0-9.]+)")
total_loss_re = re.compile(r",\s*loss\s*=\s*([0-9.]+)")

print("Paste logs below, then press CTRL+D (Linux/Mac) or CTRL+Z + Enter (Windows):\n")
text = sys.stdin.read()

entries = []
for line in text.splitlines():
    nsamp = nsamp_re.search(line)
    pacc1 = pacc1_re.search(line)
    p0 = p0loss_re.search(line)
    p1 = p1loss_re.search(line)
    total_loss = total_loss_re.search(line)

    if nsamp and pacc1 and total_loss:
        entries.append({
            "samples": float(nsamp.group(1)),
            "pacc1": float(pacc1.group(1)),
            "loss": float(total_loss.group(1)),
            "p0loss": float(p0.group(1)) if p0 else None,
            "p1loss": float(p1.group(1)) if p1 else None,
        })

if not entries:
    print("❌ No valid entries found.")
    sys.exit(1)

print(f"\n📊 Training Log Detailed Analysis")
print(f"- Entries analyzed: {len(entries)}\n")

prev = None
for i, e in enumerate(entries, 1):
    trend = ""
    if prev:
        dpacc = e["pacc1"] - prev["pacc1"]
        dpacc_pct = (dpacc / prev["pacc1"]) * 100 if prev["pacc1"] != 0 else 0
        dloss = e["loss"] - prev["loss"]
        dloss_pct = (dloss / prev["loss"]) * 100 if prev["loss"] != 0 else 0
        trend += f"Δpacc1={dpacc:+.4f} ({dpacc_pct:+.2f}%), Δloss={dloss:+.4f} ({dloss_pct:+.2f}%)"
    print(f"Entry {i:02d} | Samples={e['samples']:.0f} | pacc1={e['pacc1']:.4f} | "
          f"loss={e['loss']:.4f} | p0loss={e['p0loss']:.4f} | p1loss={e['p1loss']:.4f} {trend}")
    prev = e
