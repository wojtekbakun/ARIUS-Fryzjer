package com.example.fryzjerski.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.models.Service;

import java.util.List;

public class ServiceAdapter extends RecyclerView.Adapter<ServiceAdapter.ServiceViewHolder> {

    // Lista usług do wyświetlenia
    private List<Service> services;

    // Konstruktor adaptera, przyjmuje listę usług
    public ServiceAdapter(List<Service> services) {
        this.services = services;
    }

    @NonNull
    @Override
    public ServiceViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Tworzenie widoku dla pojedynczego elementu listy (item_service.xml)
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_service, parent, false);
        return new ServiceViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ServiceViewHolder holder, int position) {
        // Pobranie obiektu usługi z listy
        Service service = services.get(position);

        // Ustawienie danych w odpowiednich polach tekstowych
        holder.nameTextView.setText(service.getName());
        holder.descriptionTextView.setText(service.getDescription());
        holder.priceTextView.setText(String.format("%.2f zł", service.getPrice()));
    }

    @Override
    public int getItemCount() {
        // Zwraca liczbę elementów w liście
        return services.size();
    }

    // Klasa ViewHolder przechowuje referencje do elementów widoku dla pojedynczego elementu
    static class ServiceViewHolder extends RecyclerView.ViewHolder {
        TextView nameTextView, descriptionTextView, priceTextView;

        public ServiceViewHolder(@NonNull View itemView) {
            super(itemView);
            nameTextView = itemView.findViewById(R.id.serviceNameTextView);
            descriptionTextView = itemView.findViewById(R.id.serviceDescriptionTextView);
            priceTextView = itemView.findViewById(R.id.servicePriceTextView);
        }
    }
}
