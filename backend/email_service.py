import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def send_appointment_confirmation_email(
    appointment_data: dict,
    recipient_email: str
) -> bool:
    """
    Send appointment confirmation email to patient
    Returns True if email sent successfully, False otherwise
    """
    
    # Check if SMTP credentials are configured
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    # If credentials not configured, log and return False (won't crash the app)
    if not smtp_email or not smtp_password:
        logger.warning("SMTP credentials not configured. Email notification skipped.")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Appointment Confirmed - Happy Teeth Dental Clinic"
        message["From"] = smtp_email
        message["To"] = recipient_email
        
        # Email body with appointment details
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #2563eb; margin-bottom: 10px;">Happy Teeth Dental Clinic</h1>
                        <p style="color: #14b8a6; font-size: 16px;">Your smile is our priority!</p>
                    </div>
                    
                    <div style="background-color: #dbeafe; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #1e40af; margin-top: 0;">✓ Appointment Confirmed</h2>
                        <p style="font-size: 16px;">Dear {appointment_data.get('name', 'Patient')},</p>
                        <p>Your appointment has been confirmed. We look forward to seeing you!</p>
                    </div>
                    
                    <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #374151; margin-top: 0;">Appointment Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Service:</td>
                                <td style="padding: 8px 0;">{appointment_data.get('service', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Date:</td>
                                <td style="padding: 8px 0;">{appointment_data.get('date', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Time:</td>
                                <td style="padding: 8px 0;">{appointment_data.get('time', 'To be confirmed')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #059669; margin-top: 0;">Clinic Information:</h3>
                        <p style="margin: 5px 0;"><strong>Address:</strong><br>
                        First Floor, Block-B, Ubber Realty, SCO No. 33,<br>
                        above Barista, Khanpur, Kharar, Punjab 140301</p>
                        <p style="margin: 5px 0;"><strong>Phone:</strong> 092051 70496</p>
                        <p style="margin: 5px 0;"><strong>Hours:</strong> Mon-Sat: 9 AM - 9 PM | Sun: 10 AM - 6 PM</p>
                    </div>
                    
                    <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="margin: 0; font-size: 14px; color: #92400e;">
                            <strong>Important:</strong> Please arrive 10 minutes before your scheduled time. 
                            If you need to reschedule or cancel, please call us at least 24 hours in advance.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                        <p style="color: #6b7280; font-size: 14px;">
                            Thank you for choosing Happy Teeth Dental Clinic!<br>
                            We're committed to providing you with the best dental care.
                        </p>
                        <p style="color: #9ca3af; font-size: 12px; margin-top: 15px;">
                            This is an automated confirmation email. Please do not reply to this email.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text version as fallback
        text_content = f"""
        Happy Teeth Dental Clinic
        Your smile is our priority!
        
        APPOINTMENT CONFIRMED
        
        Dear {appointment_data.get('name', 'Patient')},
        
        Your appointment has been confirmed. We look forward to seeing you!
        
        APPOINTMENT DETAILS:
        Service: {appointment_data.get('service', 'N/A')}
        Date: {appointment_data.get('date', 'N/A')}
        Time: {appointment_data.get('time', 'To be confirmed')}
        
        CLINIC INFORMATION:
        Address: First Floor, Block-B, Ubber Realty, SCO No. 33,
                 above Barista, Khanpur, Kharar, Punjab 140301
        Phone: 092051 70496
        Hours: Mon-Sat: 9 AM - 9 PM | Sun: 10 AM - 6 PM
        
        IMPORTANT: Please arrive 10 minutes before your scheduled time.
        If you need to reschedule or cancel, please call us at least 24 hours in advance.
        
        Thank you for choosing Happy Teeth Dental Clinic!
        """
        
        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(message)
        
        logger.info(f"Confirmation email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False
