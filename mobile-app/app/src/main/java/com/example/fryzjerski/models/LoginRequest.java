package com.example.fryzjerski.models;

// Model reprezentujący dane wysyłane w żądaniu logowania
public class LoginRequest {
    private String email; // Email użytkownika
    private String password; // Hasło użytkownika

    // Konstruktor do inicjalizacji danych logowania
    public LoginRequest(String email, String password) {
        this.email = email;
        this.password = password;
    }
}
