package com.example.fryzjerski.network;

import com.example.fryzjerski.models.*;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.POST;
import retrofit2.http.Query;

// Interfejs definiujący wszystkie endpointy API
public interface ApiService {

    // Endpoint do rejestracji użytkownika
    @POST("/auth/register")
    Call<RegisterResponse> registerUser(@Body RegisterRequest registerRequest);

    // Endpoint do logowania użytkownika
    @POST("/auth/login")
    Call<LoginResponse> loginUser(@Body LoginRequest loginRequest);

    // Endpoint do pobierania danych profilu użytkownika
    @GET("/user/profile")
    Call<UserProfile> getUserProfile(@Header("Authorization") String token);

    // Endpoint do aktualizacji danych profilu użytkownika
    @POST("/user/profile")
    Call<Void> updateUserProfile(@Header("Authorization") String token, @Body UpdateProfileRequest request);

    // Endpoint do pobierania dostępnych usług
    @GET("/services")
    Call<List<Service>> getServices(@Header("Authorization") String token);

    // Endpoint do pobierania usług dostępnych w procesie rezerwacji
    @GET("/appointments/services")
    Call<List<Service>> getAppointmentServices();

    // Endpoint do pobierania listy pracowników
    @GET("/employees")
    Call<List<Employee>> getEmployees(@Header("Authorization") String token);

    // Endpoint do pobierania dostępnych terminów
    @GET("/available-time-slots")
    Call<List<AvailableTimeSlot>> getAvailableTimeSlots(
            @Header("Authorization") String token, // Token autoryzacyjny
            @Query("serviceId") String serviceId, // ID usługi
            @Query("employeeId") String employeeId, // ID pracownika
            @Query("date") String date // Data w formacie YYYY-MM-DD
    );
}
