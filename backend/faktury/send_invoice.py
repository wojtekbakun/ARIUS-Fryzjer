import os
import smtplib
from email.message import EmailMessage
from backend.faktury.faktury import generate_invoice, get_next_invoice_number

def send_invoice_to_customer(user_email):
    print(f"Sending invoice to {user_email}...")
    try:
        # Krok 1: Generowanie faktury
        invoice_number = get_next_invoice_number()
        print(f"Generating invoice with number: {invoice_number}")
        generate_invoice()

        # Krok 2: Lokalizacja wygenerowanej faktury
        invoice_filename = f"invoice_{invoice_number}.pdf"
        invoice_path = os.path.join('./backend/faktury/invoices', invoice_filename)

        if not os.path.exists(invoice_path):
            print(f"Invoice file not found at: {invoice_path}")
            return {"error": "Invoice file not found"}

        # Krok 3: Przygotowanie emaila
        sender_email = 'ariusz@buziaczek.pl'  # Twój email nadawcy
        sender_password = 'Ariuszek123A'  # Hasło do Twojego emaila
        subject = 'Faktura od Fryzjerski Sp. z o.o.'  # Temat emaila
        body = 'Faktura jest dołączona do wiadomości. Dziękujemy za współpracę.'  # Treść emaila

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = user_email
        msg.set_content(body)

        # Dołączenie faktury PDF
        with open(invoice_path, 'rb') as file:
            file_data = file.read()
            file_name = os.path.basename(invoice_path)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        # Krok 4: Wysłanie emaila
        print(f"Sending email to {user_email} from {sender_email}")
        with smtplib.SMTP_SSL('smtp.poczta.onet.pl', 465) as server:
            server.login(sender_email, sender_password)  # Logowanie do serwera SMTP
            server.send_message(msg)  # Wysłanie wiadomości email
        
        print(f"Invoice sent successfully to {user_email}")
        return {"message": "Invoice sent successfully"}

    except smtplib.SMTPAuthenticationError:
        print("SMTP authentication failed. Please check your email and password.")  # Błąd uwierzytelnienia SMTP
        return {"error": "SMTP authentication failed"}

    except Exception as e:
        print(f"Error occurred while sending invoice: {e}")  # Ogólny błąd podczas wysyłania faktury
        return {"error": str(e)}
