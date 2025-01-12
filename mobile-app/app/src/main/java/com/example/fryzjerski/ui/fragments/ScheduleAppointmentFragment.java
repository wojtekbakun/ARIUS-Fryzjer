package com.example.fryzjerski.ui.fragments;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CalendarView;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.adapters.TimeSlotAdapter;
import com.example.fryzjerski.models.AvailableTimeSlot;
import com.example.fryzjerski.models.Employee;
import com.example.fryzjerski.models.Service;
import com.example.fryzjerski.network.ApiClient;
import com.example.fryzjerski.network.ApiService;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ScheduleAppointmentFragment extends Fragment {

    private CalendarView calendarView;
    private RecyclerView timeSlotRecyclerView;
    private TimeSlotAdapter timeSlotAdapter;
    private Spinner serviceSpinner;
    private Spinner employeeSpinner;
    private Button confirmAppointmentButton;
    private List<AvailableTimeSlot> timeSlots = new ArrayList<>();
    private String selectedDate;
    private ApiService apiService;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_schedule_appointment, container, false);

        // Inicjalizacja widoków
        calendarView = view.findViewById(R.id.calendarView);
        timeSlotRecyclerView = view.findViewById(R.id.timeSlotRecyclerView);
        serviceSpinner = view.findViewById(R.id.serviceSpinner);
        employeeSpinner = view.findViewById(R.id.employeeSpinner);
        confirmAppointmentButton = view.findViewById(R.id.confirmAppointmentButton);

        // Inicjalizacja ApiService
        apiService = ApiClient.getClient().create(ApiService.class);

        // Konfiguracja RecyclerView
        timeSlotAdapter = new TimeSlotAdapter(timeSlots);
        timeSlotRecyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        timeSlotRecyclerView.setAdapter(timeSlotAdapter);

        // Obsługa kalendarza
        calendarView.setOnDateChangeListener((view1, year, month, dayOfMonth) -> {
            selectedDate = year + "-" + (month + 1) + "-" + dayOfMonth;
            fetchAvailableTimeSlots(selectedDate);
        });

        // Pobieranie usług i fryzjerów
        fetchServices();
        fetchEmployees();

        // Obsługa przycisku
        confirmAppointmentButton.setOnClickListener(v -> {
            // TODO: Obsługa rezerwacji po kliknięciu przycisku
            Toast.makeText(getContext(), "Appointment confirmed for " + selectedDate, Toast.LENGTH_SHORT).show();
        });

        return view;
    }

    // Pobranie listy usług z API
    private void fetchServices() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        String token = "Bearer " + preferences.getString("token", null);

        if (token == null) {
            Toast.makeText(getContext(), "Nie znaleziono tokenu, zaloguj się ponownie", Toast.LENGTH_SHORT).show();
            return;
        }

        apiService.getServices(token).enqueue(new Callback<List<Service>>() {
            @Override
            public void onResponse(Call<List<Service>> call, Response<List<Service>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    ArrayAdapter<Service> adapter = new ArrayAdapter<>(getContext(),
                            android.R.layout.simple_spinner_item, response.body());
                    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                    serviceSpinner.setAdapter(adapter);
                } else {
                    Toast.makeText(getContext(), "Failed to load services: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Service>> call, Throwable t) {
                Toast.makeText(getContext(), "Failed to load services", Toast.LENGTH_SHORT).show();
            }
        });
    }



    // Pobranie listy fryzjerów z API
    private void fetchEmployees() {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        String token = "Bearer " + preferences.getString("token", null);

        if (token == null || token.isEmpty()) {
            Toast.makeText(getContext(), "Nie znaleziono tokenu, zaloguj się ponownie", Toast.LENGTH_SHORT).show();
            return;
        }
        apiService.getEmployees(token).enqueue(new Callback<List<Employee>>() {
            @Override
            public void onResponse(Call<List<Employee>> call, Response<List<Employee>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    ArrayAdapter<Employee> adapter = new ArrayAdapter<>(getContext(),
                            android.R.layout.simple_spinner_item, response.body());
                    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                    employeeSpinner.setAdapter(adapter);
                } else {
                    Toast.makeText(getContext(), "Failed to load employees: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Employee>> call, Throwable t) {
                Toast.makeText(getContext(), "Failed to load employees", Toast.LENGTH_SHORT).show();
            }
        });
    }



    // Pobranie dostępnych terminów dla wybranego fryzjera i usługi
    private void fetchAvailableTimeSlots(String date) {
        SharedPreferences preferences = requireActivity().getSharedPreferences("user_data", Context.MODE_PRIVATE);
        String token = "Bearer " + preferences.getString("token", null);

        if (token == null) {
            Toast.makeText(getContext(), "Nie znaleziono tokenu, zaloguj się ponownie", Toast.LENGTH_SHORT).show();
            return;
        }

        Service selectedService = (Service) serviceSpinner.getSelectedItem();
        String serviceId = String.valueOf(selectedService.getId());

        Employee selectedEmployee = (Employee) employeeSpinner.getSelectedItem();
        String employeeId = String.valueOf(selectedEmployee.getId());

        apiService.getAvailableTimeSlots(token, serviceId, employeeId, date).enqueue(new Callback<List<AvailableTimeSlot>>() {
            @Override
            public void onResponse(Call<List<AvailableTimeSlot>> call, Response<List<AvailableTimeSlot>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    timeSlots.clear();
                    timeSlots.addAll(response.body());
                    timeSlotAdapter.notifyDataSetChanged();
                } else {
                    Toast.makeText(getContext(), "Failed to load time slots: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<AvailableTimeSlot>> call, Throwable t) {
                Toast.makeText(getContext(), "Failed to load time slots", Toast.LENGTH_SHORT).show();
            }
        });
    }


}
