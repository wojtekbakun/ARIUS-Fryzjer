package com.example.fryzjerski;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.fryzjerski.models.RegisterRequest;
import com.example.fryzjerski.models.RegisterResponse;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // Pobranie referencji do pól tekstowych i przycisków w widoku
        EditText nameEditText = findViewById(R.id.editTextName); // Pole na imię
        EditText surnameEditText = findViewById(R.id.editTextSurname); // Pole na nazwisko
        EditText streetEditText = findViewById(R.id.editTextStreet); // Pole na ulicę
        EditText streetNumberEditText = findViewById(R.id.editTextStreetNumber); // Pole na numer ulicy
        EditText postalCodeEditText = findViewById(R.id.editTextPostalCode); // Pole na kod pocztowy
        EditText cityEditText = findViewById(R.id.editTextCity); // Pole na miasto
        EditText nipEditText = findViewById(R.id.editTextNIP); // Pole na NIP (opcjonalne)
        EditText companyNameEditText = findViewById(R.id.editTextCompanyName); // Pole na nazwę firmy (opcjonalne)
        EditText emailEditText = findViewById(R.id.editTextEmail); // Pole na email
        EditText passwordEditText = findViewById(R.id.editTextPassword); // Pole na hasło
        Button registerButton = findViewById(R.id.registerButton); // Przycisk rejestracji
        TextView loginRedirect = findViewById(R.id.loginRedirect); // Tekst do przekierowania na ekran logowania

        // Obsługa kliknięcia przycisku rejestracji
        registerButton.setOnClickListener(v -> {
            // Pobranie wartości z pól tekstowych
            String name = nameEditText.getText().toString().trim();
            String surname = surnameEditText.getText().toString().trim();
            String street = streetEditText.getText().toString().trim();
            String streetNumber = streetNumberEditText.getText().toString().trim();
            String postalCode = postalCodeEditText.getText().toString().trim();
            String city = cityEditText.getText().toString().trim();
            String nip = nipEditText.getText().toString().trim();
            String companyName = companyNameEditText.getText().toString().trim();
            String email = emailEditText.getText().toString().trim();
            String password = passwordEditText.getText().toString().trim();

            // Walidacja pól obowiązkowych
            if (name.isEmpty() || surname.isEmpty() || street.isEmpty() || streetNumber.isEmpty() ||
                    postalCode.isEmpty() || city.isEmpty() || email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Wypełnij wszystkie obowiązkowe pola", Toast.LENGTH_SHORT).show();
                return;
            }

            // Walidacja poprawności emaila
            if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
                Toast.makeText(this, "Wprowadź poprawny adres email", Toast.LENGTH_SHORT).show();
                return;
            }

            // Tworzenie obiektu z danymi do rejestracji
            RegisterRequest registerRequest = new RegisterRequest(
                    email,
                    password,
                    name,
                    surname,
                    street,
                    streetNumber,
                    postalCode,
                    city,
                    nip.isEmpty() ? null : nip, // Jeśli NIP jest pusty, ustaw null
                    companyName.isEmpty() ? null : companyName // Jeśli nazwa firmy jest pusta, ustaw null
            );

            // Wywołanie API
            ApiService apiService = ApiClient.getClient().create(ApiService.class);
            apiService.registerUser(registerRequest).enqueue(new Callback<RegisterResponse>() {
                @Override
                public void onResponse(Call<RegisterResponse> call, Response<RegisterResponse> response) {
                    // Jeśli rejestracja zakończyła się sukcesem
                    if (response.isSuccessful() && response.body() != null) {
                        // Zapisanie imienia i nazwiska w SharedPreferences
                        SharedPreferences preferences = getSharedPreferences("user_data", MODE_PRIVATE);
                        SharedPreferences.Editor editor = preferences.edit();
                        editor.putString("first_name", name);
                        editor.putString("last_name", surname);
                        editor.apply();

                        // Wyświetlenie komunikatu o sukcesie
                        Toast.makeText(RegisterActivity.this, response.body().getMessage(), Toast.LENGTH_SHORT).show();

                        // Przejście do ekranu logowania
                        Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                        startActivity(intent);
                        finish(); // Zamknięcie ekranu rejestracji
                    } else {
                        // Obsługa błędów rejestracji
                        Toast.makeText(RegisterActivity.this, "Błąd rejestracji: " + response.code(), Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<RegisterResponse> call, Throwable t) {
                    // Obsługa błędu połączenia
                    Toast.makeText(RegisterActivity.this, "Błąd połączenia: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                }
            });
        });

        // Obsługa kliknięcia tekstu przekierowującego na ekran logowania
        loginRedirect.setOnClickListener(v -> {
            // Przejście do ekranu logowania
            Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
            startActivity(intent);
            finish();
        });
    }
}
