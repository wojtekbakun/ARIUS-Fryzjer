package com.example.fryzjerski.ui.fragments;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.adapters.EmployeeAdapter;
import com.example.fryzjerski.models.Employee;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class AboutFragment extends Fragment {

    private RecyclerView recyclerViewEmployees; // RecyclerView do wyświetlania listy fryzjerów
    private EmployeeAdapter employeeAdapter; // Adapter dla RecyclerView
    private List<Employee> employees = new ArrayList<>(); // Lista fryzjerów
    private ApiService apiService;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_about, container, false);

        // Inicjalizacja RecyclerView
        recyclerViewEmployees = view.findViewById(R.id.recyclerViewEmployees);
        recyclerViewEmployees.setLayoutManager(new LinearLayoutManager(getContext()));
        employeeAdapter = new EmployeeAdapter(employees);
        recyclerViewEmployees.setAdapter(employeeAdapter);

        // Inicjalizacja ApiService
        apiService = ApiClient.getClient().create(ApiService.class);

        // Pobierz listę fryzjerów
        fetchEmployees();

        // Obsługa przycisku oceny
        Button rateButton = view.findViewById(R.id.rateButton);
        rateButton.setOnClickListener(v -> openRatingPage());

        return view;
    }

    private void fetchEmployees() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        String token = "Bearer " + preferences.getString("token", null);

        if (token == null || token.isEmpty()) {
            Toast.makeText(getContext(), "Nie znaleziono tokenu, zaloguj się ponownie", Toast.LENGTH_SHORT).show();
            return;
        }

        // Wywołanie API do pobrania listy fryzjerów
        apiService.getEmployees(token).enqueue(new Callback<List<Employee>>() {
            @Override
            public void onResponse(Call<List<Employee>> call, Response<List<Employee>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    employees.clear();
                    employees.addAll(response.body());
                    employeeAdapter.notifyDataSetChanged();
                } else {
                    Toast.makeText(getContext(), "Nie udało się pobrać fryzjerów", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Employee>> call, Throwable t) {
                Toast.makeText(getContext(), "Błąd: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void openRatingPage() {
        // Otwórz stronę oceny w przeglądarce
        Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://www.example.com/rate-us"));
        startActivity(browserIntent);
    }
}
