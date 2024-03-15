# VŨ NHẬT QUANG_IT-E6_HUST
# vunhatquang2004@gmail.com
# Github: https://github.com/vnquang24
import requests
from tqdm import tqdm
import os
from PIL import Image

def convert_url(input_url):
    # Phân tích URL đầu vào và trích xuất các thông tin cần thiết
    parts = input_url.split('?')[1].split('&')
    params = {p.split('=')[0]: p.split('=')[1] for p in parts}
    doc = params['doc']
    subfolder = params['subfolder']
    # Tạo URL mới theo định dạng mong muốn
    new_url = f"https://repository.vnu.edu.vn/flowpaper/services/view.php?doc={doc}&format=jpg&page={{}}&subfolder={subfolder}/"
    return new_url

def download_images(base_url, total_pages, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for page in tqdm(range(1, total_pages + 1)):
        url = base_url.format(page)
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            with open(f"{save_dir}/page_{page}.jpg", "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download page {page}")
    print("Download completed.")

def create_pdf(save_dir, output_pdf):
    try:
        image_files = [os.path.join(save_dir, f) for f in os.listdir(save_dir) if f.endswith('.jpg')]
        image_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
        image_list = []
        for i, image_file in enumerate(image_files):
            if i == 0:
                img = Image.open(image_file)
                img = img.convert('RGB')
                continue
            img = Image.open(image_file)
            img = img.convert('RGB')
            image_list.append(img)
        img.save(output_pdf, save_all=True, append_images=image_list)
        print(f"PDF đã được tạo: {output_pdf}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tạo PDF: {e}")

def delete_downloaded_images(save_dir):
    for f in os.listdir(save_dir):
        os.remove(os.path.join(save_dir, f))
    print("Đã xoá tất cả các ảnh đã tải xuống.")

if __name__ == "__main__":
    input_url = input("Nhập URL cơ bản của tài liệu: ")
    base_url = convert_url(input_url)
    total_pages = int(input("Nhập tổng số trang: "))
    save_dir = "./downloaded_images"
    output_pdf = "tai_lieu_hoan_chinh.pdf"
    download_images(base_url, total_pages, save_dir)
    create_pdf(save_dir, output_pdf)
    delete_downloaded_images(save_dir)
