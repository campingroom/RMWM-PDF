import streamlit as st
import fitz  # PyMuPDF
import io
import hashlib
import zipfile
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="PDF Logo Remover Pro", layout="centered", page_icon="📄")

# --- TRANSLATIONS ---
translations = {
    "en": {
        "title": "📄 PDF Watermark & Logo Remover Pro",
        "subtitle": "Remove watermarks and logos from single or multiple PDFs. Supports image detection, manual drawing, and text search.",
        "upload": "Upload PDF file(s)",
        "method_label": "Select Removal Method:",
        "method_manual": "Manual Area Selection (Draw a Box)",
        "method_auto": "Smart Auto-Detect (Images & Text)",
        "method_text": "Text Watermark Search",
        "step1_auto": "Scan Results",
        "step1_auto_desc": "These are the image objects found on the **first page** of your first document.",
        "no_images": "No distinct image objects were found on the first page.",
        "select_remove": "Select the logos/watermarks you want to remove:",
        "remove_obj": "Remove Object {i}",
        "cannot_preview": "Cannot preview Object {i}",
        "step2": "Processing Options",
        "upload_replacement": "Upload Replacement Logo (Optional)",
        "process_btn": "Process Document(s)",
        "processing": "Processing pages...",
        "success": "Processing complete!",
        "download": "Download Result",
        "step1_manual": "Define Area to Remove",
        "step1_manual_desc": "Click and drag on the image below to draw a box over the watermark you want to remove. You can draw multiple boxes!",
        "step1_text": "Step 1: Text Search",
        "step1_text_desc": "Enter the exact text of the watermark you want to erase (e.g. 'CONFIDENTIAL').",
        "text_input_label": "Watermark Text",
        "wipe_btn": "Wipe Area(s)",
        "lang_toggle": "🇹🇭 เปลี่ยนเป็นภาษาไทย",
        "page_range": "Pages to Process (e.g. 1-3, 5). Leave blank for all pages:",
        "fill_color": "Pick a fill color (defaults to White):",
        "preview_header": "Live Preview (First Processed Page)",
        "text_preview_header": "First Page Preview (To identify text)",
        "suspect_text": "Found large suspect text:",
        "header_text": "Found Header Text (Top Margin):",
        "footer_text": "Found Footer Text (Bottom Margin):",
        "suspect_image": "Found images/backgrounds:",
        "is_bg": "⚠️ BACKGROUND"
    },
    "th": {
        "title": "📄 โปรแกรมลบลายน้ำและโลโก้ PDF (Pro)",
        "subtitle": "ลบลายน้ำและโลโก้ออกจาก PDF รองรับการทำทีละหลายไฟล์ (Batch) มีทั้งโหมดสแกนรูปภาพ วาดกรอบ และค้นหาตัวอักษร",
        "upload": "อัปโหลดไฟล์ PDF (เลือกได้หลายไฟล์)",
        "method_label": "เลือกวิธีการลบ:",
        "method_manual": "เลือกพื้นที่ลบเอง (วาดกรอบ)",
        "method_auto": "สแกนอัจฉริยะ (รูปภาพ & ข้อความใหญ่)",
        "method_text": "ค้นหาจากตัวอักษร",
        "step1_auto": "ผลการสแกน",
        "step1_auto_desc": "นี่คือรูปภาพที่พบใน **หน้าแรก** ของเอกสารฉบับแรกของคุณ",
        "no_images": "ไม่พบรูปภาพที่สามารถแยกลบได้ในหน้าแรก",
        "select_remove": "เลือกโลโก้/ลายน้ำที่คุณต้องการลบ:",
        "remove_obj": "ลบรูปที่ {i}",
        "cannot_preview": "ไม่สามารถดูตัวอย่างรูปที่ {i}",
        "step2": "ตัวเลือกการประมวลผล",
        "upload_replacement": "อัปโหลดโลโก้ใหม่เพื่อวางทับ (ไม่จำเป็น)",
        "process_btn": "เริ่มประมวลผลเอกสาร",
        "processing": "กำลังประมวลผล...",
        "success": "ประมวลผลเสร็จสิ้น!",
        "download": "ดาวน์โหลดไฟล์ที่แก้ไขแล้ว",
        "step1_manual": "กำหนดพื้นที่ที่จะลบ",
        "step1_manual_desc": "คลิกแล้วลากเมาส์บนรูปด้านล่าง เพื่อวาดกรอบสี่เหลี่ยมครอบลายน้ำที่คุณต้องการลบออก (วาดกี่กรอบก็ได้)",
        "step1_text": "ขั้นตอนที่ 1: ค้นหาด้วยตัวอักษร",
        "step1_text_desc": "พิมพ์ข้อความลายน้ำที่คุณต้องการลบให้ตรงเป๊ะๆ (เช่น 'CONFIDENTIAL')",
        "text_input_label": "ข้อความลายน้ำ",
        "wipe_btn": "เริ่มลบพื้นที่",
        "lang_toggle": "🇬🇧 Switch to English",
        "page_range": "หน้าที่จะประมวลผล (เช่น 1-3, 5) หากปล่อยว่างจะทำทุกหน้า:",
        "fill_color": "เลือกสีที่จะถม (ค่าเริ่มต้นคือสีขาว):",
        "preview_header": "ภาพตัวอย่างผลลัพธ์ (หน้าแรกที่ถูกประมวลผล)",
        "text_preview_header": "ภาพตัวอย่างหน้าแรก (เพื่อดูข้อความลายน้ำ)",
        "suspect_text": "ข้อความลายน้ำขนาดใหญ่ที่ตรวจพบ:",
        "header_text": "หัวกระดาษที่ตรวจพบ (ขอบบน):",
        "footer_text": "ท้ายกระดาษที่ตรวจพบ (ขอบล่าง):",
        "suspect_image": "รูปภาพหรือพื้นหลังที่ตรวจพบ:",
        "is_bg": "⚠️ ภาพพื้นหลัง"
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = 'th'

def toggle_lang():
    st.session_state.lang = 'en' if st.session_state.lang == 'th' else 'th'

t = translations[st.session_state.lang]

# --- UTILS ---
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def parse_page_ranges(range_str, total_pages):
    if not range_str.strip():
        return list(range(total_pages))
    
    pages = set()
    parts = range_str.split(",")
    for part in parts:
        part = part.strip()
        if not part: continue
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                start_idx = max(0, int(start.strip()) - 1)
                end_idx = min(total_pages - 1, int(end.strip()) - 1)
                if start_idx <= end_idx:
                    pages.update(range(start_idx, end_idx + 1))
            except ValueError:
                pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < total_pages:
                    pages.add(idx)
            except ValueError:
                pass
    return sorted(list(pages))

import statistics

def get_smart_suspects_from_page(doc, page_num=0):
    page = doc.load_page(page_num)
    page_area = page.rect.width * page.rect.height
    page_height = page.rect.height
    
    # 1. Analyze Text
    text_dict = page.get_text("dict")
    font_sizes = []
    text_spans = []
    
    header_texts = set()
    footer_texts = set()
    
    for block in text_dict.get("blocks", []):
        if block.get("type") == 0: # text block
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)
                    bbox = span.get("bbox", (0, 0, 0, 0))
                    if text and size > 0:
                        font_sizes.append(size)
                        text_spans.append({"text": text, "size": size})
                        
                        y0, y1 = bbox[1], bbox[3]
                        if y1 < (page_height * 0.12):
                            header_texts.add(text)
                        elif y0 > (page_height * 0.88):
                            footer_texts.add(text)
                        
    suspect_texts = set()
    if font_sizes:
        median_size = statistics.median(font_sizes)
        # Threshold for abnormally large text (e.g., > 2.0x median)
        threshold = median_size * 2.0
        for span in text_spans:
            if span["size"] > threshold:
                suspect_texts.add(span["text"])
                
    # 2. Analyze Images
    image_list = page.get_images(full=True)
    images = []
    seen_hashes = set()
    for img_index, img in enumerate(image_list):
        xref = img[0]
        try:
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            bbox = page.get_image_bbox(img)
            img_hash = hashlib.md5(image_bytes).hexdigest()
            
            if img_hash not in seen_hashes:
                seen_hashes.add(img_hash)
                
                # Check if it's a background (e.g., area > 50% of page)
                bbox_area = (bbox.x1 - bbox.x0) * (bbox.y1 - bbox.y0)
                is_background = bbox_area > (page_area * 0.5)
                
                images.append({
                    "xref": xref,
                    "bytes": image_bytes,
                    "ext": image_ext,
                    "bbox": bbox,
                    "hash": img_hash,
                    "is_background": is_background
                })
        except Exception:
            pass
            
    return sorted(list(suspect_texts)), sorted(list(header_texts)), sorted(list(footer_texts)), images

# --- PROCESSING FUNCTIONS ---
def process_pdf_smart(doc, pages_to_process, target_hashes, target_texts, target_header_texts, target_footer_texts, fill_color, replacement_logo_bytes=None):
    for page_num in pages_to_process:
        page = doc.load_page(page_num)
        page_height = page.rect.height
        
        # 1. Remove Images
        if target_hashes:
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_hash = hashlib.md5(image_bytes).hexdigest()
                    if img_hash in target_hashes:
                        bbox = page.get_image_bbox(img)
                        shape = page.new_shape()
                        shape.draw_rect(bbox)
                        shape.finish(color=fill_color, fill=fill_color)
                        shape.commit()
                        if replacement_logo_bytes:
                            rect = fitz.Rect(bbox)
                            page.insert_image(rect, stream=replacement_logo_bytes)
                except Exception:
                    pass
                    
        # 2. Remove Text
        for text_query in target_texts:
            text_instances = page.search_for(text_query, quads=True)
            for quad in text_instances:
                shape = page.new_shape()
                shape.draw_quad(quad)
                shape.finish(color=fill_color, fill=fill_color)
                shape.commit()
                if replacement_logo_bytes:
                    page.insert_image(quad.rect, stream=replacement_logo_bytes)
                    
        # 3. Remove Header Text (Zoned)
        for text_query in target_header_texts:
            text_instances = page.search_for(text_query, quads=True)
            for quad in text_instances:
                if quad.ul.y < (page_height * 0.12):
                    shape = page.new_shape()
                    shape.draw_quad(quad)
                    shape.finish(color=fill_color, fill=fill_color)
                    shape.commit()
                    if replacement_logo_bytes:
                        page.insert_image(quad.rect, stream=replacement_logo_bytes)
                        
        # 4. Remove Footer Text (Zoned)
        for text_query in target_footer_texts:
            text_instances = page.search_for(text_query, quads=True)
            for quad in text_instances:
                if quad.ll.y > (page_height * 0.88):
                    shape = page.new_shape()
                    shape.draw_quad(quad)
                    shape.finish(color=fill_color, fill=fill_color)
                    shape.commit()
                    if replacement_logo_bytes:
                        page.insert_image(quad.rect, stream=replacement_logo_bytes)
                        
    return doc

def process_pdf_by_area(doc, pages_to_process, rects, fill_color, replacement_logo_bytes=None):
    for page_num in pages_to_process:
        page = doc.load_page(page_num)
        for rect in rects:
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=fill_color, fill=fill_color)
            shape.commit()
            if replacement_logo_bytes:
                page.insert_image(rect, stream=replacement_logo_bytes)
    return doc

