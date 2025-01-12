import os
import datetime
import uuid
from fpdf import FPDF
import requests

# Import danych firmy
from backend.faktury.company_data import COMPANY_DATA


def login_and_get_token():
    login_url = os.path.join(COMPANY_DATA.get('backend_url', ''), '/auth/login')
    payload = {
        "email": COMPANY_DATA.get('username'),
        "password": COMPANY_DATA.get('password')
    }
    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        token = response.json().get('token')
        if not token:
            print("Token JWT nie został otrzymany.")
            return None
        return token
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas logowania: {e}")
        return None

def get_client_data(token):
    invoice_data_url = os.path.join(COMPANY_DATA.get('backend_url', ''), 'payments/invoice-data')
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(invoice_data_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych klienta: {e}")
        return None

def get_services_data(token):
    services_url = os.path.join(COMPANY_DATA.get('backend_url', ''), 'appointments/services')
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(services_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania usług: {e}")
        return []

class InvoicePDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ścieżka do folderu z czcionkami
        fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')

        # Dodajemy czcionki DejaVu (obsługa polskich znaków)
        self.add_font('DejaVu', '', os.path.join(fonts_dir, 'DejaVuSans.ttf'), uni=True)
        self.add_font('DejaVu', 'B', os.path.join(fonts_dir, 'DejaVuSans-Bold.ttf'), uni=True)
        # Ustaw czcionkę domyślną
        self.set_font('DejaVu', '', 10)

        # Ustawienia strony
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):        
        # Logo prawego górnego rogu
        right_logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')  # Nowa ścieżka do prawego logo
        if os.path.exists(right_logo_path):
            # Pobierz szerokość strony
            page_width = self.w
            # Ustaw margines prawy (domyślnie 15 mm)
            right_margin = 15
            # Szerokość logo
            logo_width = 45
            # Oblicz pozycję x dla prawego logo
            x_position = page_width - right_margin - logo_width
            self.image(right_logo_path, x=x_position, y=8, w=45, h=15)  # Wstawiamy prawe logo

        self.set_y(10)
        self.set_x(30)
        self.set_font('DejaVu', 'B', 11)
        self.cell(0, 10, "Faktura VAT", ln=True, align='L')
        self.ln(5)

    def footer(self):
        # Stopka - numer strony
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f"Strona {self.page_no()} / {{nb}}", align='C')

def get_next_invoice_number(counter_file='invoice_counter.txt', invoices_dir='./backend/faktury/invoices'):
    """
    Pobiera następny numer faktury, inkrementuje licznik i zapisuje go.
    Numer jest 7-cyfrowy z wiodącymi zerami, np. 0000001.
    """
    # Upewnij się, że katalog invoices istnieje
    if not os.path.exists(invoices_dir):
        os.makedirs(invoices_dir)

    counter_path = os.path.join(invoices_dir, counter_file)

    # Jeśli plik z licznikiem nie istnieje, rozpocznij od 1
    if not os.path.exists(counter_path):
        current_number = 1
    else:
        with open(counter_path, 'r') as f:
            try:
                current_number = int(f.read().strip()) + 1
            except ValueError:
                current_number = 1  # W razie błędu resetuj licznik

    # Zapisz zaktualizowany licznik
    with open(counter_path, 'w') as f:
        f.write(str(current_number))

    # Zwroc numer faktury jako 7-cyfrowy string z wiodącymi zerami
    return f"{current_number:07d}"

