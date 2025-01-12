package com.example.fryzjerski.models;

// Model reprezentujący dane wysyłane w żądaniu aktualizacji profilu
public class UpdateProfileRequest {
    private String firstName; // Imię użytkownika
    private String lastName; // Nazwisko użytkownika
    private String email; // Email użytkownika
    private String street; // Ulica użytkownika
    private String streetNumber; // Numer ulicy użytkownika
    private String postalCode; // Kod pocztowy użytkownika
    private String city; // Miasto użytkownika
    private String nip; // NIP użytkownika (opcjonalne)
    private String companyName; // Nazwa firmy użytkownika (opcjonalne)
    private String password; // Hasło użytkownika (opcjonalne)

    // Konstruktor do inicjalizacji wszystkich pól
    public UpdateProfileRequest(String firstName, String lastName, String email, String street,
                                String streetNumber, String postalCode, String city,
                                String nip, String companyName, String password) {
        this.firstName = firstName; // Ustawienie imienia użytkownika
        this.lastName = lastName; // Ustawienie nazwiska użytkownika
        this.email = email; // Ustawienie adresu email
        this.street = street; // Ustawienie ulicy
        this.streetNumber = streetNumber; // Ustawienie numeru ulicy
        this.postalCode = postalCode; // Ustawienie kodu pocztowego
        this.city = city; // Ustawienie miasta
        this.nip = nip; // Ustawienie NIP (opcjonalne)
        this.companyName = companyName; // Ustawienie nazwy firmy (opcjonalne)
        this.password = password; // Ustawienie hasła (opcjonalne)
    }

    // Getter do pobrania imienia użytkownika
    public String getFirstName() {
        return firstName;
    }

    // Setter do ustawienia imienia użytkownika
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    // Getter do pobrania nazwiska użytkownika
    public String getLastName() {
        return lastName;
    }

    // Setter do ustawienia nazwiska użytkownika
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    // Getter do pobrania adresu email
    public String getEmail() {
        return email;
    }

    // Setter do ustawienia adresu email
    public void setEmail(String email) {
        this.email = email;
    }

    // Getter do pobrania ulicy
    public String getStreet() {
        return street;
    }

    // Setter do ustawienia ulicy
    public void setStreet(String street) {
        this.street = street;
    }

    // Getter do pobrania numeru ulicy
    public String getStreetNumber() {
        return streetNumber;
    }

    // Setter do ustawienia numeru ulicy
    public void setStreetNumber(String streetNumber) {
        this.streetNumber = streetNumber;
    }

    // Getter do pobrania kodu pocztowego
    public String getPostalCode() {
        return postalCode;
    }

    // Setter do ustawienia kodu pocztowego
    public void setPostalCode(String postalCode) {
        this.postalCode = postalCode;
    }

    // Getter do pobrania miasta
    public String getCity() {
        return city;
    }

    // Setter do ustawienia miasta
    public void setCity(String city) {
        this.city = city;
    }

    // Getter do pobrania NIP
    public String getNip() {
        return nip;
    }

    // Setter do ustawienia NIP
    public void setNip(String nip) {
        this.nip = nip;
    }

    // Getter do pobrania nazwy firmy
    public String getCompanyName() {
        return companyName;
    }

    // Setter do ustawienia nazwy firmy
    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    // Getter do pobrania hasła
    public String getPassword() {
        return password;
    }

    // Setter do ustawienia hasła
    public void setPassword(String password) {
        this.password = password;
    }
}