def process_pdf_by_text(doc, pages_to_process, text_query, fill_color, replacement_logo_bytes=None):
    for page_num in pages_to_process:
        page = doc.load_page(page_num)
        text_instances = page.search_for(text_query, quads=True)
        for quad in text_instances:
            shape = page.new_shape()
            shape.draw_quad(quad)
            shape.finish(color=fill_color, fill=fill_color)
            shape.commit()
            if replacement_logo_bytes:
                page.insert_image(quad.rect, stream=replacement_logo_bytes)
    return doc

# --- BATCH RUNNER ---
def run_batch_process(uploaded_files, page_range_str, process_func, *args):
    # Returns (download_data, download_filename, mime_type, preview_img_bytes)
    preview_img_bytes = None
    
    if len(uploaded_files) == 1:
        file_bytes = uploaded_files[0].getvalue()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        total_pages = len(doc)
        pages_to_process = parse_page_ranges(page_range_str, total_pages)
        doc = process_func(doc, pages_to_process, *args)
        
        if pages_to_process:
            pix = doc.load_page(pages_to_process[0]).get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            preview_img_bytes = pix.tobytes("png")
            
        return doc.write(), f"cleaned_{uploaded_files[0].name}", "application/pdf", preview_img_bytes
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, file in enumerate(uploaded_files):
                file_bytes = file.getvalue()
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                total_pages = len(doc)
                pages_to_process = parse_page_ranges(page_range_str, total_pages)
                doc = process_func(doc, pages_to_process, *args)
                zip_file.writestr(f"cleaned_{file.name}", doc.write())
                
                if i == 0 and pages_to_process:
                    pix = doc.load_page(pages_to_process[0]).get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                    preview_img_bytes = pix.tobytes("png")
                    
        return zip_buffer.getvalue(), "cleaned_documents.zip", "application/zip", preview_img_bytes

