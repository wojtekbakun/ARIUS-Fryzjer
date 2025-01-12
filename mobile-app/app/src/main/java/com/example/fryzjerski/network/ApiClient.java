package com.example.fryzjerski.network;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

// Klasa odpowiedzialna za konfigurację klienta Retrofit
public class ApiClient {
    private static final String BASE_URL = "http://10.0.2.2:8080"; // Bazowy URL serwera API (dla emulatora Androida)
    private static Retrofit retrofit; // Instancja Retrofit

    // Metoda zwracająca instancję Retrofit
    public static Retrofit getClient() {
        if (retrofit == null) {
            // Inicjalizacja Retrofit z bazowym URL i konwerterem JSON
            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL) // Ustawienie bazowego URL
                    .addConverterFactory(GsonConverterFactory.create()) // Dodanie konwertera do obsługi JSON
                    .build();
        }
        return retrofit; // Zwraca zainicjalizowaną instancję Retrofit
    }
}
