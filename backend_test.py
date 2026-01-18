#!/usr/bin/env python3
"""
Backend API Testing for Happy Teeth Dental Clinic
Tests appointment booking and gallery management APIs
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Backend URL from frontend environment
BACKEND_URL = "https://dental-excellence-3.preview.emergentagent.com/api"

class DentalClinicAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = {
            "appointment_apis": {},
            "gallery_apis": {},
            "overall_success": True
        }
        
    def log_result(self, test_name, success, message, response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if not success:
            self.test_results["overall_success"] = False
            
        if response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
        print()
        
    def test_health_check(self):
        """Test API health check"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Health Check", True, f"API is active: {data.get('message', '')}")
                return True
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_appointment_apis(self):
        """Test all appointment-related APIs"""
        print("=== TESTING APPOINTMENT BOOKING APIs ===")
        
        # Test data - realistic dental appointment data
        appointment_data = {
            "name": "Sarah Johnson",
            "phone": "+1-555-0123",
            "email": "sarah.johnson@email.com",
            "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "time": "10:00 AM",
            "service": "Dental Cleaning",
            "message": "Regular checkup and cleaning appointment"
        }
        
        created_appointment_id = None
        
        # 1. Test POST /api/appointments - Create appointment
        try:
            response = self.session.post(
                f"{self.base_url}/appointments",
                json=appointment_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                appointment = response.json()
                created_appointment_id = appointment.get("id")
                
                # Verify all fields are present
                required_fields = ["id", "name", "phone", "email", "date", "service", "status", "createdAt"]
                missing_fields = [field for field in required_fields if field not in appointment]
                
                if not missing_fields and appointment["status"] == "pending":
                    self.log_result("POST /api/appointments", True, 
                                  f"Appointment created successfully with ID: {created_appointment_id}")
                    self.test_results["appointment_apis"]["create"] = True
                else:
                    self.log_result("POST /api/appointments", False, 
                                  f"Missing fields: {missing_fields} or incorrect status")
                    self.test_results["appointment_apis"]["create"] = False
            else:
                self.log_result("POST /api/appointments", False, 
                              f"Status code: {response.status_code}, Response: {response.text}")
                self.test_results["appointment_apis"]["create"] = False
                
        except Exception as e:
            self.log_result("POST /api/appointments", False, f"Error: {str(e)}")
            self.test_results["appointment_apis"]["create"] = False
        
        # 2. Test GET /api/appointments - Retrieve appointments
        try:
            response = self.session.get(f"{self.base_url}/appointments")
            
            if response.status_code == 200:
                appointments = response.json()
                
                if isinstance(appointments, list):
                    # Check if our created appointment is in the list
                    found_appointment = None
                    if created_appointment_id:
                        found_appointment = next((apt for apt in appointments if apt.get("id") == created_appointment_id), None)
                    
                    if found_appointment:
                        self.log_result("GET /api/appointments", True, 
                                      f"Retrieved {len(appointments)} appointments, including our test appointment")
                        self.test_results["appointment_apis"]["get"] = True
                    else:
                        self.log_result("GET /api/appointments", False, 
                                      f"Retrieved {len(appointments)} appointments but test appointment not found")
                        self.test_results["appointment_apis"]["get"] = False
                else:
                    self.log_result("GET /api/appointments", False, "Response is not a list")
                    self.test_results["appointment_apis"]["get"] = False
            else:
                self.log_result("GET /api/appointments", False, 
                              f"Status code: {response.status_code}, Response: {response.text}")
                self.test_results["appointment_apis"]["get"] = False
                
        except Exception as e:
            self.log_result("GET /api/appointments", False, f"Error: {str(e)}")
            self.test_results["appointment_apis"]["get"] = False
        
        # 3. Test PATCH /api/appointments/:id/status - Update status
        if created_appointment_id:
            # Test confirming appointment
            try:
                status_update = {"status": "confirmed"}
                response = self.session.patch(
                    f"{self.base_url}/appointments/{created_appointment_id}/status",
                    json=status_update,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    updated_appointment = response.json()
                    if updated_appointment.get("status") == "confirmed":
                        self.log_result("PATCH /api/appointments/:id/status (confirm)", True, 
                                      "Appointment status updated to confirmed")
                        self.test_results["appointment_apis"]["update_confirm"] = True
                    else:
                        self.log_result("PATCH /api/appointments/:id/status (confirm)", False, 
                                      f"Status not updated correctly: {updated_appointment.get('status')}")
                        self.test_results["appointment_apis"]["update_confirm"] = False
                else:
                    self.log_result("PATCH /api/appointments/:id/status (confirm)", False, 
                                  f"Status code: {response.status_code}, Response: {response.text}")
                    self.test_results["appointment_apis"]["update_confirm"] = False
                    
            except Exception as e:
                self.log_result("PATCH /api/appointments/:id/status (confirm)", False, f"Error: {str(e)}")
                self.test_results["appointment_apis"]["update_confirm"] = False
            
            # Test cancelling appointment
            try:
                status_update = {"status": "cancelled"}
                response = self.session.patch(
                    f"{self.base_url}/appointments/{created_appointment_id}/status",
                    json=status_update,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    updated_appointment = response.json()
                    if updated_appointment.get("status") == "cancelled":
                        self.log_result("PATCH /api/appointments/:id/status (cancel)", True, 
                                      "Appointment status updated to cancelled")
                        self.test_results["appointment_apis"]["update_cancel"] = True
                    else:
                        self.log_result("PATCH /api/appointments/:id/status (cancel)", False, 
                                      f"Status not updated correctly: {updated_appointment.get('status')}")
                        self.test_results["appointment_apis"]["update_cancel"] = False
                else:
                    self.log_result("PATCH /api/appointments/:id/status (cancel)", False, 
                                  f"Status code: {response.status_code}, Response: {response.text}")
                    self.test_results["appointment_apis"]["update_cancel"] = False
                    
            except Exception as e:
                self.log_result("PATCH /api/appointments/:id/status (cancel)", False, f"Error: {str(e)}")
                self.test_results["appointment_apis"]["update_cancel"] = False
        else:
            self.log_result("PATCH /api/appointments/:id/status", False, 
                          "Cannot test status update - no appointment ID available")
            self.test_results["appointment_apis"]["update_confirm"] = False
            self.test_results["appointment_apis"]["update_cancel"] = False
    
    def test_gallery_apis(self):
        """Test all gallery-related APIs"""
        print("=== TESTING GALLERY MANAGEMENT APIs ===")
        
        created_image_id = None
        
        # 1. Test GET /api/gallery - Should return seeded images
        try:
            response = self.session.get(f"{self.base_url}/gallery")
            
            if response.status_code == 200:
                images = response.json()
                
                if isinstance(images, list):
                    if len(images) >= 6:
                        self.log_result("GET /api/gallery", True, 
                                      f"Retrieved {len(images)} gallery images (expected 6+ seeded images)")
                        self.test_results["gallery_apis"]["get"] = True
                    else:
                        self.log_result("GET /api/gallery", False, 
                                      f"Only {len(images)} images found, expected 6+ seeded images")
                        self.test_results["gallery_apis"]["get"] = False
                else:
                    self.log_result("GET /api/gallery", False, "Response is not a list")
                    self.test_results["gallery_apis"]["get"] = False
            else:
                self.log_result("GET /api/gallery", False, 
                              f"Status code: {response.status_code}, Response: {response.text}")
                self.test_results["gallery_apis"]["get"] = False
                
        except Exception as e:
            self.log_result("GET /api/gallery", False, f"Error: {str(e)}")
            self.test_results["gallery_apis"]["get"] = False
        
        # 2. Test POST /api/gallery - Add new image
        try:
            image_data = {
                "url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=800",
                "title": "Modern Dental Equipment",
                "category": "equipment"
            }
            
            response = self.session.post(
                f"{self.base_url}/gallery",
                json=image_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                image = response.json()
                created_image_id = image.get("id")
                
                # Verify all fields are present
                required_fields = ["id", "url", "title", "category", "createdAt"]
                missing_fields = [field for field in required_fields if field not in image]
                
                if not missing_fields:
                    self.log_result("POST /api/gallery", True, 
                                  f"Gallery image created successfully with ID: {created_image_id}")
                    self.test_results["gallery_apis"]["create"] = True
                else:
                    self.log_result("POST /api/gallery", False, 
                                  f"Missing fields: {missing_fields}")
                    self.test_results["gallery_apis"]["create"] = False
            else:
                self.log_result("POST /api/gallery", False, 
                              f"Status code: {response.status_code}, Response: {response.text}")
                self.test_results["gallery_apis"]["create"] = False
                
        except Exception as e:
            self.log_result("POST /api/gallery", False, f"Error: {str(e)}")
            self.test_results["gallery_apis"]["create"] = False
        
        # 3. Test DELETE /api/gallery/:id - Delete image
        if created_image_id:
            try:
                response = self.session.delete(f"{self.base_url}/gallery/{created_image_id}")
                
                if response.status_code == 200:
                    result = response.json()
                    if "message" in result and "deleted" in result["message"].lower():
                        self.log_result("DELETE /api/gallery/:id", True, 
                                      f"Gallery image deleted successfully: {result['message']}")
                        self.test_results["gallery_apis"]["delete"] = True
                    else:
                        self.log_result("DELETE /api/gallery/:id", False, 
                                      f"Unexpected response: {result}")
                        self.test_results["gallery_apis"]["delete"] = False
                else:
                    self.log_result("DELETE /api/gallery/:id", False, 
                                  f"Status code: {response.status_code}, Response: {response.text}")
                    self.test_results["gallery_apis"]["delete"] = False
                    
            except Exception as e:
                self.log_result("DELETE /api/gallery/:id", False, f"Error: {str(e)}")
                self.test_results["gallery_apis"]["delete"] = False
        else:
            self.log_result("DELETE /api/gallery/:id", False, 
                          "Cannot test image deletion - no image ID available")
            self.test_results["gallery_apis"]["delete"] = False
        
        # 4. Verify deletion by checking if image is gone
        if created_image_id and self.test_results["gallery_apis"].get("delete"):
            try:
                response = self.session.get(f"{self.base_url}/gallery")
                if response.status_code == 200:
                    images = response.json()
                    deleted_image = next((img for img in images if img.get("id") == created_image_id), None)
                    
                    if not deleted_image:
                        self.log_result("Verify Image Deletion", True, 
                                      "Confirmed: Deleted image no longer appears in gallery")
                    else:
                        self.log_result("Verify Image Deletion", False, 
                                      "Error: Deleted image still appears in gallery")
                        self.test_results["gallery_apis"]["delete"] = False
            except Exception as e:
                self.log_result("Verify Image Deletion", False, f"Error verifying deletion: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🦷 Happy Teeth Dental Clinic - Backend API Testing")
        print("=" * 60)
        
        # Test API connectivity first
        if not self.test_health_check():
            print("❌ Cannot connect to backend API. Stopping tests.")
            return False
        
        # Test appointment APIs
        self.test_appointment_apis()
        
        # Test gallery APIs  
        self.test_gallery_apis()
        
        # Print summary
        self.print_summary()
        
        return self.test_results["overall_success"]
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        # Appointment API results
        print("🗓️  APPOINTMENT APIs:")
        apt_results = self.test_results["appointment_apis"]
        print(f"   Create Appointment: {'✅' if apt_results.get('create') else '❌'}")
        print(f"   Get Appointments: {'✅' if apt_results.get('get') else '❌'}")
        print(f"   Update Status (Confirm): {'✅' if apt_results.get('update_confirm') else '❌'}")
        print(f"   Update Status (Cancel): {'✅' if apt_results.get('update_cancel') else '❌'}")
        
        # Gallery API results
        print("\n🖼️  GALLERY APIs:")
        gallery_results = self.test_results["gallery_apis"]
        print(f"   Get Gallery Images: {'✅' if gallery_results.get('get') else '❌'}")
        print(f"   Create Gallery Image: {'✅' if gallery_results.get('create') else '❌'}")
        print(f"   Delete Gallery Image: {'✅' if gallery_results.get('delete') else '❌'}")
        
        # Overall result
        print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if self.test_results['overall_success'] else '❌ SOME TESTS FAILED'}")
        print("=" * 60)

if __name__ == "__main__":
    tester = DentalClinicAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)