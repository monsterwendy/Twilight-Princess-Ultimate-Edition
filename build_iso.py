#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

print("=== Twilight Princess Ultimate Edition ISO Build (Linux) ===")
print("⚠️  MAKE SURE YOU COMPLETED THE ORIGINAL BUILD INSTRUCTIONS FIRST ⚠️\n")

iso_input = input("Enter path to your GameCube USA ISO (GCN USA | 60Hz .iso): ").strip().strip('"')
iso_src = Path(iso_input).expanduser().resolve()

if not iso_src.exists():
    print(f"❌ ISO not found at '{iso_src}'. Exiting.")
    exit(1)

if not iso_src.is_file():
    print(f"❌ '{iso_src}' is not a file. Exiting.")
    exit(1)

orig_iso = Path("orig/GZ2E01/baserom.iso").resolve()
orig_iso.parent.mkdir(parents=True, exist_ok=True)

if iso_src == orig_iso:
    print(f"\n✓ ISO already at {orig_iso}, skipping copy.")
else:
    print(f"\nCopying ISO → {orig_iso}")
    shutil.copy2(iso_src, orig_iso)

print("\nRunning ninja build...\n")
build = subprocess.run(["ninja"])

if build.returncode != 0:
    print("❌ Compilation failed.")
    exit(1)

output_input = input("Enter output path + filename for your rebuilt ISO (example: /home/user/rebuilt_tp.iso): ").strip().strip('"')
output_iso = Path(output_input).expanduser().resolve()

if output_iso == orig_iso:
    print("❌ Output path cannot be the same as the input ISO. Choose a different path.")
    exit(1)

output_iso.parent.mkdir(parents=True, exist_ok=True)

print("\nBuilding 60FPS patched ISO...\n")

rebuild = subprocess.run([
    "python3",
    "tools/rebuild-decomp-tp.py",
    str(orig_iso),
    str(output_iso),
    str(Path().resolve()),
])

if rebuild.returncode != 0:
    print("❌ ISO build failed.")
    exit(1)

print("\n✅ ISO Build Complete!")
print(f"Modded ISO is ready at: {output_iso}")
