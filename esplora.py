#!/usr/bin/env python3
"""TEMPORANEO: secondo scarico indipendente (i link di riserva della pagina, tutte le colonne) per i test. Salva in esplora_out/."""
import json, os, time, urllib.request
OUT = "esplora_out"
os.makedirs(OUT, exist_ok=True)
for k, (nome, url) in enumerate(json.load(open("link_riserva.json")).items()):
    if k: time.sleep(13)
    for n in range(4):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.sdmx.data+csv;version=1.0.0, text/csv", "User-Agent": "Mozilla/5.0 (report-popolazione)"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = r.read()
            open(os.path.join(OUT, "scarico_" + nome), "wb").write(d)
            print(nome, len(d), flush=True)
            break
        except Exception as e:
            print(nome, "errore", e, flush=True); time.sleep(30)
