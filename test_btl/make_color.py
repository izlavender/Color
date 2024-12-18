import csv
import colorsys
import webcolors

# Hàm tính khoảng cách màu giữa 2 màu RGB
def color_distance(rgb1, rgb2):
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2))

# Danh sách các màu CSS3 với tên và mã hex
CSS3_COLORS = {
    "aliceblue": "#F0F8FF", "antiquewhite": "#FAEBD7", "aqua": "#00FFFF", "aquamarine": "#7FFFD4", "azure": "#F0FFFF",
    "beige": "#F5F5DC", "bisque": "#FFE4C4", "black": "#000000", "blanchedalmond": "#FFEBCD", "blue": "#0000FF",
    "blueviolet": "#8A2BE2", "brown": "#A52A2A", "burlywood": "#DEB887", "cadetblue": "#5F9EA0", "chartreuse": "#7FFF00",
    "chocolate": "#D2691E", "coral": "#FF7F50", "cornflowerblue": "#6495ED", "cornsilk": "#FFF8DC", "crimson": "#DC143C",
    "cyan": "#00FFFF", "darkblue": "#00008B", "darkcyan": "#008B8B", "darkgoldenrod": "#B8860B", "darkgray": "#A9A9A9",
    "darkgreen": "#006400", "darkkhaki": "#BDB76B", "darkmagenta": "#8B008B", "darkolivegreen": "#556B2F", "darkorange": "#FF8C00",
    "darkorchid": "#9932CC", "darkred": "#8B0000", "darksalmon": "#E9967A", "darkseagreen": "#8FBC8F", "darkslateblue": "#483D8B",
    "darkslategray": "#2F4F4F", "darkturquoise": "#00CED1", "darkviolet": "#9400D3", "deeppink": "#FF1493", "deepskyblue": "#00BFFF",
    "dimgray": "#696969", "dodgerblue": "#1E90FF", "firebrick": "#B22222", "floralwhite": "#FFFAF0", "forestgreen": "#228B22",
    "fuchsia": "#FF00FF", "gainsboro": "#DCDCDC", "ghostwhite": "#F8F8FF", "gold": "#FFD700", "goldenrod": "#DAA520",
    "gray": "#808080", "green": "#008000", "greenyellow": "#ADFF2F", "honeydew": "#F0FFF0", "hotpink": "#FF69B4",
    "indianred": "#CD5C5C", "indigo": "#4B0082", "ivory": "#FFFFF0", "khaki": "#F0E68C", "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5", "lawngreen": "#7CFC00", "lemonchiffon": "#FFFACD", "lightblue": "#ADD8E6", "lightcoral": "#F08080",
    "lightcyan": "#E0FFFF", "lightgoldenrodyellow": "#FAFAD2", "lightgray": "#D3D3D3", "lightgreen": "#90EE90", "lightpink": "#FFB6C1",
    "lightsalmon": "#FFA07A", "lightseagreen": "#20B2AA", "lightskyblue": "#87CEFA", "lightslategray": "#778899", "lightsteelblue": "#B0C4DE",
    "lightyellow": "#FFFFE0", "lime": "#00FF00", "limegreen": "#32CD32", "linen": "#FAF0E6", "magenta": "#FF00FF",
    "maroon": "#800000", "mediumaquamarine": "#66CDAA", "mediumblue": "#0000CD", "mediumorchid": "#BA55D3", "mediumpurple": "#9370DB",
    "mediumseagreen": "#3CB371", "mediumslateblue": "#7B68EE", "mediumspringgreen": "#00FA9A", "mediumturquoise": "#48D1CC", "mediumvioletred": "#C71585",
    "midnightblue": "#191970", "mintcream": "#F5FFFA", "mistyrose": "#FFE4E1", "moccasin": "#FFE4B5", "navajowhite": "#FFDEAD",
    "navy": "#000080", "oldlace": "#FDF5E6", "olive": "#808000", "olivedrab": "#6B8E23", "orange": "#FFA500",
    "orangered": "#FF4500", "orchid": "#DA70D6", "palegoldenrod": "#EEE8AA", "palegreen": "#98FB98", "paleturquoise": "#AFEEEE",
    "palevioletred": "#D87093", "papayawhip": "#FFEFD5", "peachpuff": "#FFDAB9", "peru": "#CD853F", "pink": "#FFC0CB",
    "plum": "#DDA0DD", "powderblue": "#B0E0E6", "purple": "#800080", "rebeccapurple": "#663399", "red": "#FF0000",
    "rosybrown": "#BC8F8F", "royalblue": "#4169E1", "saddlebrown": "#8B4513", "salmon": "#FA8072", "sandybrown": "#F4A460",
    "seashell": "#FFF5EE", "sienna": "#A0522D", "silver": "#C0C0C0", "skyblue": "#87CEEB", "slateblue": "#6A5ACD",
    "slategray": "#708090", "snow": "#FFFAFA", "springgreen": "#00FF7F", "steelblue": "#4682B4", "tan": "#D2B48C",
    "teal": "#008080", "thistle": "#D8BFD8", "tomato": "#FF6347", "turquoise": "#40E0D0", "violet": "#EE82EE",
    "wheat": "#F5DEB3", "white": "#FFFFFF", "whitesmoke": "#F5F5F5", "yellow": "#FFFF00", "yellowgreen": "#9ACD32"
}


# Hàm tìm tên màu gần nhất từ mã RGB
def get_nearest_color_name(r, g, b):
    try:
        # Cố gắng lấy tên chính xác nếu có
        color_name = webcolors.rgb_to_name((r, g, b))
    except ValueError:
        # Nếu không có tên chính xác, lấy tên màu gần nhất từ danh sách các màu CSS3
        min_distance = float('inf')
        color_name = None
        for name, hex_code in CSS3_COLORS.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_code)
            distance = color_distance((r, g, b), (r_c, g_c, b_c))
            if distance < min_distance:
                min_distance = distance
                color_name = name
    return color_name

# Đường dẫn để lưu file CSV
output_file = "sampled_colors_with_names.csv"

# Khai báo khoảng lấy mẫu (mỗi 10 cho H, mỗi 5 cho S và V)
hue_range = range(0, 360, 10)
saturation_range = range(0, 101, 5)
value_range = range(0, 101, 5)

# Mở file và ghi dữ liệu vào CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["mau", "ten_mau", "hex", "H", "S", "V"])

    # Biến đếm cho màu
    color_id = 1

    # Duyệt qua từng giá trị lấy mẫu cho H, S, và V
    for h in hue_range:
        for s in saturation_range:
            for v in value_range:
                # Chuyển đổi từ HSV sang RGB (giá trị trong khoảng [0, 1])
                r, g, b = colorsys.hsv_to_rgb(h / 360.0, s / 100.0, v / 100.0)

                # Chuyển đổi RGB từ [0, 1] sang [0, 255]
                r, g, b = int(r * 255), int(g * 255), int(b * 255)

                # Tạo mã hex
                hex_color = f"#{r:02X}{g:02X}{b:02X}"

                # Lấy tên màu gần nhất
                color_name = get_nearest_color_name(r, g, b)

                # Ghi thông tin màu vào file CSV
                writer.writerow([color_id, color_name, hex_color, h, s, v])
                color_id += 1

print(f"File {output_file} đã được tạo thành công với tên màu gần nhất từ không gian HSV!")
