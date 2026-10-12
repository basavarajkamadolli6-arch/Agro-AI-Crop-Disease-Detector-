
import os
import zipfile

zip_path = (
    r"C:\Users\admin\.cache\huggingface\hub\datasets--mohanty--PlantVillage"
    r"\snapshots\9e97599868962bd0079b8db4b7f1efa9185fa1e7\data.zip"
)
output_dir = r"C:\AgroAI\dataset"

os.makedirs(output_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as archive:
    entries = archive.infolist()
    total = len(entries)

    for i, info in enumerate(entries, 1):
        target = os.path.join(output_dir, info.filename)

        if info.is_dir():
            os.makedirs(target, exist_ok=True)
            continue

        if os.path.isfile(target) and os.path.getsize(target) == info.file_size:
            continue

        os.makedirs(os.path.dirname(target), exist_ok=True)

        with archive.open(info) as source, open(target, "wb") as destination:
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                destination.write(chunk)

        if i % 100 == 0 or i == total:
            print(f"Processed {i}/{total} entries", flush=True)

print("EXTRACTION FINISHED:", output_dir)
