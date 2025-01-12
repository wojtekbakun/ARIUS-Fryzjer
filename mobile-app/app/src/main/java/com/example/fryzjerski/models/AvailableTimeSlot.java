package com.example.fryzjerski.models;

// Model reprezentujący dostępny termin
public class AvailableTimeSlot {
    private String time; // Godzina terminu
    private boolean available; // Czy termin jest dostępny

    // Konstruktor do inicjalizacji danych
    public AvailableTimeSlot(String time, boolean available) {
        this.time = time;
        this.available = available;
    }

    // Getter do pobrania godziny
    public String getTime() {
        return time;
    }

    // Getter do sprawdzenia dostępności
    public boolean isAvailable() {
        return available;
    }
}
