You can convert any infomration to QR Code by following code

import qrcode
import image

qr = qrcode.QRCode(
    version=15,
    box_size=10,     # Size of the box where QR code will be displayed
    border=5    # It is the white part of the image -- border in all 4 sides with white color
)

# Inside data put the information
data = "Emrul Hasan Emon"
# Any thing can be putted inside the quotation

qr.add_data(data)
qr.make(fit=True)
qr_image = qr.make_image(fill="black", black_color="white")
qr_image.save("test.png")

print("Emrul")
