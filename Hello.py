from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def create_hotel_bill(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Register the DejaVu Sans font
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))  # Ensure the path to the font is correct
    c.setFont("DejaVu", 16)

    # Title
    c.drawString(100, height - 50, "RajVeer Hotel")
    
    # Address
    c.setFont("DejaVu", 12)
    c.drawString(100, height - 70, "Swargate, near bus stand, Pune")
    
    # Order Details
    c.setFont("DejaVu", 12)
    c.drawString(100, height - 100, "Order: #520580")
    c.drawString(100, height - 120, "Table: Dinning - 4")
    c.drawString(100, height - 140, "Type: Dine-in")
    c.drawString(100, height - 160, "DateTime: 20-Jan-2025 03:57 PM")
    
    # Items Header
    c.setFont("DejaVu", 12)
    c.drawString(100, height - 200, "Item")
    c.drawString(300, height - 200, "Qty")
    c.drawString(350, height - 200, "Rate")
    c.drawString(450, height - 200, "Amt")
    
    # Item details
    items = [
        ("Tea", 1, 20.00, 20.00),
        ("Jira Rice", 1, 100.00, 100.00),
        ("Paneer Butter Masala", 1, 400.00, 400.00),
        ("Butter Nan", 1, 30.00, 30.00),
        ("Jira Rice", 1, 80.00, 80.00),
        ("Jira Rice", 1, 100.00, 100.00),
    ]
    
    y_position = height - 220
    for item in items:
        c.setFont("DejaVu", 12)
        c.drawString(100, y_position, item[0])
        c.drawString(300, y_position, str(item[1]))
        c.drawString(350, y_position, f"₹ {item[2]:.2f}")  # Using ₹ symbol
        c.drawString(450, y_position, f"₹ {item[3]:.2f}")  # Using ₹ symbol
        y_position -= 20
    
    # Subtotal, Discount, Service Charges, GST, Total
    c.setFont("DejaVu", 12)
    c.drawString(100, y_position, "Subtotal:")
    c.drawString(450, y_position, "₹ 730.00")  # Using ₹ symbol
    y_position -= 20
    
    c.drawString(100, y_position, "Discount (9.32%):")
    c.drawString(450, y_position, "- ₹ 68.00")  # Using ₹ symbol
    y_position -= 20
    
    c.drawString(100, y_position, "Service Charges (2%):")
    c.drawString(450, y_position, "+ ₹ 13.24")  # Using ₹ symbol
    y_position -= 20
    
    c.drawString(100, y_position, "GST (5%):")
    c.drawString(450, y_position, "+ ₹ 33.10")  # Using ₹ symbol
    y_position -= 20
    
    c.drawString(100, y_position, "Total:")
    c.drawString(450, y_position, "₹ 708.34")  # Using ₹ symbol
    
    
       # Add upi image
    upi_image_path = "/home/shekru/Documents/login/login/upi.jpeg"
    c.drawImage(upi_image_path, 40, y_position - 120, width=500, height=75)
     
    # Add QR code image
    qr_image_path = "/home/shekru/Documents/login/login/Qr.jpeg"
    c.drawImage(qr_image_path, 270, y_position - 265, width=100, height=100)
    
    # Payment Link
    c.setFont("DejaVu", 12)
    c.drawString(255, y_position - 280, "Scan to Pay")
    c.drawString(330, y_position - 280, "₹ 708.34")  # Using ₹ symbol
    c.drawString(255, y_position - 300, "https://menumitra.com")
    
    # Save the PDF
    c.save()

# Create the PDF bill
create_hotel_bill("Rajveer_Hotel_Billno.pdf")
