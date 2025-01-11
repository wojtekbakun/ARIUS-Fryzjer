# Backend Flask z Dockerem

Ten projekt to backendowa aplikacja stworzona w Flasku, obsługująca funkcje związane z uwierzytelnianiem użytkowników, rezerwacjami oraz innymi usługami. Aplikacja została opakowana w kontenery przy użyciu Dockera, aby zapewnić łatwe wdrożenie.

---


## 🛠️ **Instalacja i uruchomienie**

Backend działa przy uruchomieniu z dockerem, jednak jezeli chcesz edytować pythonowe pliki to musisz pracować na wirtualnym środowisku.


### 1. Klonowanie repozytorium
Sklonuj projekt na swoją lokalną maszynę:
```
git clone https://github.com/wojtekbakun/ARIUS-Fryzjer
cd ARIUS-Fryzjer
```

### 2. Utworzenie i aktywacja wirtualnego środowiska
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```


### 3. Konfiguracja środowiska

Utwórz plik .env w katalogu głównym projektu i dodaj kluczowe zmienne środowiskowe:
```
SECRET_KEY=supersecretkey
JWT_SECRET_KEY=another_super_secret_key
DATABASE_URL=sqlite:///db.sqlite
```

### 4. Budowanie kontenerów
Zbuduj obrazy Dockera:
```
docker-compose build
```

### 5. Uruchomienie kontenerów

Uruchom aplikację w kontenerach:
```
docker-compose up
```

Aplikacja będzie dostępna pod adresem: http://localhost:8080.

## Migracje bazy danych

Aby zainicjalizować lub zaktualizować bazę danych, wykonaj następujące kroki:
### 1. Wykonaj migracje

Uruchom następujące komendy w venv:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
## Aktualne endpointy

| Metoda | Endpoint                                | Parametry (Body / Query)                                                                                                                                         | Zwraca                                                                                             |
|--------|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| **POST**   | `/auth/register`                         | Body:  
```json
{
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "street": "string",
  "street_number": "string",
  "postal_code": "string",
  "city": "string",
  "nip": "string",
  "company_name": "string"
}
```                                                                                                                                                         |  
```json
{
  "message": "User registered successfully"
}
```                                                                                           |
| **POST**   | `/auth/login`                            | Body:  
```json
{
  "email": "string",
  "password": "string"
}
```                                                                                                                                                                    |  
```json
{
  "token": "string",
  "email": "string"
}
```                                                                                           |
| **GET**    | `/user/profile`                          | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
{
  "id": "int",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "street": "string",
  "street_number": "string",
  "postal_code": "string",
  "city": "string",
  "nip": "string",
  "company_name": "string",
  "purchase_date": "YYYY-MM-DD"
}
```                                                                                                   |
| **POST**   | `/user/profile`                          | Nagłówek: `Authorization: Bearer <token>`  
Body:  
```json
{
  "first_name": "string",
  "last_name": "string",
  "street": "string",
  "street_number": "string",
  "postal_code": "string",
  "city": "string",
  "nip": "string",
  "company_name": "string"
}
```                                                                                                                                                     |  
```json
{
  "message": "Profile data updated successfully"
}
```                                                                                           |
| **GET**    | `/appointments/services`                 | Brak                                                                                                                                                                                                      |  
```json
[
  {
    "id": "int",
    "name": "string",
    "price": "float"
  },
  ...
]
```                                                                                                           |
| **POST**   | `/appointments/appointment`             | Body:  
```json
{
  "user_id": "int",
  "service_id": "int",
  "date": "YYYY-MM-DD HH:MM:SS"
}
```                                                                                                                                                                      |  
```json
{
  "message": "Appointment created successfully"
}
```                                                                                     |
| **GET**    | `/appointments`                        | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
[
  {
    "id": "int",
    "service": "int", 
    "date": "YYYY-MM-DD HH:MM:SS",
    "status": "string"
  },
  ...
]
```                                                                                                       |
| **PUT**    | `/appointments/appointment/<int:id>`    | Nagłówek: `Authorization: Bearer <token>`  
Body (opcjonalne pola do aktualizacji):  
```json
{
  "service_id": "int",
  "date": "YYYY-MM-DD HH:MM:SS",
  "status": "string"
}
```                                                                                                                                                     |  
```json
{
  "message": "Appointment updated successfully"
}
```                                                                                     |
| **DELETE** | `/appointments/appointment/<int:id>`     | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                              |  
```json
{
  "message": "Appointment deleted successfully"
}
```                                                                                           |
| **POST**   | `/reviews/review`                       | Body:  
```json
{
  "service_id": "int",
  "rating": "int",
  "comment": "string"
}
```                                                                                                                                                                    |  
```json
{
  "message": "Review submitted successfully"
}
```                                                                                     |
| **POST**   | `/payments/payment`                     | Body:  
```json
{
  "user_id": "int",
  "amount": "float"
}
```                                                                                                                                                                     |  
```json
{
  "message": "Payment created"
}
```                                                                                   |
| **GET**    | `/payments/invoice-data`                | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
{
  "id": "int",
  "email": "string",
  "street": "string",
  "street_number": "string",
  "postal_code": "string",
  "city": "string",
  "nip": "string",
  "company_name": "string",
  "purchase_date": "YYYY-MM-DD"
}
```                                                                                                   |
| **POST**   | `/payments/invoice-data`                | Nagłówek: `Authorization: Bearer <token>`  
Body:  
```json
{
  "street": "string",
  "street_number": "string",
  "postal_code": "string",
  "city": "string",
  "nip": "string",
  "company_name": "string"
}
```                                                                                                                                                     |  
```json
{
  "message": "Invoice data updated successfully"
}
```                                                                                           |
| **POST**   | `/employees/employee`                   | Body:  
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "service_ids": ["int", ...]  // (opcjonalnie, jeśli chcesz przypisywać usługi)
}
```                                                                                                                                                     |  
```json
{
  "message": "Employee created successfully"
}
```                                                                                   |
| **GET**    | `/employees`                            | Brak                                                                                                                                                                                                      |  
```json
[
  {
    "id": "int",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "services": [
      {
        "id": "int",
        "name": "string",
        "price": "float"
      }
    ]
  },
  ...
]
```                                                                                                       |
| **GET**    | `/employees/<int:id>`                   | Brak                                                                                                                                                                                                      |  
```json
{
  "id": "int",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "services": [
    {
      "id": "int",
      "name": "string",
      "price": "float"
    }
  ]
}
```                                                                                                       |
| **PUT**    | `/employees/<int:id>`                   | Body:  
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "service_ids": ["int", ...] // (przypisanie nowych usług)
}
```                                                                                                                                                     |  
```json
{
  "message": "Employee updated successfully"
}
```                                                                                   |
| **DELETE** | `/employees/<int:id>`                   | Brak                                                                                                                                                                                                      |  
```json
{
  "message": "Employee deleted successfully"
}
```                                                                                                       |
| **POST**   | `/services`                              | Nagłówek: `Authorization: Bearer <token>`  
Body:  
```json
{
  "name": "string",
  "description": "string",
  "price": "float"
}
```                                                                                                                                                     |  
```json
{
  "message": "Service created successfully"
}
```                                                                                   |
| **GET**    | `/services`                              | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
[
  {
    "id": "int",
    "name": "string",
    "description": "string",
    "price": "float"
  },
  ...
]
```                                                                                                       |
| **GET**    | `/services/<int:id>`                     | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
{
  "id": "int",
  "name": "string",
  "description": "string",
  "price": "float"
}
```                                                                                           |
| **PUT**    | `/services/<int:id>`                     | Nagłówek: `Authorization: Bearer <token>`  
Body:  
```json
{
  "name": "string",
  "description": "string",
  "price": "float"
}
```                                                                                                                                                     |  
```json
{
  "message": "Service updated successfully"
}
```                                                                                   |
| **DELETE** | `/services/<int:id>`                     | Nagłówek: `Authorization: Bearer <token>`                                                                                                                                                               |  
```json
{
  "message": "Service deleted successfully"
}
```                                                                                           |