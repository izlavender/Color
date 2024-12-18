import cv2
import pandas as pd
import numpy as np
from scipy.spatial import KDTree

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Thiết lập độ phân giải
cap.set(3, 720)  # Chiều rộng
cap.set(4, 1280)  # Chiều cao

h = s = v = 0  # Khởi tạo giá trị màu HSV

# Đọc tệp CSV và xây dựng KDTree
index = ["mau", "ten_mau", "hex", "H", "S", "V"]
try:
    csv = pd.read_csv("sampled_colors_with_names.csv", names=index, header=0)
    csv["HSV"] = list(zip(csv["H"], csv["S"], csv["V"]))
    kd_tree = KDTree(csv["HSV"].tolist())
except FileNotFoundError:
    print("Không tìm thấy file CSV!")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Hàm vẽ hình vuông xung quanh điểm trung tâm
def veHinhVuong(img, x, y):
    VANG = (0, 255, 255)
    XANH_DUONG = (255, 225, 0)
    cv2.line(img, (x - 150, y - 150), (x - 100, y - 150), VANG, 2)
    cv2.line(img, (x - 150, y - 150), (x - 150, y - 100), XANH_DUONG, 2)
    cv2.line(img, (x + 150, y - 150), (x + 100, y - 150), VANG, 2)
    cv2.line(img, (x + 150, y - 150), (x + 150, y - 100), XANH_DUONG, 2)
    cv2.line(img, (x + 150, y + 150), (x + 100, y + 150), VANG, 2)
    cv2.line(img, (x + 150, y + 150), (x + 150, y + 100), XANH_DUONG, 2)
    cv2.line(img, (x - 150, y + 150), (x - 100, y + 150), VANG, 2)
    cv2.line(img, (x - 150, y + 150), (x - 150, y + 100), XANH_DUONG, 2)
    cv2.circle(img, (x, y), 5, (255, 255, 153), -1)

# Hàm lấy giá trị HSV từ camera
def layHSV(x, y):
    global h, s, v
    bgr_color = img[y, x]
    hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)
    h, s, v = hsv_color[0][0]
    return h, s, v

# Hàm tìm tên màu gần nhất
def layTenMau(h, s, v):
    dist, index = kd_tree.query((h, s, v))
    return csv.loc[index, "ten_mau"]

# Hiển thị tên và mã màu lên ảnh
def hienThiText(img, x, y):
    bgr_color = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
    b, g, r = int(bgr_color[0]), int(bgr_color[1]), int(bgr_color[2])
    cv2.rectangle(img, (x - 150, y - 220), (x + 300, y - 170), (b, g, r), -1)
    text = layTenMau(h, s, v) + f" | H={h} S={s} V={v}"
    cv2.putText(img, text, (x - 140, y - 190), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

frame_count = 0
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)  # Lật ảnh để giống gương
    x, y = int(img.shape[1] / 2), int(img.shape[0] / 2)

    # Cập nhật mỗi 10 khung hình để giảm lag
    if frame_count % 10 == 0:
        layHSV(x, y)
    frame_count += 1

    veHinhVuong(img, x, y)
    hienThiText(img, x, y)
    cv2.imshow('Trình phát hiện màu', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
