# Backend Flask z Dockerem

Backend do obsługi aplikacji rezerwacji usług fryzjerskich, zbudowany przy użyciu frameworka Flask i wdrożony w kontenerze Dockera.

---

## 🔧 **Funkcjonalności**

do wypisania

---

## 📁 **Struktura katalogów**
project-backend/
├── app/
│   ├── init.py          # Inicjalizacja aplikacji
│   ├── routes.py            # Definicje endpointów API
│   ├── models.py            # Definicje modeli baz danych
│   ├── config.py            # Konfiguracja aplikacji
│   ├── extensions.py        # Inicjalizacja rozszerzeń (Flask-SQLAlchemy, JWT)
├── requirements.txt         # Lista zależności Python
├── Dockerfile               # Konfiguracja obrazu Dockera
├── docker-compose.yaml      # Konfiguracja kontenerów Docker
└── wsgi.py                  # Punkt startowy aplikacji

---

## 🛠️ **Instalacja i uruchomienie**

### Uruchomienie lokalne

Do uruchomienia backendu na swoim komputerze nalezy wykonać następujące kroki:

#### Sklonowanie repozytorium
git clone https://github.com/wojtekbakun/ARIUS-Fryzjer
cd ARIUS-Fryzjer

#### Utworzenie i aktywacja wirtualnego środowiska
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

#### Uruchomienie aplikcji
```
flask run
```

### Uruchomienie z Dockerem
Budowa obrazu dockera:
```
docker-compose build
```

Uruchomienie kontenera:
```
docker-compose up
```
