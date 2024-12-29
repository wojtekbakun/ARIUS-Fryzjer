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

### 1. Wejdź do kontenera backendu

Uruchom:
```
docker exec -it flask-app-1 sh
```

### 2. Wykonaj migracje

Wewnątrz kontenera uruchom następujące komendy:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Aktualne endpointy
| Metoda | Endpoint                | Parametry (Body / Query)                                                                                   | Zwraca                                         |
|--------|-------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| POST   | `/auth/register`        | Body: `{ "email": "string", "password": "string" }`                                                        | `{ "message": "User registered successfully" }` |
| POST   | `/auth/login`           | Body: `{ "email": "string", "password": "string" }`                                                        | `{ "token": "string", "id": "int", "email": "string" }` |
| GET    | `/user/profile`         | Nagłówek: `Authorization: Bearer <token>`                                                                  | `{ "id": "int", "email": "string" }`          |
| GET    | `/appointments/services`| Brak                                                                                                       | `[ { "id": "int", "name": "string", "price": "float" }, ... ]` |
| POST   | `/appointments`         | Body: `{ "user_id": "int", "service_id": "int", "date": "YYYY-MM-DD HH:MM:SS" }`                           | `{ "message": "Appointment created successfully" }` |
| GET    | `/appointments`         | Nagłówek: `Authorization: Bearer <token>`                                                                  | `[ { "id": "int", "service": "string", "date": "YYYY-MM-DD HH:MM:SS", "status": "string" }, ... ]` |
| POST   | `/reviews`              | Body: `{ "service_id": "int", "rating": "int", "comment": "string" }`                                      | `{ "message": "Review submitted successfully" }` |
| POST   | `/payments`             | Body: `{ "user_id": "int", "amount": "float" }`                                                            | `{ "message": "Payment created successfully" }` |