# --- UI MAIN ---
with st.sidebar:
    st.button(t["lang_toggle"], on_click=toggle_lang, use_container_width=True)
    st.title(t["title"])
    st.write(t["subtitle"])
    
    st.divider()
    uploaded_files = st.file_uploader(t["upload"], type=['pdf'], accept_multiple_files=True)
    
    if uploaded_files:
        st.divider()
        mode = st.radio(t["method_label"], [t["method_manual"], t["method_auto"]])
        
        # Auto-detect background color
        try:
            first_doc_bytes_sidebar = uploaded_files[0].getvalue()
            first_doc_sidebar = fitz.open(stream=first_doc_bytes_sidebar, filetype="pdf")
            page_0 = first_doc_sidebar.load_page(0)
            pix_sidebar = page_0.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
            bg_r, bg_g, bg_b = pix_sidebar.pixel(5, 5)[:3]
            default_hex = f"#{bg_r:02x}{bg_g:02x}{bg_b:02x}".upper()
        except Exception:
            default_hex = "#FFFFFF"
            
        st.divider()
        st.header(t["step2"])
        page_range_str = st.text_input(t["page_range"], placeholder="e.g. 1-5, 8")
        
        st.caption(f"✨ Auto-detected background: {default_hex}")
        hex_color = st.color_picker(t["fill_color"], default_hex)
        replacement_img = st.file_uploader(t["upload_replacement"], type=['png', 'jpg', 'jpeg'], key="rep_logo")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>built by campingroom —</p>", unsafe_allow_html=True)

