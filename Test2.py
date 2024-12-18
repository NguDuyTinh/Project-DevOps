import os

# Định nghĩa dấu hiệu của file JPG và PNG
JPG_SIGNATURE = b'\xFF\xD8'
JPG_END_SIGNATURE = b'\xFF\xD9'
PNG_SIGNATURE = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
PNG_END_SIGNATURE = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'

def is_valid_jpg(img_data):
    """Kiểm tra tính hợp lệ của file JPG dựa trên signature"""
    return img_data.startswith(JPG_SIGNATURE) and img_data.endswith(JPG_END_SIGNATURE)

def is_valid_png(img_data):
    """Kiểm tra tính hợp lệ của file PNG dựa trên signature"""
    return img_data.startswith(PNG_SIGNATURE) and img_data.endswith(PNG_END_SIGNATURE)

def extract_images_from_volume(volume_file_path, output_dir):
    try:
        # Biến lưu trữ các hình ảnh đã phục hồi
        recovered_images = []
        img_count = 0

        # Kiểm tra và tạo thư mục lưu trữ nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Đọc toàn bộ dữ liệu từ volume
        with open(volume_file_path, 'rb') as f:
            volume_data = f.read()

        img_start = 0
        while img_start < len(volume_data):
            # Tìm JPG
            jpg_start = volume_data.find(JPG_SIGNATURE, img_start)
            png_start = volume_data.find(PNG_SIGNATURE, img_start)

            # Tìm vị trí JPG hoặc PNG đầu tiên
            if jpg_start != -1 and (jpg_start < png_start or png_start == -1):
                img_end = volume_data.find(JPG_END_SIGNATURE, jpg_start) + 2
                if img_end != -1:
                    img_data = volume_data[jpg_start:img_end]
                    if is_valid_jpg(img_data):  # Kiểm tra tính hợp lệ của file JPG
                        with open(os.path.join(output_dir, f'recovered_image_{img_count}.jpg'), 'wb') as img_file:
                            img_file.write(img_data)
                        recovered_images.append(f'recovered_image_{img_count}.jpg')
                        print(f"Recovered JPG image {img_count}")
                        img_count += 1
                    else:
                        print(f"Invalid JPG image at {jpg_start}, skipping...")
                    img_start = img_end
                else:
                    img_start = jpg_start + len(JPG_SIGNATURE)
            elif png_start != -1:
                # Trích xuất file PNG
                img_end = volume_data.find(PNG_END_SIGNATURE, png_start) + len(PNG_END_SIGNATURE)
                if img_end != -1:
                    img_data = volume_data[png_start:img_end]
                    if is_valid_png(img_data):  # Kiểm tra tính hợp lệ của file PNG
                        with open(os.path.join(output_dir, f'recovered_image_{img_count}.png'), 'wb') as img_file:
                            img_file.write(img_data)
                        recovered_images.append(f'recovered_image_{img_count}.png')
                        print(f"Recovered PNG image {img_count}")
                        img_count += 1
                    else:
                        print(f"Invalid PNG image at {png_start}, skipping...")
                    img_start = img_end
                else:
                    img_start = png_start + len(PNG_SIGNATURE)
            else:
                break  # Nếu không tìm thấy dấu hiệu ảnh nữa thì thoát

        # Trả về danh sách các tệp đã phục hồi
        return recovered_images

    except Exception as e:
        print(f"Error: {e}")
        return []

# Ví dụ sử dụng
volume_file = "E:/image003.vol"  # Thay đổi đường dẫn tới file volume
output_dir = "C:/recovered_images1/"  # Đường dẫn tới thư mục lưu ảnh phục hồi

recovered_files = extract_images_from_volume(volume_file, output_dir)

# In ra các tệp đã phục hồi
if recovered_files:
    print("Recovered images:")
    for file in recovered_files:
        print(file)
else:
    print("No images found or could not recover images.")