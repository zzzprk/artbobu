import fitz  # PyMuPDF

pdf_path = "pdf/포트폴리오 정리중.pdf"
image_dir = "image"

# PDF 열기
pdf = fitz.open(pdf_path)

# 36페이지 (2016년 작품)
print("36페이지에서 이미지 추출 중...")
page_36 = pdf[35]
images_36 = page_36.get_images()

for img_index, img in enumerate(images_36):
    xref = img[0]
    pix = fitz.Pixmap(pdf, xref)

    # JPEG로 저장
    if pix.n - pix.alpha < 4:
        filename = f"{image_dir}/image_34_{img_index + 1}.jpg"
        pix.save(filename, "jpeg")
        print(f"  ✓ {filename}")
    else:
        pix = fitz.Pixmap(fitz.csRGB, pix)
        filename = f"{image_dir}/image_34_{img_index + 1}.jpg"
        pix.save(filename, "jpeg")
        print(f"  ✓ {filename}")

# 38페이지 (웰컴 투 PP)
print("\n38페이지에서 이미지 추출 중...")
page_38 = pdf[37]
images_38 = page_38.get_images()

for img_index, img in enumerate(images_38):
    xref = img[0]
    pix = fitz.Pixmap(pdf, xref)

    # JPEG로 저장
    if pix.n - pix.alpha < 4:
        filename = f"{image_dir}/image_30_{img_index + 1}.jpg"
        pix.save(filename, "jpeg")
        print(f"  ✓ {filename}")
    else:
        pix = fitz.Pixmap(fitz.csRGB, pix)
        filename = f"{image_dir}/image_30_{img_index + 1}.jpg"
        pix.save(filename, "jpeg")
        print(f"  ✓ {filename}")

pdf.close()
print("\n✅ 모든 이미지 추출 완료!")
