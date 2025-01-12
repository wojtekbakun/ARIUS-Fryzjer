package com.example.fryzjerski.models;

public class Appointment {
    private String id;         // Appointment ID
    private String serviceId;  // Service ID
    private String userId;     // User ID
    private String dateTime;   // Appointment date and time
    private String status;     // Appointment status (e.g., pending, confirmed)

    // Getters
    public String getId() {
        return id;
    }

    public String getServiceId() {
        return serviceId;
    }

    public String getUserId() {
        return userId;
    }

    public String getDateTime() {
        return dateTime;
    }

    public String getStatus() {
        return status;
    }
}
