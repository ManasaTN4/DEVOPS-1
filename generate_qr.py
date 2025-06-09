import qrcode

# Change this to any session ID you want
session_id = "abc123"

# Your local link for QR
url = "http://192.168.6.14:5000"

# Generate QR code
qr = qrcode.make(url)

# Save it as an image
qr.save("session_qr.png")

print("QR code generated for session: {session_id}")
print("Scan this QR to visit: {url}")
