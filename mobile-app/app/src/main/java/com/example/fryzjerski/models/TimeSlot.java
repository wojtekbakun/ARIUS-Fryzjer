package com.example.fryzjerski.models;

// Model reprezentujący pojedynczy termin
public class TimeSlot {
    private String day; // Dzień terminu
    private String time; // Godzina terminu
    private boolean isOccupied; // Czy termin jest zajęty

    // Konstruktor do inicjalizacji danych
    public TimeSlot(String day, String time, boolean isOccupied) {
        this.day = day;
        this.time = time;
        this.isOccupied = isOccupied;
    }

    // Getter do pobrania dnia
    public String getDay() {
        return day;
    }

    // Getter do pobrania godziny
    public String getTime() {
        return time;
    }

    // Getter do sprawdzenia, czy termin jest zajęty
    public boolean isOccupied() {
        return isOccupied;
    }
}
