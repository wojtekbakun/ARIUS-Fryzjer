package com.example.fryzjerski.ui.fragments;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.adapters.ServiceAdapter;
import com.example.fryzjerski.models.Service;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CatalogFragment extends Fragment {

    private RecyclerView recyclerViewServices; // RecyclerView do wyświetlania listy usług
    private ServiceAdapter serviceAdapter; // Adapter obsługujący listę usług
    private List<Service> services = new ArrayList<>(); // Lista usług
    private ApiService apiService;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_catalog, container, false);

        // Inicjalizacja RecyclerView
        recyclerViewServices = view.findViewById(R.id.recyclerViewServices);
        serviceAdapter = new ServiceAdapter(services);
        recyclerViewServices.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerViewServices.setAdapter(serviceAdapter);

        // Inicjalizacja ApiService
        apiService = ApiClient.getClient().create(ApiService.class);

        // Pobranie danych z API
        fetchServices();

        return view;
    }

    private void fetchServices() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", getContext().MODE_PRIVATE);
        String token = preferences.getString("token", null);

        if (token == null) {
            // Wyświetlenie błędu, jeśli token jest pusty
            Toast.makeText(getContext(), "Nie znaleziono tokenu, zaloguj się ponownie", Toast.LENGTH_SHORT).show();
            return;
        }

        apiService.getServices(token).enqueue(new Callback<List<Service>>() {
            @Override
            public void onResponse(Call<List<Service>> call, Response<List<Service>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    services.clear();
                    services.addAll(response.body());
                    serviceAdapter.notifyDataSetChanged();
                } else {
                    Toast.makeText(getContext(), "Nie udało się pobrać usług", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Service>> call, Throwable t) {
                Toast.makeText(getContext(), "Błąd: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
