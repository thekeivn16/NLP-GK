import unicodedata
import difflib
import bisect
from typing import List


def norm_for_align(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    result = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return result.replace("đ", "d").replace("Đ", "D").lower()


def load_lines(path: str) -> List[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def align_rec_gt_fixed(rec_gt_path: str, gt_path: str, output_path: str):
    rec_lines = load_lines(rec_gt_path)
    gt_lines = load_lines(gt_path)
    
    rec_norm_parts = []
    line_offsets = [0] 
    current_offset = 0
    
    output_grid = [list(line) for line in rec_lines]

    for line in rec_lines:
        norm_line = norm_for_align(line)
        rec_norm_parts.append(norm_line)
        rec_norm_parts.append("\n")
        
        current_offset += len(norm_line) + 1
        line_offsets.append(current_offset)
        
    rec_flat_diff = "".join(rec_norm_parts)
    
    gt_full_nfc = "\n".join([unicodedata.normalize("NFC", l) for l in gt_lines]) + "\n"
    gt_flat_diff = "".join([norm_for_align(c) if c != '\n' else '\n' for c in gt_full_nfc])

    if len(gt_full_nfc) != len(gt_flat_diff):
        gt_flat_diff = norm_for_align(gt_full_nfc).replace("\n", "\n")

    sm = difflib.SequenceMatcher(None, rec_flat_diff, gt_flat_diff, autojunk=False)
    opcodes = sm.get_opcodes()

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            source_segment = gt_full_nfc[j1:j2]
            current_rec_idx = i1
            seg_cursor = 0
            
            while current_rec_idx < i2:
                line_idx = bisect.bisect_right(line_offsets, current_rec_idx) - 1
                line_start_flat = line_offsets[line_idx]
                local_char_start = current_rec_idx - line_start_flat
                line_end_flat = line_offsets[line_idx+1] - 1
                chunk_end = min(i2, line_end_flat)
                length = chunk_end - current_rec_idx
                
                if length > 0:
                    chunk_source = source_segment[seg_cursor : seg_cursor + length]
                    safe_len = min(length, len(output_grid[line_idx]) - local_char_start)
                    output_grid[line_idx][local_char_start : local_char_start + safe_len] = list(chunk_source[:safe_len])
                    current_rec_idx += length
                    seg_cursor += length
                
                if current_rec_idx == line_end_flat:
                    if current_rec_idx < i2:
                        current_rec_idx += 1
                        seg_cursor += 1
                    else:
                        break

    with open(output_path, "w", encoding="utf-8") as f:
        for char_list in output_grid:
            f.write("".join(char_list) + "\n")


if __name__ == "__main__":
    align_rec_gt_fixed("rec_gt.txt", "gt.txt", "rec_gt_corrected.txt")
