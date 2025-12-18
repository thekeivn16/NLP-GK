## Mô tả

Project này bao gồm các công cụ để:
1. Chuyển đổi PDF sang text
2. Thay đổi đường dẫn ảnh trong file label
3. Dóng hàng dựa trên văn bản gốc
4. Cập nhật label với text đã hiệu chỉnh

## Cài đặt

```bash
pip install PyMuPDF
```

## Cấu trúc file

```
.
├── alignment.py    # Dóng hàng dựa trên văn bản gốc
├── update_label_transcription.py          # Cập nhật label với text đã sửa
├── change_label_path.py      # Đổi đường dẫn ảnh trong label
├── pdf_to_text.py            # Chuyển PDF sang text
└── README.md
```

## Hướng dẫn sử dụng

### 1. Chuyển đổi PDF sang text (tùy chọn)

```bash
python pdf_to_text.py
```

**Input:**
- File PDF cần chuyển đổi (chỉnh sửa đường dẫn trong file)

**Output:**
- File text với nội dung từ PDF

**Cấu hình:**
- Mở file `pdf_to_text.py`
- Sửa `pdf_path` và `txt_path` theo đường dẫn mong muốn

### 2. Thay đổi đường dẫn ảnh

Chuẩn hóa đường dẫn ảnh trong file label:

```bash
python change_label_path.py
```

**Input:**
- `Label_raw.txt`: File label gốc với đường dẫn cần đổi

**Output:**
- `Label.txt`: File label với đường dẫn đã chuẩn hóa (vd: `raw/123.jpg`)

**Cấu hình:**
- `input_file`: File label đầu vào
- `output_file`: File label đầu ra
- `new_folder`: Tên thư mục mới cho ảnh

### 3. Dóng hàng dựa trên văn bản gốc

Sửa lỗi thiếu/sai dấu trong text OCR bằng cách so sánh với văn bản gốc:

```bash
python alignment.py
```

**Input:**
- `rec_gt.txt`: File chứa text OCR cần sửa (format: `đường/dẫn/ảnh\ttext`)
- `gt.txt`: File ground truth (text chuẩn có dấu đầy đủ)

**Output:**
- `rec_gt_corrected.txt`: File text đã được hiệu chỉnh dấu

**Lưu ý:**
- File `gt.txt` là text gốc đã được kiểm tra, có đầy đủ dấu thanh
- Script sử dụng thuật toán diff để tự động thêm dấu vào text OCR

### 4. Cập nhật label với text đã hiệu chỉnh

Thay thế text trong file label JSON bằng text đã sửa:

```bash
python update_label_transcription.py
```

**Input:**
- `rec_gt_corrected.txt`: Text đã hiệu chỉnh từ bước 3
- `Label.txt`: File label JSON cần cập nhật

**Output:**
- `Label_final.txt`: File label đã được cập nhật với text đúng

**Cấu hình:**
- `final_rec_file`: File text đã hiệu chỉnh
- `label_file`: File label cần cập nhật
- `output_file`: File label đầu ra

