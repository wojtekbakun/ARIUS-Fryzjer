package com.example.fryzjerski;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import androidx.appcompat.app.AppCompatActivity;

public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        // Ustawienie opóźnienia dla ekranu powitalnego (SplashScreen)
        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            // Przejście do LoginActivity po 2 sekundach
            Intent intent = new Intent(SplashActivity.this, LoginActivity.class);
            startActivity(intent);
            finish(); // Zamknięcie SplashActivity
        }, 2000); // Opóźnienie 2 sekundy (2000 ms)
    }
}
