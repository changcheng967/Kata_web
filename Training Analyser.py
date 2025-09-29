import sys
import re

# Regex patterns
pacc1_re = re.compile(r"pacc1 = ([0-9.]+)")
loss_re = re.compile(r"qscloss = [0-9.]+, loss = ([0-9.]+)")
p0loss_re = re.compile(r"p0loss = ([0-9.]+)")
p1loss_re = re.compile(r"p1loss = ([0-9.]+)")
nsamp_re = re.compile(r"nsamp = ([0-9.]+)")

print("Paste logs below, then press CTRL+D (Linux/Mac) or CTRL+Z + Enter (Windows):\n")
text = sys.stdin.read()

entries = []
for line in text.splitlines():
    nsamp = nsamp_re.search(line)
    pacc1 = pacc1_re.search(line)
    loss = loss_re.search(line)
    p0 = p0loss_re.search(line)
    p1 = p1loss_re.search(line)

    if nsamp and pacc1 and loss:
        entries.append({
            "samples": float(nsamp.group(1)),
            "pacc1": float(pacc1.group(1)),
            "loss": float(loss.group(1)),
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
        dloss = e["loss"] - prev["loss"]
        trend += f"Δpacc1={dpacc:+.4f}, Δloss={dloss:+.4f}"
    print(f"Entry {i:02d} | Samples={e['samples']:.0f} | pacc1={e['pacc1']:.4f} | "
          f"loss={e['loss']:.4f} | p0loss={e['p0loss']:.4f} | p1loss={e['p1loss']:.4f} {trend}")
    prev = e
