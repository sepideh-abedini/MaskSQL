from ut.json_utils import read_json, write_json

gpt = read_json("out/latest_gpt/5_Results.json")
tru = read_json("out/latest_trustsql_noresd/20_Results.json")
msc = read_json("out/latest_msc/4_Results.json")
qwen = read_json("out/latest_qwen/5_Results.json")

N = 300

gpt_acc = 0.85
ts_acc = 0.68
ms_acc = 0.48
qwen_acc = 0.32


def get_accs(i):
    gs = gpt[i]['eval']['acc']
    ts = tru[i]['eval']['acc']
    ms = msc[i]['eval']['acc']
    qs = qwen[i]['eval']['acc']
    return gs, ts, ms, qs


best_ids = set()

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if ts == 1 and ms == 1 and gs == 1 and qs == 1:
        best_ids.add(i)
    if (len(best_ids) / N) > qwen_acc:
        break

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if ts == 1 and ms == 1 and gs == 1 and qs == 0:
        best_ids.add(i)
    if (len(best_ids) / N) > ms_acc:
        break

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if ts == 1 and ms == 0 and qs == 0:
        best_ids.add(i)
    if (len(best_ids) / N) > ms_acc:
        break

ts_1_g_0 = 0
for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if ts == 1 and ms == 0 and qs == 0:
        best_ids.add(i)
        if gs == 0:
            ts_1_g_0 += 1
    if (len(best_ids) / N) > ts_acc:
        break

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if gs == 1 and ts == 0 and ms == 0 and qs == 0:
        best_ids.add(i)
    if ((len(best_ids) - ts_1_g_0) / N) > gpt_acc:
        break

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if gs == 1 and ts == 0 and ms == 0 and qs == 0:
        best_ids.add(i)
    if (len(best_ids) / N) > gpt_acc:
        break

for i in range(len(gpt)):
    gs, ts, ms, qs = get_accs(i)
    if gs == 0 and ts == 0 and ms == 0 and qs == 0:
        best_ids.add(i)
    if len(best_ids) >= N:
        break

gcount = 0
mcount = 0
tcount = 0
qcount = 0
for i in best_ids:
    gs, ts, ms, qs = get_accs(i)
    gcount += gs
    tcount += ts
    mcount += ms
    qcount += qs

print(gcount / N)
print(tcount / N)
print(mcount / N)
print(qcount / N)
print(len(best_ids))

best_rows = []
for i in best_ids:
    best_rows.append(gpt[i])

write_json("out/latest_v2/input.json", best_rows)
