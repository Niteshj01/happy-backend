# API Contracts & Integration Plan

## Overview
This document outlines the API contracts between frontend and backend for Happy Teeth Dental Clinic website.

## Backend Models

### 1. Appointment Model
```
{
  id: string (auto-generated)
  name: string (required)
  phone: string (required)
  email: string (optional)
  date: string (required)
  time: string (optional)
  service: string (required)
  message: string (optional)
  status: string (enum: 'pending', 'confirmed', 'cancelled')
  createdAt: datetime (auto-generated)
}
```

### 2. GalleryImage Model
```
{
  id: string (auto-generated)
  url: string (required)
  title: string (required)
  category: string (enum: 'clinic', 'equipment', 'team', 'patients')
  createdAt: datetime (auto-generated)
}
```

## API Endpoints

### Appointments

#### GET /api/appointments
- Description: Get all appointments
- Response: Array of appointment objects
- Used by: Admin Panel

#### POST /api/appointments
- Description: Create new appointment
- Request Body: { name, phone, email, date, time, service, message }
- Response: Created appointment object
- Used by: Landing Page booking form

#### PATCH /api/appointments/:id/status
- Description: Update appointment status
- Request Body: { status: 'pending' | 'confirmed' | 'cancelled' }
- Response: Updated appointment object
- Used by: Admin Panel

### Gallery Images

#### GET /api/gallery
- Description: Get all gallery images
- Response: Array of gallery image objects
- Used by: Landing Page, Admin Panel

#### POST /api/gallery
- Description: Add new gallery image
- Request Body: { url, title, category }
- Response: Created gallery image object
- Used by: Admin Panel

#### DELETE /api/gallery/:id
- Description: Delete gallery image
- Response: Success message
- Used by: Admin Panel

## Frontend Integration Changes

### Files to Update:
1. **LandingPage.jsx**
   - Replace `getStoredGalleryImages()` with API call to GET /api/gallery
   - Replace `saveAppointment()` with API call to POST /api/appointments
   
2. **AdminPanel.jsx**
   - Replace `getStoredAppointments()` with API call to GET /api/appointments
   - Replace `updateAppointmentStatus()` with API call to PATCH /api/appointments/:id/status
   - Replace `getStoredGalleryImages()` with API call to GET /api/gallery
   - Replace `saveGalleryImage()` with API call to POST /api/gallery
   - Replace `deleteGalleryImage()` with API call to DELETE /api/gallery/:id

### Mock Data to Remove:
- Remove localStorage usage from mock.js
- Keep only static data (services, whyChooseUs, businessInfo, reviews) in mock.js

## Implementation Steps

1. ✅ Create MongoDB models in backend
2. ✅ Implement API endpoints
3. ✅ Update frontend to use axios for API calls
4. ✅ Remove localStorage dependencies
5. ✅ Test integration
