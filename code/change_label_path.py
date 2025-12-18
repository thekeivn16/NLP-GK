import re


def change_image_paths(input_file, output_file, new_folder):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = re.sub(r'[^/\s\t]+/(\d+\.jpg)', rf'{new_folder}/\1', content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)


if __name__ == "__main__":
    input_file = 'Label_raw.txt'
    output_file = 'Label.txt'
    new_folder = 'raw'
    
    change_image_paths(input_file, output_file, new_folder)
