# Wybór obrazu bazowego
FROM python:3.12.8

# Ustaw katalog roboczy
WORKDIR /backend

# Skopiuj pliki i instaluj zależności
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj całą aplikację
COPY . .

# Ustaw zmienne środowiskowe
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port aplikacji
EXPOSE 5000

# Polecenie startowe
CMD ["flask", "run"]