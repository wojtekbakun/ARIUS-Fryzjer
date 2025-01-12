package com.example.fryzjerski.models;

import androidx.annotation.Nullable;

import com.google.gson.annotations.SerializedName;

public class UserProfile {

    @SerializedName("first_name")
    @Nullable
    private String firstName;

    @SerializedName("last_name")
    @Nullable
    private String lastName;

    @SerializedName("email")
    private String email;

    @SerializedName("street")
    @Nullable
    private String street;

    @SerializedName("street_number")
    @Nullable
    private String streetNumber;

    @SerializedName("postal_code")
    @Nullable
    private String postalCode;

    @SerializedName("city")
    @Nullable
    private String city;

    @SerializedName("nip")
    @Nullable
    private String nip;

    @SerializedName("company_name")
    @Nullable
    private String companyName;

    // Konstruktor
    public UserProfile(@Nullable String firstName, @Nullable String lastName, @Nullable String street,
                       @Nullable String streetNumber, @Nullable String postalCode, @Nullable String city,
                       @Nullable String nip, @Nullable String companyName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.street = street;
        this.streetNumber = streetNumber;
        this.postalCode = postalCode;
        this.city = city;
        this.nip = nip;
        this.companyName = companyName;
        this.email = email;
    }

    @Nullable
    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(@Nullable String firstName) {
        this.firstName = firstName;
    }

    @Nullable
    public String getLastName() {
        return lastName;
    }

    public void setLastName(@Nullable String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Nullable
    public String getStreet() {
        return street;
    }

    public void setStreet(@Nullable String street) {
        this.street = street;
    }

    @Nullable
    public String getStreetNumber() {
        return streetNumber;
    }

    public void setStreetNumber(@Nullable String streetNumber) {
        this.streetNumber = streetNumber;
    }

    @Nullable
    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(@Nullable String postalCode) {
        this.postalCode = postalCode;
    }

    @Nullable
    public String getCity() {
        return city;
    }

    public void setCity(@Nullable String city) {
        this.city = city;
    }

    @Nullable
    public String getNip() {
        return nip;
    }

    public void setNip(@Nullable String nip) {
        this.nip = nip;
    }

    @Nullable
    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(@Nullable String companyName) {
        this.companyName = companyName;
    }

    @Override
    public String toString() {
        return "UserProfile{" +
                "firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", email='" + email + '\'' +
                ", street='" + street + '\'' +
                ", streetNumber='" + streetNumber + '\'' +
                ", postalCode='" + postalCode + '\'' +
                ", city='" + city + '\'' +
                ", nip='" + nip + '\'' +
                ", companyName='" + companyName + '\'' +
                '}';
    }
}
