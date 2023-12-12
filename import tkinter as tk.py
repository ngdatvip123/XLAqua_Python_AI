import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Tạo một đối tượng Tkinter
win = tk.Tk()

# Đặt tiêu đề cho cửa sổ
win.title("Image Viewer")

# Đặt kích thước cửa sổ
win.geometry("800x400")

# Biến toàn cục lưu trữ ảnh gốc
original_image = None
processed_image = None

# Hàm để chọn ảnh từ thư mục và hiển thị
def select_image(self):
    global original_image, processed_image

    # Hiển thị hộp thoại để chọn tệp hình ảnh
    Img = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.png;*.jpeg"), ("All files", "*.*")))
    self.line_Edit.setText(Img[0])
    name =self.line_Edit.text()
    img1= cv2.imread(name)
    img2=cv2.Canny(img1,100,200)
    # Kiểm tra xem người dùng đã chọn ảnh hay chưa
    if Img:
        # Lưu trữ ảnh gốc
        original_image = Image.open(Img)

        # Chỉnh kích thước ảnh gốc
        resized_image = original_image.resize((300, 300))

        # Chuyển đổi ảnh gốc thành định dạng Tkinter PhotoImage
        original_photo = ImageTk.PhotoImage(resized_image)

        # Hiển thị ảnh gốc trong một nhãn (label)
        original_label.configure(image=original_photo)
        original_label.image = original_photo  # Lưu tham chiếu đến ảnh

        # Thực hiện xử lý ảnh và lưu trữ ảnh đã xử lý
        processed_image = process_image(original_image)

        # Chỉnh kích thước ảnh đã xử lý
        resized_processed_image = processed_image.resize((300, 300))

        # Chuyển đổi ảnh đã xử lý thành định dạng Tkinter PhotoImage
        processed_photo = ImageTk.PhotoImage(resized_processed_image)

        # Hiển thị ảnh đã xử lý trong một nhãn (label)
        processed_label.configure(image=processed_photo)
        processed_label.image = processed_photo  # Lưu tham chiếu đến ảnh

        # Kiểm tra hình ảnh đã được hiển thị thành công
        print("Image displayed successfully!")

from PIL import ImageOps
from PIL import ImageEnhance
from PIL import ImageFilter
import cv2
from PyQt5 import QtGui
# Hàm để xử lý ảnh (chức năng nâng cao chất lượng ảnh)
def process_image(self):
    
    name =self.line_Edit.text()
    img=cv2.imread(name)
    brightness = 7
    contrast = 2.3
        # call addWeighted function. use beta = 0 to effectively only operate one one image
    ouput = cv2.addWeighted( img, contrast, img, 0, brightness)
    self.image =ouput
        # khai bao kich thuoc anh
    dimensions = self.image.shape
    height = self.image.shape[0]
    width = self.image.shape[1]
    channels = self.image.shape[2]
        #height,width,channel= self.image.shape
    bytesPerLine = 3* width
        # chuyen doi hinh anh vc2 thanh pyqt5       
    self.image = QtGui.QImage(self.image.data, width, height, bytesPerLine,QtGui.QImage.Format_RGB888).rgbSwapped()
        #xuat len man hin
    self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))

from skimage.feature import hog
import numpy as np
# Hàm để rút trích đặc trưng HOG từ ảnh
def extract_hog_features(image):
    # Chuyển đổi ảnh thành dạng grayscale
    grayscale_image = image.convert("L")

    # Chuyển đổi ảnh thành mảng numpy
    image_array = np.array(grayscale_image)

    # Rút trích đặc trưng HOG
    feature, hog_image = hog(image_array, visualize=True)

    # Chuyển đổi ảnh HOG thành định dạng PIL Image
    hog_image_pil = Image.fromarray(hog_image.astype(np.uint8))

    return hog_image_pil

# Hàm để rút trích đặc trưng từ ảnh và hiển thị
def extract_features():
    global original_image, processed_image

    # Kiểm tra xem đã chọn ảnh hay chưa
    if original_image:
        # Rút trích đặc trưng HOG từ ảnh gốc
        hog_image = extract_hog_features(original_image)

        # Chỉnh kích thước ảnh HOG
        resized_hog_image = hog_image.resize((300, 300))

        # Chuyển đổi ảnh HOG thành định dạng Tkinter PhotoImage
        hog_photo = ImageTk.PhotoImage(resized_hog_image)

        # Hiển thị ảnh HOG trong một nhãn (label)
        processed_label.configure(image=hog_photo)
        processed_label.image = hog_photo  # Lưu tham chiếu đến ảnh

        # Kiểm tra rút trích đặc trưng đã thành công
        print("Features extracted successfully!")
# Tạo một nút (button) để lựa chọn ảnh
select_button = tk.Button(win, text="Select Image", command=select_image)
select_button.pack(side=tk.LEFT, padx=10, pady=10)

# Tạo một nhãn (label) để hiển thị ảnh gốc
original_label = tk.Label(win)
original_label.pack(side=tk.LEFT)

process_button = tk.Button(win, text="process_Image", command=process_image)
process_button.pack(side=tk.LEFT, padx=10, pady=10)

# Tạo một nhãn (label) để hiển thị ảnh gốc
original_label = tk.Label(win)
original_label.pack(side=tk.LEFT)
# Tạo một nhãn (label) để hiển thị ảnh đã xử lý
processed_label = tk.Label(win)
processed_label.pack(side=tk.LEFT)

extract_button = tk.Button(win, text="Extract Features", command=extract_features)
extract_button.pack(side=tk.LEFT, padx=10, pady=10)
# Chạy vòng lặp chính của ứng dụng
win.mainloop()
