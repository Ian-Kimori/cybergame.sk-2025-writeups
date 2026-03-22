import fitz  # PyMuPDF

doc = fitz.open('recovered/f0003441_important.pdf')

for page_num, page in enumerate(doc, start=1):
    print(f"\n===== Page {page_num} =====")

    # Text
    text = page.get_text()
    print("Text:")
    print(text.strip()[:500], "...\n")  # Print first 500 chars

    # Images
    images = page.get_images(full=True)
    print(f"Images found: {len(images)}")
    for i, img in enumerate(images):
        xref = img[0]
        info = doc.extract_image(xref)
        image_bytes = info["image"]
        image_ext = info["ext"]
        image_filename = f"page{page_num}_img{i + 1}.{image_ext}"
        with open(image_filename, "wb") as f:
            f.write(image_bytes)
        print(f"  Image {i + 1}: {image_ext.upper()}, {len(image_bytes) // 1024} KB saved as {image_filename}")

    # Annotations
    annotations = list(page.annots() or [])
    print(f"Annotations found: {len(annotations)}")
    for i, annot in enumerate(annotations):
        print(f"  Annotation {i + 1}: type={annot.type[1]}, content={annot.info.get('content')}")

    # Fonts (via page.get_text("dict"))
    font_data = page.get_text("dict")["blocks"]
    fonts = set()
    for block in font_data:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                fonts.add((span["font"], span.get("size")))
    print("Fonts used on page:")
    for font_name, font_size in fonts:
        print(f"  {font_name}, size {font_size}")

    # Links
    links = page.get_links()
    print(f"Links found: {len(links)}")
    for link in links:
        print(f"  Link: {link.get('uri') or link.get('file')}")

    # Drawing objects
    drawings = page.get_drawings()
    print(f"Drawing objects found: {len(drawings)}")
    for d in drawings:
        print(f"  Type: {d['type']}, Color: {d.get('color')}, Rect: {d.get('rect')}, Items: {len(d.get('items', []))}")

    # Note: Drawing objects are vector instructions like lines, rectangles, curves, etc.
    # They cannot be 'extracted' like images, but you can analyze and reconstruct them based on the geometry.

doc.close()
