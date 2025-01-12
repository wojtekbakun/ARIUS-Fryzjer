from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Payment, User
from backend.extensions import db
from datetime import datetime
from backend.faktury.send_invoice import send_invoice_to_customer

# Tworzenie Blueprint dla zarządzania płatnościami i fakturami
payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/payment", methods=["POST"])
@jwt_required()
def create_payment():
    """
    Tworzy nową płatność wraz z danymi faktury.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika

    # Pobieranie szczegółów usług z żądania
    services_details = data.get("services_details", [])  # Lista szczegółów usług
    total_cost = sum(service["price"] for service in services_details)  # Obliczenie całkowitego kosztu

    # Tworzenie nowego obiektu Payment z danymi z żądania
    new_payment = Payment(
        user_id=user_id,  # ID użytkownika dokonującego płatności
        amount=total_cost,  # Kwota płatności
        status="pending",  # Status płatności, domyślnie "pending"
        invoice_name=data.get("invoice_name", f"Invoice-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),  # Nazwa faktury
        invoice_sent=data.get("invoice_sent", False),  # Czy faktura została wysłana
        services_details=json.dumps(services_details),  # Szczegóły usług w formacie JSON
        total_cost=total_cost,  # Całkowity koszt usług
        invoice_date=datetime.utcnow()  # Data utworzenia faktury
    )
    db.session.add(new_payment)  # Dodanie nowej płatności do sesji
    db.session.commit()  # Zapisanie zmian w bazie danych

    # Zwrócenie odpowiedzi z komunikatem o sukcesie i ID płatności
    return jsonify({
        "message": "Payment and invoice created successfully",
        "payment_id": new_payment.id
    }), 201


@payment_bp.route("/invoice-data", methods=["GET"])
@jwt_required()
def invoice_data():
    """
    Pobiera dane użytkownika do faktury.
    """
    auth_user_email = get_jwt_identity()  # Pobranie emaila zalogowanego użytkownika
    user = User.query.filter_by(email=auth_user_email).first()  # Wyszukanie użytkownika po emailu
    
    if not user:
        # Zwrócenie błędu, jeśli użytkownik nie został znaleziony
        return jsonify({"error": "User not found"}), 404

    # Przygotowanie danych faktury na podstawie danych użytkownika
    invoice_data = {
        "id": user.id,
        "email": user.email,
        "street": user.street,
        "street_number": user.street_number,
        "postal_code": user.postal_code,
        "city": user.city,
        "nip": user.nip,
        "company_name": user.company_name,
        "purchase_date": user.created_at.strftime("%Y-%m-%d")  # Data zakupu
    }

    # Zwrócenie danych faktury jako odpowiedź JSON
    return jsonify(invoice_data), 200


@payment_bp.route("/invoice-data", methods=["POST"])
@jwt_required()
def update_invoice_data():
    """
    Aktualizuje dane użytkownika potrzebne do faktury.
    """
    auth_user_email = get_jwt_identity()  # Pobranie emaila zalogowanego użytkownika
    user = User.query.filter_by(email=auth_user_email).first()  # Wyszukanie użytkownika po emailu
    
    if not user:
        # Zwrócenie błędu, jeśli użytkownik nie został znaleziony
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()  # Pobranie danych z żądania JSON

    # Aktualizacja danych użytkownika na podstawie danych z żądania
    user.street = data.get("street", user.street)  # Aktualizacja ulicy
    user.street_number = data.get("street_number", user.street_number)  # Aktualizacja numeru ulicy
    user.postal_code = data.get("postal_code", user.postal_code)  # Aktualizacja kodu pocztowego
    user.city = data.get("city", user.city)  # Aktualizacja miejscowości
    user.nip = data.get("nip", user.nip)  # Aktualizacja NIP
    user.company_name = data.get("company_name", user.company_name)  # Aktualizacja nazwy firmy/instytucji

    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Invoice data updated successfully"}), 200  # Zwrócenie komunikatu o sukcesie


@payment_bp.route("/invoice", methods=["GET"])
@jwt_required()
def get_invoices():
    """
    Pobiera wszystkie faktury użytkownika.
    """
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika
    payments = Payment.query.filter_by(user_id=user_id).all()  # Pobranie wszystkich płatności użytkownika
    
    invoices = []
    for payment in payments:
        # Tworzenie słownika z danymi faktury
        invoices.append({
            "payment_id": payment.id,
            "invoice_name": payment.invoice_name,
            "invoice_date": payment.invoice_date.strftime("%Y-%m-%d %H:%M:%S") if payment.invoice_date else None,  # Data faktury
            "services_details": json.loads(payment.services_details) if payment.services_details else [],  # Szczegóły usług
            "total_cost": payment.total_cost,  # Całkowity koszt
            "invoice_sent": payment.invoice_sent,  # Czy faktura została wysłana
            "status": payment.status  # Status płatności
        })

    # Zwrócenie listy faktur jako odpowiedź JSON
    return jsonify(invoices), 200


@payment_bp.route("/send-invoice/<int:payment_id>", methods=["POST"])
@jwt_required()
def send_invoice_endpoint(payment_id):
    """
    Wysyła fakturę do użytkownika na podstawie ID płatności.
    """
    user_email = get_jwt_identity()  # Pobranie emaila zalogowanego użytkownika
    print(f"User email from token: {user_email}")  # Logowanie emaila użytkownika

    user = User.query.filter_by(email=user_email).first()  # Wyszukanie użytkownika po emailu
    if not user:
        print("User not found.")  # Logowanie błędu
        return jsonify({"error": "User not found."}), 404

    payment = Payment.query.filter_by(id=payment_id).first()  # Wyszukanie płatności po ID
    if not payment:
        print("Payment not found.")  # Logowanie błędu
        return jsonify({"error": "Payment not found."}), 404

    try:
        print(f"Calling send_invoice_to_customer for email: {user.email}")  # Logowanie wywołania funkcji wysyłającej fakturę
        send_invoice_to_customer(user_email=user.email)  # Wywołanie funkcji wysyłającej fakturę

        payment.invoice_sent = True  # Aktualizacja statusu faktury na wysłaną
        db.session.commit()  # Zapisanie zmian w bazie danych

        return jsonify({"message": "Invoice sent successfully"}), 200  # Zwrócenie komunikatu o sukcesie
    except Exception as e:
        print(f"Error in endpoint: {e}")  # Logowanie błędu
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # Zwrócenie błędu serwera
