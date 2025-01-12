package com.example.fryzjerski.models;

// Model reprezentujący dane zwracane przez API po zalogowaniu
public class LoginResponse {
    private String token; // Token autoryzacyjny
    private int id; // ID użytkownika
    private String email; // Email użytkownika

    // Getter do pobrania tokena
    public String getToken() {
        return token;
    }

    // Getter do pobrania ID użytkownika
    public int getId() {
        return id;
    }

    // Getter do pobrania emaila
    public String getEmail() {
        return email;
    }
}
