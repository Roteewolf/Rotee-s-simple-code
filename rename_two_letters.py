import os
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}

def gen_labels():
    for a in range(ord('a'), ord('z')+1):
        for b in range(ord('a'), ord('z')+1):
            yield chr(a) + chr(b)

def rename_images(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("❌ 경로가 존재하지 않습니다.")
        return

    # 하위 폴더 무시
    imgs = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMG_EXTS
    ]

    if not imgs:
        print("⚠️ 변환할 이미지가 없습니다.")
        return

    imgs.sort(key=lambda x: (x.stat().st_mtime, x.name))  # 시간→이름 순

    labels = gen_labels()
    max_labels = 26 * 26

    if len(imgs) > max_labels:
        print(f"❌ 파일 {len(imgs)}개 > 최대 {max_labels}개 (aa~zz)")
        return

    # 1) 임시 이름
    temp_files = []
    for img in imgs:
        tmp = img.with_name(f".__tmp_{img.name}")
        os.replace(img, tmp)
        temp_files.append(tmp)

    # 2) 최종 이름
    for tmp, lab in zip(temp_files, labels):
        new_name = tmp.with_name(lab + tmp.suffix.lower())
        os.replace(tmp, new_name)

    print(f"✅ 총 {len(imgs)}개 파일 → aa, ab, ac… 로 변경 완료!")


if __name__ == "__main__":
    folder = input("📁 폴더 경로를 입력하세요: ").strip()
    rename_images(folder)
