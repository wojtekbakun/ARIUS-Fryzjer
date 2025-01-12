import os
import smtplib
from email.message import EmailMessage
from backend.faktury.faktury import generate_invoice, get_next_invoice_number

def send_invoice_to_customer(user_email):
    print(f"Sending invoice to {user_email}...")
    try:
        # Step 1: Generate the invoice
        invoice_number = get_next_invoice_number()
        print(f"Generating invoice with number: {invoice_number}")
        generate_invoice()

        # Step 2: Locate the generated invoice
        invoice_filename = f"invoice_{invoice_number}.pdf"
        invoice_path = os.path.join('./backend/faktury/invoices', invoice_filename)

        if not os.path.exists(invoice_path):
            print(f"Invoice file not found at: {invoice_path}")
            return {"error": "Invoice file not found"}

        # Step 3: Prepare the email
        sender_email = 'ariusz@buziaczek.pl'  # Twój email nadawcy
        sender_password = 'Ariuszek123A'  # Hasło do Twojego emaila
        subject = 'Your Invoice from Twoja Firma Sp. z o.o.'
        body = 'Please find your invoice attached.'

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email
        msg.set_content(body)

        # Attach the PDF invoice
        with open(invoice_path, 'rb') as file:
            file_data = file.read()
            file_name = os.path.basename(invoice_path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        # Step 4: Send the email
        print(f"Sending email to {user_email} from {sender_email}")
        with smtplib.SMTP_SSL('smtp.poczta.onet.pl', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"Invoice sent successfully to {user_email}")
        return {"message": "Invoice sent successfully"}

    except smtplib.SMTPAuthenticationError:
        print("SMTP authentication failed. Please check your email and password.")
        return {"error": "SMTP authentication failed"}

    except Exception as e:
        print(f"Error occurred while sending invoice: {e}")
        return {"error": str(e)}