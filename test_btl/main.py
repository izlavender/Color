import cv2
import pandas as pd

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Thiết lập độ phân giải
cap.set(3, 720)  # chiều rộng
cap.set(4, 1280)  # chiều cao

b = g = r = 0  # Khởi tạo giá trị màu BGR


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


# Đọc tệp CSV bằng pandas và đặt tên cho từng cột
index = ["mau", "ten_mau", "hex", "R", "G", "B"]
csv = pd.read_csv("colors.csv", names=index, header=None)


# Hàm lấy giá trị BGR từ camera
def layBGR(x, y):
    global b, g, r
    b, g, r = img[y, x]
    b, g, r = int(b), int(g), int(r)
    return b, g, r


# Hàm tính khoảng cách nhỏ nhất để lấy tên màu phù hợp nhất
def layTenMau(b, g, r):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(b - int(csv.loc[i, "B"])) + abs(g - int(csv.loc[i, "G"])) + abs(r - int(csv.loc[i, "R"]))
        if (d <= minimum):
            minimum = d
            ten_mau = csv.loc[i, "ten_mau"]
    return ten_mau


# Hiển thị tên và mã màu lên ảnh
def hienThiText(img, x, y):
    cv2.rectangle(img, (x - 150, y - 220), (x + 300, y - 170), (b, g, r), -1)
    text = layTenMau(b, g, r) + " | R=" + str(r) + " G=" + str(g) + " B=" + str(b)
    cv2.putText(img, text, (x - 140, y - 190), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)  # Lật ảnh để giống gương
    x, y = int(img.shape[1] / 2), int(img.shape[0] / 2)
    layBGR(x, y)
    layTenMau(b, g, r)
    veHinhVuong(img, x, y)
    hienThiText(img, x, y)
    cv2.imshow('Trình phát hiện màu', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