def generate_invoice():
    # Tworzymy obiekt PDF
    pdf = InvoicePDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # -----------------------
    # BLOK 1: Dane faktury
    # -----------------------
    # Pobieramy dane sprzedawcy i klienta
    seller = COMPANY_DATA
    buyer = get_client_data()
    services = get_services_data()

    # Generujemy kolejny numer faktury
    invoice_number = get_next_invoice_number()

    # Daty: wystawienia, sprzedaży, płatności itp.
    date_of_issue = datetime.datetime.now().strftime("%Y-%m-%d")
    date_of_sale = (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d")
    payment_deadline = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")

    # Sekcja tytułowa (pozioma) - Sprzedawca & Nabywca & Dane Faktury
    pdf.set_font('DejaVu', '', 9)

    # Sprzedawca (lewa kolumna)
    pdf.set_y(25)
    pdf.set_x(10)
    pdf.multi_cell(80, 5,
        f"Sprzedawca:\n"
        f"{seller['nazwa']}\n"
        f"{seller['ulica']} {seller['nr_ulicy']}\n"
        f"{seller['kod_pocztowy']} {seller['miejscowosc']}\n"
        f"NIP: {seller['nip']}",
        border=0
    )

    # Nabywca (prawa kolumna)
    pdf.set_y(25)
    pdf.set_x(110)
    pdf.multi_cell(80, 5,
        f"Nabywca:\n"
        f"{buyer['nazwa']}\n"
        f"{buyer['ulica']} {buyer['nr_ulicy']}\n"
        f"{buyer['kod_pocztowy']} {buyer['miejscowosc']}\n"
        f"NIP: {buyer['nip']}",
        border=0,
        align="L"
    )

    # Informacje o fakturze (numer, daty)
    pdf.set_y(50)
    pdf.set_x(10)
    pdf.set_font('DejaVu', 'B', 10)
    pdf.cell(90, 6, f"Faktura nr: {invoice_number}", ln=1)
    pdf.set_font('DejaVu', '', 9)
    pdf.set_x(10)
    pdf.cell(90, 6, f"Data wystawienia: {date_of_issue}", ln=1)
    pdf.set_x(10)
    pdf.cell(90, 6, f"Data sprzedaży: {date_of_sale}", ln=1)

    # -----------------------
    # BLOK 2: Tabela z usługami
    # -----------------------
    # Nagłówki tabeli
    table_headers = [
        "Lp.", "Indeks", "Nazwa", "J.M.", "Ilość",
        "Cena netto", "Stawka VAT", "Wartość netto", "VAT", "Wartość brutto"
    ]
    col_widths = [10, 15, 45, 10, 10, 20, 20, 25, 15, 25]

    pdf.set_font('DejaVu', 'B', 7)  # Mniejszy rozmiar czcionki dla tabeli
    for header, w in zip(table_headers, col_widths):
        pdf.cell(w, 6, header, border=1, align='C')
    pdf.ln()

    # Wiersze tabeli
    pdf.set_font('DejaVu', '', 8)  # Mniejszy rozmiar czcionki dla danych w tabeli
    total_net = 0
    total_vat = 0
    total_gross = 0

    for i, srv in enumerate(services, start=1):
        # Obliczenia wartości
        net_value = srv["ilosc"] * srv["cena_netto"]
        vat_amount = round(net_value * srv["stawka_vat"] / 100.0, 2)
        gross_value = net_value + vat_amount

        total_net += net_value
        total_vat += vat_amount
        total_gross += gross_value

        # Generowanie wierszy tabeli
        pdf.cell(col_widths[0], 6, str(i), border=1, align='C')  # Lp.
        pdf.cell(col_widths[1], 6, srv["indeks"], border=1, align='C')  # Indeks
        pdf.cell(col_widths[2], 6, srv["nazwa"], border=1, align='L')  # Nazwa
        pdf.cell(col_widths[3], 6, srv["jm"], border=1, align='C')  # J.M.
        pdf.cell(col_widths[4], 6, str(srv["ilosc"]), border=1, align='C')  # Ilość
        pdf.cell(col_widths[5], 6, f"{srv['cena_netto']:.2f}", border=1, align='R')  # Cena netto
        pdf.cell(col_widths[6], 6, f"{srv['stawka_vat']}%", border=1, align='C')  # Stawka VAT
        pdf.cell(col_widths[7], 6, f"{net_value:.2f}", border=1, align='R')  # Wartość netto
        pdf.cell(col_widths[8], 6, f"{vat_amount:.2f}", border=1, align='R')  # VAT
        pdf.cell(col_widths[9], 6, f"{gross_value:.2f}", border=1, align='R')  # Wartość brutto
        pdf.ln()

    # -----------------------
    # BLOK 3: Podsumowanie
    # -----------------------
    pdf.ln(4)
    pdf.set_font('DejaVu', 'B', 10)
    pdf.cell(0, 5, "Podsumowanie", ln=1)

    pdf.set_font('DejaVu', '', 9)
    pdf.cell(0, 5, f"Razem netto: {total_net:.2f} zł", ln=1)
    pdf.cell(0, 5, f"Kwota VAT: {total_vat:.2f} zł", ln=1)
    pdf.cell(0, 5, f"Razem brutto: {total_gross:.2f} zł", ln=1)
    pdf.cell(0, 5, "Kwota zapłacona: 0.00 zł", ln=1)
    pdf.cell(0, 5, f"Pozostało do zapłaty: {total_gross:.2f} zł", ln=1)

    # -----------------------
    # BLOK 4: Uwagi
    # -----------------------
    pdf.ln(10)
    pdf.set_font('DejaVu', 'B', 8)
    pdf.multi_cell(0, 5, "Uwagi: ")

    # -----------------------
    # PODPISY
    # -----------------------
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 8)
    pdf.cell(90, 5, "..........................", align='C')
    pdf.cell(0, 5, "..........................", align='C', ln=1)
    pdf.cell(90, 5, "Podpis osoby wystawiającej", align='C')
    pdf.cell(0, 5, "Podpis osoby odbierającej", align='C')

    # Zapis do pliku w folderze 'invoices'
    invoices_dir = './backend/faktury/invoices'
    if not os.path.exists(invoices_dir):
        os.makedirs(invoices_dir)

    invoice_filename = f"invoice_{invoice_number}.pdf"
    invoice_path = os.path.join(invoices_dir, invoice_filename)
    pdf.output(invoice_path)
    print(f"Faktura została zapisana jako: {invoice_path}")

def main():
    generate_invoice()

if __name__ == "__main__":
    main()
