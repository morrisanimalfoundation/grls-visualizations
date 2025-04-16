import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

main_dir = Path(sys.argv[1])
feature_dir = Path(sys.argv[2])
diff_dir = Path(sys.argv[3])
diff_dir.mkdir(parents=True, exist_ok=True)

def compare_images(main_img_path, feature_img_path, diff_img_path, threshold=5.0):
    img1 = Image.open(main_img_path).convert("RGB")
    img2 = Image.open(feature_img_path).convert("RGB")

    diff = ImageChops.difference(img1, img2)
    stat = ImageStat.Stat(diff)
    rms = sum([v**2 for v in stat.rms]) ** 0.5

    if rms > threshold:
        print(f"❌ {main_img_path.name} changed — RMS diff = {rms:.2f}")
        diff.save(diff_img_path)
        return False
    else:
        print(f"✅ {main_img_path.name} passed — RMS diff = {rms:.2f}")
        return True

all_passed = True

for img_main in main_dir.glob("*.png"):
    img_feature = feature_dir / img_main.name
    if not img_feature.exists():
        print(f"⚠️ Missing {img_main.name} in feature branch.")
        continue

    diff_img = diff_dir / f"diff_{img_main.name}"
    passed = compare_images(img_main, img_feature, diff_img)
    if not passed:
        all_passed = False

if not all_passed:
    sys.exit("One or more plot images differ beyond threshold.")

