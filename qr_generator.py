import qrcode

# Replace with your actual URL
session_id = "AI(Artificial Intellegence)"
url = "http://192.168.6.14:5000"

img = qrcode.make(url)
img.save("qr_attendance.png")
print("QR Code saved as qr_attendance.png")
