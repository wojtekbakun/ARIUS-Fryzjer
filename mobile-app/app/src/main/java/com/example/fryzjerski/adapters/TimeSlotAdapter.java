package com.example.fryzjerski.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.fryzjerski.R;
import com.example.fryzjerski.models.AvailableTimeSlot;

import java.util.List;

public class TimeSlotAdapter extends RecyclerView.Adapter<TimeSlotAdapter.TimeSlotViewHolder> {

    // Lista dostępnych terminów
    private List<AvailableTimeSlot> timeSlots;

    // Konstruktor adaptera, przyjmuje listę terminów
    public TimeSlotAdapter(List<AvailableTimeSlot> timeSlots) {
        this.timeSlots = timeSlots;
    }

    @NonNull
    @Override
    public TimeSlotViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // Tworzenie widoku dla pojedynczego elementu listy (item_time_slot.xml)
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_time_slot, parent, false);
        return new TimeSlotViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull TimeSlotViewHolder holder, int position) {
        // Pobranie obiektu terminu z listy
        AvailableTimeSlot timeSlot = timeSlots.get(position);

        // Ustawienie godziny i stanu dostępności
        holder.timeTextView.setText(timeSlot.getTime());
        holder.itemView.setEnabled(timeSlot.isAvailable()); // Element aktywny tylko, jeśli termin jest dostępny
    }

    @Override
    public int getItemCount() {
        // Zwraca liczbę elementów w liście
        return timeSlots.size();
    }

    // Klasa ViewHolder przechowuje referencje do elementów widoku dla pojedynczego elementu
    static class TimeSlotViewHolder extends RecyclerView.ViewHolder {
        TextView timeTextView;

        public TimeSlotViewHolder(@NonNull View itemView) {
            super(itemView);
            timeTextView = itemView.findViewById(R.id.timeTextView);
        }
    }
}
