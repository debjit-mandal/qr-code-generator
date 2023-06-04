import qrcode

from PIL import Image, ImageDraw

def generate_qr_code(data, filename, size=10, color="black", background="white", logo_path=None, logo_size=30, logo_color=None, error_correction=qrcode.constants.ERROR_CORRECT_M, encoding=None, rounded_corners=False, corner_radius=10):

    try:

        qr = qrcode.QRCode(

            version=1,

            error_correction=error_correction,

            box_size=size,

            border=4,

        )

        if encoding:

            qr.add_data(data, encoding=encoding)

        else:

            qr.add_data(data)

        qr.make(fit=True)

        # Generate the QR code image

        qr_image = qr.make_image(fill_color=color, back_color=background)

        # Check if rounded corners are enabled

        if rounded_corners:

            qr_image = add_rounded_corners(qr_image, corner_radius)

        # Check if a logo is provided and embed it in the QR code

        if logo_path:

            logo_image = Image.open(logo_path).convert("RGBA")

            logo_image = logo_image.resize((logo_size, logo_size), Image.ANTIALIAS)

            if logo_color:

                logo_image = change_logo_color(logo_image, logo_color)

            qr_width, qr_height = qr_image.size

            logo_width, logo_height = logo_image.size

            logo_position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

            qr_image.paste(logo_image, logo_position, logo_image)

        # Save the QR code image

        qr_image.save(filename)

        # Display the generated QR code in the console

        qr_image.show()

        print("QR code generated successfully!")

    except Exception as e:

        print("An error occurred while generating the QR code:", str(e))

def add_rounded_corners(image, radius):

    mask = Image.new("L", image.size, 0)

    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)

    image.putalpha(mask)

    return image

def change_logo_color(logo_image, color):

    logo_data = logo_image.getdata()

    new_logo_data = []

    for item in logo_data:

        # Preserve alpha value

        if item[3] > 0:

            new_logo_data.append((color[0], color[1], color[2], item[3]))

        else:

            new_logo_data.append(item)

    logo_image.putdata(new_logo_data)

    return logo_image

# Example usage

data = input("Enter the data for the QR code: ")  # The data you want to encode in the QR code

filename = "qr_code.png"  # The filename to save the QR code image

size = 10  # The size of each box in the QR code (default is 10)

color = "black"  # The color of the QR code (default is black)

background = "white"  # The background color of the QR code (default is white)

logo_path = "logo.png"  # Path to the logo or image you want to embed in the QR code

logo_size = 50  # The size of the logo or image (default is 30)

logo_color = (255, 0, 0)  # The color for the embedded logo or image (default is None)

error_correction = qrcode.constants.ERROR_CORRECT_M  # Error correction level (default is medium)

encoding = None  # Encoding mode (default is None)

rounded_corners = True  # Enable rounded corners

corner_radius = 10  # Radius for rounded corners

generate_qr_code(data, filename, size, color, background, logo_path, logo_size, logo_color, error_correction, encoding, rounded_corners, corner_radius)

