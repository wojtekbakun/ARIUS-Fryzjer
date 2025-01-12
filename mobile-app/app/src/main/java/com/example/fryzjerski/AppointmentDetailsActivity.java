package com.example.fryzjerski;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class AppointmentDetailsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_appointment_details);

        // Pobranie nazwy usługi z Intentu
        String serviceName = getIntent().getStringExtra("serviceName");

        // Ustawienie nazwy usługi w polu tekstowym
        TextView serviceNameTextView = findViewById(R.id.serviceNameTextView);
        serviceNameTextView.setText(serviceName);
    }
}