if not uploaded_files:
    st.info("👈 Please upload a PDF file from the sidebar to get started. / กรุณาอัปโหลดไฟล์ PDF จากเมนูด้านซ้ายเพื่อเริ่มต้นใช้งาน")
else:
    first_doc_bytes = uploaded_files[0].getvalue()
    first_doc = fitz.open(stream=first_doc_bytes, filetype="pdf")
    
    fill_color_rgb = hex_to_rgb(hex_color)
    rep_bytes = replacement_img.read() if replacement_img else None
    
    if mode == t["method_auto"]:
        st.header(t["step1_auto"])
        st.write(t["step1_auto_desc"])
        suspect_texts, header_texts, footer_texts, images = get_smart_suspects_from_page(first_doc, page_num=0)
        
        selected_texts = []
        selected_headers = []
        selected_footers = []
        selected_hashes = []
        
        if not suspect_texts and not header_texts and not footer_texts and not images:
            st.info(t["no_images"])
        else:
            if suspect_texts:
                st.write(f"**{t['suspect_text']}**")
                for text_val in suspect_texts:
                    if st.checkbox(f"\"{text_val}\"", key=f"txt_{text_val}"):
                        selected_texts.append(text_val)
                st.divider()
                
            if header_texts:
                st.write(f"**{t['header_text']}**")
                for text_val in header_texts:
                    if st.checkbox(f"\"{text_val}\"", key=f"hdr_{text_val}"):
                        selected_headers.append(text_val)
                st.divider()
                
            if footer_texts:
                st.write(f"**{t['footer_text']}**")
                for text_val in footer_texts:
                    if st.checkbox(f"\"{text_val}\"", key=f"ftr_{text_val}"):
                        selected_footers.append(text_val)
                st.divider()
                
            if images:
                st.write(f"**{t['suspect_image']}**")
                cols = st.columns(min(len(images), 4))
                for i, img_data in enumerate(images):
                    col = cols[i % 4]
                    with col:
                        try:
                            img_obj = Image.open(io.BytesIO(img_data["bytes"]))
                            cap = f"Object {i+1} {t['is_bg'] if img_data['is_background'] else ''}"
                            st.image(img_obj, caption=cap, use_container_width=True)
                            if st.checkbox(t["remove_obj"].format(i=i+1), key=f"remove_{img_data['hash']}"):
                                selected_hashes.append(img_data["hash"])
                        except Exception:
                            st.error(t["cannot_preview"].format(i=i+1))
                            
            if (selected_texts or selected_headers or selected_footers or selected_hashes) and st.button(t["process_btn"], type="primary"):
                with st.spinner(t["processing"]):
                    data, fname, mime, preview = run_batch_process(uploaded_files, page_range_str, process_pdf_smart, set(selected_hashes), set(selected_texts), set(selected_headers), set(selected_footers), fill_color_rgb, rep_bytes)
                    st.success(t["success"])
                    st.download_button(label=t["download"], data=data, file_name=fname, mime=mime)
                    if preview:
                        st.write(f"### {t['preview_header']}")
                        st.image(preview, use_container_width=True)
                        
    else: # Manual Area
        st.header(t["step1_manual"])
        st.write(t["step1_manual_desc"])
        
        page = first_doc.load_page(0)
        mat = fitz.Matrix(1.0, 1.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Prevent Streamlit Cloud from garbage collecting the image URL
        st.session_state["_canvas_bg_image"] = img
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)", # Translucent red fill
            stroke_width=2,
            stroke_color="#FF0000", # Red stroke
            background_image=st.session_state["_canvas_bg_image"],
            update_streamlit=True,
            height=img.height,
            width=img.width,
            drawing_mode="rect",
            key="canvas",
        )
        
        rects = []
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            for obj in objects:
                if obj["type"] == "rect":
                    left = obj["left"]
                    top = obj["top"]
                    width = obj["width"] * obj["scaleX"]
                    height = obj["height"] * obj["scaleY"]
                    rects.append(fitz.Rect(left, top, left + width, top + height))
                    
        if len(rects) == 0:
            st.info("👆 Please draw at least one rectangle on the image above.")
        else:
            st.success(f"Selected {len(rects)} area(s) to remove.")
            if st.button(t["wipe_btn"], type="primary"):
                with st.spinner(t["processing"]):
                    data, fname, mime, preview = run_batch_process(uploaded_files, page_range_str, process_pdf_by_area, rects, fill_color_rgb, rep_bytes)
                    st.success(t["success"])
                    st.download_button(label=t["download"], data=data, file_name=fname, mime=mime)
                    if preview:
                        st.write(f"### {t['preview_header']}")
                        st.image(preview, use_container_width=True)
