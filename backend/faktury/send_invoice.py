import os
import smtplib
from email.message import EmailMessage
from faktury import generate_invoice, get_next_invoice_number

def send_invoice_to_customer(user_email):
    try:
        # Step 1: Generate the invoice
        invoice_number = get_next_invoice_number()
        generate_invoice()

        # Step 2: Locate the generated invoice
        invoice_filename = f"invoice_{invoice_number}.pdf"
        invoice_path = os.path.join('./backend/faktury/invoices', invoice_filename)

        if not os.path.exists(invoice_path):
            print("Invoice file not found.")
            return

        # Step 3: Prepare the email
        sender_email = 'ariusz@buziaczek.pl'
        sender_password = 'Ariuszek123A'
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
        with smtplib.SMTP_SSL('smtp.poczta.onet.pl', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print('Invoice sent successfully to', user_email)
    
    except Exception as e:
        print(f'Error occurred while sending invoice: {e}')


if __name__ == '__main__':
    send_invoice_to_customer('mikolajdrozdz1@gmail.com')