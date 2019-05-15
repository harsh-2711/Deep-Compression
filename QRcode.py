#############################
#### QR Code Generator ######
#############################

import qrcode
import cv2

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

f = open("am_decoded.txt","r")
lines = f.readlines()
s = ""
for line in lines:
	s = s + line
print(s)

f.close()

qr.add_data(s)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.show()