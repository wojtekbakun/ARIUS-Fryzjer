package com.example.fryzjerski.models;

// Model reprezentujący dane wysyłane w żądaniu rejestracji
public class RegisterRequest {
    private String email; // Email użytkownika
    private String password; // Hasło użytkownika
    private String name; // Imię użytkownika
    private String surname; // Nazwisko użytkownika
    private String street; // Ulica użytkownika
    private String street_number; // Numer ulicy użytkownika
    private String postal_code; // Kod pocztowy użytkownika
    private String city; // Miasto użytkownika
    private String nip; // NIP użytkownika (opcjonalne)
    private String company_name; // Nazwa firmy użytkownika (opcjonalne)

    // Konstruktor do inicjalizacji danych rejestracji
    public RegisterRequest(String email, String password, String name, String surname,
                           String street, String street_number, String postal_code,
                           String city, String nip, String company_name) {
        this.email = email;
        this.password = password;
        this.name = name;
        this.surname = surname;
        this.street = street;
        this.street_number = street_number;
        this.postal_code = postal_code;
        this.city = city;
        this.nip = nip;
        this.company_name = company_name;
    }
}
