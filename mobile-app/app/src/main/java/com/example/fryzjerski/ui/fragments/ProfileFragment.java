package com.example.fryzjerski.ui.fragments;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.fryzjerski.R;
import com.example.fryzjerski.models.UpdateProfileRequest;
import com.example.fryzjerski.models.UserProfile;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProfileFragment extends Fragment {

    private TextView textWelcome; // Tekst powitalny
    private EditText editTextFirstName, editTextLastName, editTextStreet, editTextStreetNumber,
            editTextPostalCode, editTextCity, editTextNip, editTextCompanyName;
    private Button buttonUpdateProfile;
    private ApiService apiService;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profile, container, false);

        // Inicjalizacja widoków
        textWelcome = view.findViewById(R.id.textWelcome);
        editTextFirstName = view.findViewById(R.id.editTextFirstName);
        editTextLastName = view.findViewById(R.id.editTextLastName);
        editTextStreet = view.findViewById(R.id.editTextStreet);
        editTextStreetNumber = view.findViewById(R.id.editTextStreetNumber);
        editTextPostalCode = view.findViewById(R.id.editTextPostalCode);
        editTextCity = view.findViewById(R.id.editTextCity);
        editTextNip = view.findViewById(R.id.editTextNip);
        editTextCompanyName = view.findViewById(R.id.editTextCompanyName);
        buttonUpdateProfile = view.findViewById(R.id.buttonUpdateProfile);

        // Inicjalizacja ApiService
        apiService = ApiClient.getClient().create(ApiService.class);

        // Ustawienie tekstu powitalnego
        setWelcomeMessage();

        // Pobranie danych użytkownika
        fetchUserProfile();

        // Obsługa kliknięcia przycisku aktualizacji
        buttonUpdateProfile.setOnClickListener(v -> updateUserProfile());

        return view;
    }

    private void setWelcomeMessage() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        String firstName = preferences.getString("first_name", ""); // Pobranie imienia z SharedPreferences
        String lastName = preferences.getString("last_name", "");   // Pobranie nazwiska z SharedPreferences

        // Wyświetlenie tekstu powitalnego
        if (!firstName.isEmpty() && !lastName.isEmpty()) {
            textWelcome.setText(String.format("Witaj, %s %s", firstName, lastName));
        } else {
            textWelcome.setText("Witaj!"); // Domyślny tekst powitalny
        }
    }

    private void fetchUserProfile() {
        String token = getToken();

        apiService.getUserProfile(token).enqueue(new Callback<UserProfile>() {
            @Override
            public void onResponse(Call<UserProfile> call, Response<UserProfile> response) {
                if (response.isSuccessful() && response.body() != null) {
                    UserProfile userProfile = response.body();

                    // Ustawienie danych profilu w polach tekstowych
                    editTextFirstName.setText(userProfile.getFirstName());
                    editTextLastName.setText(userProfile.getLastName());
                    editTextStreet.setText(userProfile.getStreet());
                    editTextStreetNumber.setText(userProfile.getStreetNumber());
                    editTextPostalCode.setText(userProfile.getPostalCode());
                    editTextCity.setText(userProfile.getCity());
                    editTextNip.setText(userProfile.getNip());
                    editTextCompanyName.setText(userProfile.getCompanyName());
                } else {
                    Toast.makeText(getContext(), "Nie udało się pobrać danych", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<UserProfile> call, Throwable t) {
                Toast.makeText(getContext(), "Błąd: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateUserProfile() {
        String token = getToken();

        // Tworzenie obiektu żądania aktualizacji
        UpdateProfileRequest request = new UpdateProfileRequest(
                editTextFirstName.getText().toString(),
                editTextLastName.getText().toString(),
                null, // Email nie jest aktualizowany
                editTextStreet.getText().toString(),
                editTextStreetNumber.getText().toString(),
                editTextPostalCode.getText().toString(),
                editTextCity.getText().toString(),
                editTextNip.getText().toString(),
                editTextCompanyName.getText().toString(),
                null // Opcjonalne pole hasła
        );

        apiService.updateUserProfile(token, request).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(getContext(), "Profil zaktualizowany pomyślnie", Toast.LENGTH_SHORT).show();
                    fetchUserProfile(); // Odświeżenie danych po aktualizacji
                } else {
                    Toast.makeText(getContext(), "Nie udało się zaktualizować profilu", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(getContext(), "Błąd: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private String getToken() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        return preferences.getString("token", null);
    }
}
