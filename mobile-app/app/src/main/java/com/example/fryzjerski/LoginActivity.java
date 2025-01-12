package com.example.fryzjerski;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.fryzjerski.models.LoginRequest;
import com.example.fryzjerski.models.LoginResponse;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Pobranie referencji do elementów widoku
        EditText emailEditText = findViewById(R.id.editTextEmail); // Pole do wprowadzenia emaila
        EditText passwordEditText = findViewById(R.id.editTextPassword); // Pole do wprowadzenia hasła
        Button loginButton = findViewById(R.id.loginButton); // Przycisk logowania
        TextView registerRedirect = findViewById(R.id.registerRedirect); // Tekst przekierowujący na ekran rejestracji

        // Obsługa kliknięcia przycisku logowania
        loginButton.setOnClickListener(v -> {
            String email = emailEditText.getText().toString(); // Pobranie wprowadzonego emaila
            String password = passwordEditText.getText().toString(); // Pobranie wprowadzonego hasła

            // Sprawdzenie, czy pola nie są puste
            if (email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Wypełnij wszystkie pola", Toast.LENGTH_SHORT).show();
            } else {
                // Tworzenie obiektu żądania logowania
                LoginRequest loginRequest = new LoginRequest(email, password);

                // Inicjalizacja ApiService i wywołanie API
                ApiService apiService = ApiClient.getClient().create(ApiService.class);
                apiService.loginUser(loginRequest).enqueue(new Callback<LoginResponse>() {
                    @Override
                    public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                        // Jeśli logowanie zakończyło się sukcesem
                        if (response.isSuccessful() && response.body() != null) {
                            // Zapisanie tokena użytkownika w SharedPreferences
                            SharedPreferences preferences = getSharedPreferences("user_data", MODE_PRIVATE);
                            SharedPreferences.Editor editor = preferences.edit();
                            editor.putString("token", "Bearer " + response.body().getToken());
                            editor.apply();
                            Log.d("LoginActivity", "Saved token: " + response.body().getToken()); // Logowanie zapisanego tokena

                            // Wyświetlenie komunikatu o sukcesie logowania
                            Toast.makeText(LoginActivity.this, "Zalogowano pomyślnie!", Toast.LENGTH_SHORT).show();

                            // Przejście do głównego ekranu aplikacji (MainActivity)
                            Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                            startActivity(intent);
                            finish(); // Zamknięcie ekranu logowania
                        } else {
                            // Obsługa błędu logowania
                            Toast.makeText(LoginActivity.this, "Błąd logowania: " + response.code(), Toast.LENGTH_SHORT).show();
                        }
                    }

                    @Override
                    public void onFailure(Call<LoginResponse> call, Throwable t) {
                        // Obsługa błędu połączenia z serwerem
                        Toast.makeText(LoginActivity.this, "Błąd połączenia: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });

        // Obsługa kliknięcia tekstu przekierowującego na ekran rejestracji
        registerRedirect.setOnClickListener(v -> {
            // Przejście do ekranu rejestracji (RegisterActivity)
            Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
            startActivity(intent);
            finish(); // Zamknięcie ekranu logowania
        });
    }
}
