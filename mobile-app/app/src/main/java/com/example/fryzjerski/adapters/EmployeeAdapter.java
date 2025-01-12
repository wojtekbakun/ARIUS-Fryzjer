package com.example.fryzjerski.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.models.Employee;

import java.util.List;

public class EmployeeAdapter extends RecyclerView.Adapter<EmployeeAdapter.EmployeeViewHolder> {

    // Lista pracowników do wyświetlenia
    private final List<Employee> employees;

    // Konstruktor adaptera, przyjmuje listę pracowników
    public EmployeeAdapter(List<Employee> employees) {
        this.employees = employees;
    }

    @NonNull
    @Override
    public EmployeeViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Tworzenie widoku dla pojedynczego elementu listy (item_employee.xml)
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_employee, parent, false);
        return new EmployeeViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull EmployeeViewHolder holder, int position) {
        // Pobranie obiektu pracownika z listy
        Employee employee = employees.get(position);

        // Ustawienie danych w odpowiednich polach tekstowych
        holder.nameTextView.setText(employee.getFirstName() + " " + employee.getLastName());
        holder.emailTextView.setText(employee.getEmail());
        holder.phoneTextView.setText(employee.getPhone());
    }

    @Override
    public int getItemCount() {
        // Zwraca liczbę elementów w liście
        return employees.size();
    }

    // Klasa ViewHolder przechowuje referencje do elementów widoku dla pojedynczego elementu
    public static class EmployeeViewHolder extends RecyclerView.ViewHolder {
        TextView nameTextView, emailTextView, phoneTextView;

        public EmployeeViewHolder(@NonNull View itemView) {
            super(itemView);
            nameTextView = itemView.findViewById(R.id.employeeNameTextView);
            emailTextView = itemView.findViewById(R.id.employeeEmailTextView);
            phoneTextView = itemView.findViewById(R.id.employeePhoneTextView);
        }
    }
}
