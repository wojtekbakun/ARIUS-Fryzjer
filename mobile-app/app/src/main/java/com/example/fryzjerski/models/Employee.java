package com.example.fryzjerski.models;

// Model reprezentujący dane pracownika
public class Employee {
    private int id; // ID pracownika
    private String firstName; // Imię pracownika
    private String lastName; // Nazwisko pracownika
    private String email; // Email pracownika
    private String phone; // Telefon pracownika

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    @Override
    public String toString() {
        return firstName + " " + lastName;
    }
}
