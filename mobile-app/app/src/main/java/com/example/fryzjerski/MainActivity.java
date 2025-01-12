package com.example.fryzjerski;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.example.fryzjerski.ui.fragments.AboutFragment;
import com.example.fryzjerski.ui.fragments.CatalogFragment;
import com.example.fryzjerski.ui.fragments.ProfileFragment;
import com.example.fryzjerski.ui.fragments.ScheduleAppointmentFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Inicjalizacja dolnego paska nawigacji
        BottomNavigationView bottomNavigationView = findViewById(R.id.bottomNavigationView);

        // Ustawienie domyślnego fragmentu na "Katalog"
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragmentContainer, new CatalogFragment())
                .commit();

        // Obsługa kliknięć na elementy dolnego paska nawigacji
        bottomNavigationView.setOnItemSelectedListener(item -> {
            Fragment selectedFragment = null;

            // Sprawdzenie, który element został kliknięty
            if (item.getItemId() == R.id.nav_catalog) {
                selectedFragment = new CatalogFragment(); // Fragment "Katalog"
            } else if (item.getItemId() == R.id.nav_about) {
                selectedFragment = new AboutFragment(); // Fragment "O nas"
            } else if (item.getItemId() == R.id.nav_schedule_appointment) {
                selectedFragment = new ScheduleAppointmentFragment(); // Fragment "Umów wizytę"
            } else if (item.getItemId() == R.id.nav_profile) {
                selectedFragment = new ProfileFragment(); // Fragment "Profil"
            }

            // Jeśli wybrano fragment, wykonaj zamianę
            if (selectedFragment != null) {
                getSupportFragmentManager().beginTransaction()
                        .replace(R.id.fragmentContainer, selectedFragment)
                        .commit();
            }
            return true; // Zwróć true, aby potwierdzić wybór
        });
    }
}
