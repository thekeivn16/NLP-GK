import json
import os
import re


def parse_rec(rec_file):
    mapping = {}
    
    with open(rec_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t', 1)
            if len(parts) < 2:
                continue
            
            img_path = parts[0]
            text_content = parts[1]
            filename = os.path.basename(img_path) 
            
            match = re.match(r'(\d+)_crop_(\d+)\.jpg', filename)
            if match:
                page_id = match.group(1)
                crop_idx = int(match.group(2))
                
                if page_id not in mapping:
                    mapping[page_id] = {}
                
                mapping[page_id][crop_idx] = text_content
    
    return mapping


def update_label_with_final_path(label_path, output_path, mapping_data):
    updated_lines = []
    
    with open(label_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 2:
                parts = line.split(' ', 1)
            
            if len(parts) < 2:
                continue
            
            old_img_path = parts[0]  
            json_str = parts[-1]
            
            try:
                data = json.loads(json_str)
                filename = os.path.basename(old_img_path)  
                page_id = os.path.splitext(filename)[0]
                
                if page_id in mapping_data:
                    page_map = mapping_data[page_id]
                    
                    for i, item in enumerate(data):
                        if i in page_map:
                            item['transcription'] = page_map[i]
                
                new_img_path = f"final/{filename}"
                new_json_str = json.dumps(data, ensure_ascii=False)
                updated_lines.append(f"{new_img_path}\t{new_json_str}")
                
            except json.JSONDecodeError:
                filename = os.path.basename(old_img_path)
                new_img_path = f"final/{filename}"
                updated_lines.append(f"{new_img_path}\t{json_str}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in updated_lines:
            f.write(line + '\n')


if __name__ == "__main__":
    final_rec_file = 'rec_gt_corrected.txt'
    label_file = 'Label.txt'
    output_file = 'Label_final.txt'
    
    mapping = parse_rec(final_rec_file)
    update_label_with_final_path(label_file, output_file, mapping)
