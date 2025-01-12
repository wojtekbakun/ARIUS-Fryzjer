from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Payment, User
from backend.extensions import db
from datetime import datetime

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/payment", methods=["POST"])
@jwt_required()
def create_payment():
    """
    Tworzy nową płatność wraz z danymi faktury.
    """
    data = request.get_json()
    user_id = get_jwt_identity()

    # Pobieranie szczegółów usług z żądania
    services_details = data.get("services_details", [])
    total_cost = sum(service["price"] for service in services_details)

    new_payment = Payment(
        user_id=user_id,
        amount=total_cost,
        status="pending",
        invoice_name=data.get("invoice_name", f"Invoice-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
        invoice_sent=data.get("invoice_sent", False),
        services_details=json.dumps(services_details),
        total_cost=total_cost,
        invoice_date=datetime.utcnow()
    )
    db.session.add(new_payment)
    db.session.commit()

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
    auth_user_email = get_jwt_identity()
    user = User.query.filter_by(email=auth_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    invoice_data = {
        "id": user.id,
        "email": user.email,
        "street": user.street,
        "street_number": user.street_number,
        "postal_code": user.postal_code,
        "city": user.city,
        "nip": user.nip,
        "company_name": user.company_name,
        "purchase_date": user.created_at.strftime("%Y-%m-%d")
    }

    return jsonify(invoice_data), 200


@payment_bp.route("/invoice-data", methods=["POST"])
@jwt_required()
def update_invoice_data():
    """
    Aktualizuje dane użytkownika potrzebne do faktury.
    """
    auth_user_email = get_jwt_identity()
    user = User.query.filter_by(email=auth_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.street = data.get("street", user.street)
    user.street_number = data.get("street_number", user.street_number)
    user.postal_code = data.get("postal_code", user.postal_code)
    user.city = data.get("city", user.city)
    user.nip = data.get("nip", user.nip)
    user.company_name = data.get("company_name", user.company_name)

    db.session.commit()
    return jsonify({"message": "Invoice data updated successfully"}), 200



@payment_bp.route("/invoice", methods=["GET"])
@jwt_required()
def get_invoices():
    """
    Pobiera wszystkie faktury użytkownika.
    """
    user_id = get_jwt_identity()
    payments = Payment.query.filter_by(user_id=user_id).all()
    
    invoices = []
    for payment in payments:
        invoices.append({
            "payment_id": payment.id,
            "invoice_name": payment.invoice_name,
            "invoice_date": payment.invoice_date.strftime("%Y-%m-%d %H:%M:%S") if payment.invoice_date else None,
            "services_details": json.loads(payment.services_details) if payment.services_details else [],
            "total_cost": payment.total_cost,
            "invoice_sent": payment.invoice_sent,
            "status": payment.status
        })

    return jsonify(invoices), 200