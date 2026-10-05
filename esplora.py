#!/usr/bin/env python3
"""TEMPORANEO: esplora ISTAT dai server di GitHub (da qui ISTAT risponde). Salva in esplora_out/."""
import json, os, time, urllib.request
B = "https://esploradati.istat.it/SDMXWS/rest/"
OUT = "esplora_out"
os.makedirs(OUT, exist_ok=True)
def get(url, nome, accept="application/vnd.sdmx.data+csv;version=1.0.0, text/csv"):
    for n in range(4):
        try:
            req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "Mozilla/5.0 (report-popolazione)"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = r.read()
            open(os.path.join(OUT, nome), "wb").write(d)
            print(nome, len(d), flush=True)
            return d
        except Exception as e:
            print(nome, "errore", e, flush=True); time.sleep(30)
    return None
d = get(B + "codelist/IT1/CL_ITTER107/1.0", "ITTER107.json", "application/json")
if d:
    cs = json.loads(d)["data"]["codelists"][0]["codes"]
    json.dump([(c["id"], c["names"].get("it")) for c in cs if c["id"].startswith(("ITC4", "IT10", "IT11")) or c["id"] in ("IT", "ITTOT")], open(os.path.join(OUT, "ITTER107_lombardia.json"), "w"), ensure_ascii=False, indent=1)
    os.remove(os.path.join(OUT, "ITTER107.json"))
time.sleep(13)
# tutte le aree, totale, 2025-2026: verifica dei codici delle province
get(B + "data/22_289_DF_DCIS_POPRES1_1/A..JAN.9.TOTAL.99?startPeriod=2025&endPeriod=2026&format=csvfile", "residenti_tutte_aree_2025_2026.csv")
time.sleep(13)
# ricostruzione 2018 (bilancio), Varese
get(B + "data/164_164_DF_DCIS_RICPOPRES2011_2/A.ITC41....?startPeriod=2018&endPeriod=2018&format=csvfile", "ric2_varese_2018.csv")
time.sleep(13)
# bilancio: tutti i tipi di dato di Varese
get(B + "data/22_315_DF_DCIS_POPORESBIL1_1/A.ITC41...?startPeriod=2019&endPeriod=2026&format=csvfile", "bilancio_varese_tutto.csv")
time.sleep(13)
# bilancio per Lombardia e Italia (per controlli)
get(B + "data/22_315_DF_DCIS_POPORESBIL1_1/A.ITC4+IT.NTGROW_REGOF+INTERTNMIG_REGOF+TOTAL_BAL.9?startPeriod=2019&endPeriod=2026&format=csvfile", "bilancio_lombardia_italia.csv")
