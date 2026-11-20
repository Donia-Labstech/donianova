#!/usr/bin/env python3
"""Repo mode: build the site from _src and merge it into the repo root (the deployed folder).
Usage (from anywhere):  python3 _src/publish.py
- validates guides_extra.json, builds into _build/, requires 0 missing French strings,
- copies the build over the repo root, never overwriting promos.json (owned by the campaign agent)
  and never deleting anything."""
import os, sys, subprocess, shutil, json
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC); BUILD = os.path.join(ROOT, "_build")
r = subprocess.run([sys.executable, os.path.join(SRC, "check_guides.py")])
if r.returncode: sys.exit("❌ guide validation failed — fix guides_extra.json")
shutil.rmtree(BUILD, ignore_errors=True)
r = subprocess.run([sys.executable, os.path.join(SRC, "build.py")], env=dict(os.environ, DN_OUT=BUILD))
if r.returncode: sys.exit("❌ build failed")
miss = json.load(open(os.path.join(SRC, "fr_missing.json"), encoding="utf-8"))
if miss:
    print("❌ French translations missing (add them to _src/fr_dict.json, English -> French):")
    for m in miss: print("  ", json.dumps(m, ensure_ascii=False))
    shutil.rmtree(BUILD, ignore_errors=True); sys.exit(1)
for dirpath, _, files in os.walk(BUILD):
    rel = os.path.relpath(dirpath, BUILD); dst = os.path.join(ROOT, rel) if rel != "." else ROOT
    os.makedirs(dst, exist_ok=True)
    for f in files:
        if rel == "." and f == "promos.json" and os.path.exists(os.path.join(ROOT, f)): continue
        shutil.copy2(os.path.join(dirpath, f), os.path.join(dst, f))
shutil.rmtree(BUILD, ignore_errors=True)
print("✅ site rebuilt into repo root")
