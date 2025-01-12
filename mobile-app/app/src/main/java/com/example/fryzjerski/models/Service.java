package com.example.fryzjerski.models;

// Model reprezentujący dane usługi
public class Service {
    private int id; // ID usługi
    private String name; // Nazwa usługi
    private String description; // Opis usługi
    private float price; // Cena usługi

    // Getter do pobrania ID usługi
    public int getId() {
        return id;
    }

    // Setter do ustawienia ID usługi
    public void setId(int id) {
        this.id = id;
    }

    // Getter do pobrania nazwy usługi
    public String getName() {
        return name;
    }

    // Setter do ustawienia nazwy usługi
    public void setName(String name) {
        this.name = name;
    }

    // Getter do pobrania opisu usługi
    public String getDescription() {
        return description;
    }

    // Setter do ustawienia opisu usługi
    public void setDescription(String description) {
        this.description = description;
    }

    // Getter do pobrania ceny usługi
    public float getPrice() {
        return price;
    }

    // Setter do ustawienia ceny usługi
    public void setPrice(float price) {
        this.price = price;
    }
}
