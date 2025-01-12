package com.example.fryzjerski.models;

// Model reprezentujący dane zwracane przez API po rejestracji
public class RegisterResponse {
    private String message; // Wiadomość zwracana przez serwer (np. sukces rejestracji)

    // Getter do pobrania wiadomości
    public String getMessage() {
        return message;
    }
}
