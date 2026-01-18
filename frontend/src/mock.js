// Mock data for Happy Teeth Dental Clinic

export const mockAppointments = [
  {
    id: '1',
    name: 'Rajesh Kumar',
    phone: '9876543210',
    email: 'rajesh@example.com',
    date: '2024-03-15',
    time: '10:00 AM',
    service: 'Dental Implants',
    message: 'Need consultation for dental implant',
    status: 'pending',
    createdAt: '2024-03-10T10:30:00Z'
  },
  {
    id: '2',
    name: 'Priya Sharma',
    phone: '9876543211',
    email: 'priya@example.com',
    date: '2024-03-16',
    time: '2:00 PM',
    service: 'Invisalign',
    message: 'Interested in clear aligners',
    status: 'confirmed',
    createdAt: '2024-03-11T14:20:00Z'
  },
  {
    id: '3',
    name: 'Amit Verma',
    phone: '9876543212',
    email: 'amit@example.com',
    date: '2024-03-17',
    time: '11:30 AM',
    service: 'General Dentistry',
    message: 'Regular checkup needed',
    status: 'pending',
    createdAt: '2024-03-12T09:15:00Z'
  }
];

export const mockGalleryImages = [
  {
    id: '1',
    url: 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=800&q=80',
    title: 'Modern Dental Clinic',
    category: 'clinic'
  },
  {
    id: '2',
    url: 'https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800&q=80',
    title: 'State-of-the-Art Equipment',
    category: 'equipment'
  },
  {
    id: '3',
    url: 'https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=800&q=80',
    title: 'Comfortable Treatment Room',
    category: 'clinic'
  },
  {
    id: '4',
    url: 'https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=800&q=80',
    title: 'Professional Dental Team',
    category: 'team'
  },
  {
    id: '5',
    url: 'https://images.unsplash.com/photo-1609840112855-9ab5ad8f66e4?w=800&q=80',
    title: 'Advanced Dental Technology',
    category: 'equipment'
  },
  {
    id: '6',
    url: 'https://images.unsplash.com/photo-1588776814546-daab30f310ce?w=800&q=80',
    title: 'Happy Patient Care',
    category: 'patients'
  }
];

export const mockReviews = [
  {
    id: '1',
    name: 'Simran Kaur',
    rating: 5,
    text: 'Highly recommend this place to anyone looking for quality dental care. The staff is professional and caring.',
    date: '2024-02-20'
  },
  {
    id: '2',
    name: 'Rohit Singh',
    rating: 5,
    text: 'Very nice and responsive doctor and staff, having great experience. Best dental clinic in Kharar!',
    date: '2024-02-15'
  },
  {
    id: '3',
    name: 'Neha Gupta',
    rating: 5,
    text: 'Excellent service and truly skilled hands — highly recommend! Got my dental implants done here.',
    date: '2024-02-10'
  },
  {
    id: '4',
    name: 'Mandeep Kumar',
    rating: 5,
    text: 'Best dentist in Kharar! Very professional and the clinic is equipped with latest technology.',
    date: '2024-02-05'
  }
];

export const services = [
  {
    id: '1',
    title: 'Dental Implants',
    description: 'Permanent solution for missing teeth with advanced implant technology',
    icon: 'tooth'
  },
  {
    id: '2',
    title: 'Invisalign/Orthodontics',
    description: 'Straighten your teeth discreetly with clear aligners and expert orthodontic care',
    icon: 'smile'
  },
  {
    id: '3',
    title: 'Cosmetic Dentistry',
    description: 'Transform your smile with veneers, whitening, and aesthetic treatments',
    icon: 'sparkles'
  },
  {
    id: '4',
    title: 'Endodontics',
    description: 'Root canal treatments performed with precision and minimal discomfort',
    icon: 'activity'
  },
  {
    id: '5',
    title: 'General Dentistry',
    description: 'Comprehensive oral care including cleanings, fillings, and preventive treatments',
    icon: 'shield'
  },
  {
    id: '6',
    title: 'Emergency Dental Care',
    description: 'Same-day appointments for urgent dental issues',
    icon: 'clock'
  }
];

export const whyChooseUs = [
  {
    id: '1',
    title: 'Best Dentist in Kharar',
    description: 'Expert-led care you can trust',
    icon: 'award'
  },
  {
    id: '2',
    title: 'State-of-the-Art Technology',
    description: 'Latest equipment for precise treatments',
    icon: 'zap'
  },
  {
    id: '3',
    title: 'Patient-Centric Approach',
    description: 'Comfortable, personalized care',
    icon: 'heart'
  },
  {
    id: '4',
    title: '5.0 Star Rating',
    description: '178+ verified happy patients',
    icon: 'star'
  },
  {
    id: '5',
    title: 'Convenient Location',
    description: 'Easy to find in Kharar, above Barista',
    icon: 'map-pin'
  },
  {
    id: '6',
    title: 'Flexible Hours',
    description: 'Open until 9 PM for your convenience',
    icon: 'clock'
  }
];

export const businessInfo = {
  name: 'Happy Teeth Dental Clinic & Implant Centre',
  tagline: 'Your smile is our priority!',
  phone: '092051 70496',
  email: 'info@happyteethkharar.com',
  address: 'First Floor, Block-B, Ubber Realty, SCO No. 33, above Barista, Khanpur, Kharar, Punjab 140301',
  rating: 5.0,
  reviewCount: 178,
  hours: {
    monday: '9:00 AM - 9:00 PM',
    tuesday: '9:00 AM - 9:00 PM',
    wednesday: '9:00 AM - 9:00 PM',
    thursday: '9:00 AM - 9:00 PM',
    friday: '9:00 AM - 9:00 PM',
    saturday: '9:00 AM - 9:00 PM',
    sunday: '10:00 AM - 6:00 PM'
  },
  googleMapsEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3430.1234567890!2d76.6489!3d30.7408!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzDCsDQ0JzI3LjAiTiA3NsKwMzgnNTYuMCJF!5e0!3m2!1sen!2sin!4v1234567890'
};

// Admin credentials (mock)
export const adminCredentials = {
  username: 'admin',
  password: 'admin123'
};

// Local storage helpers
export const getStoredAppointments = () => {
  const stored = localStorage.getItem('appointments');
  return stored ? JSON.parse(stored) : mockAppointments;
};

export const saveAppointment = (appointment) => {
  const appointments = getStoredAppointments();
  const newAppointment = {
    ...appointment,
    id: Date.now().toString(),
    status: 'pending',
    createdAt: new Date().toISOString()
  };
  appointments.push(newAppointment);
  localStorage.setItem('appointments', JSON.stringify(appointments));
  return newAppointment;
};

export const updateAppointmentStatus = (id, status) => {
  const appointments = getStoredAppointments();
  const updated = appointments.map(apt => 
    apt.id === id ? { ...apt, status } : apt
  );
  localStorage.setItem('appointments', JSON.stringify(updated));
  return updated;
};

export const getStoredGalleryImages = () => {
  const stored = localStorage.getItem('galleryImages');
  return stored ? JSON.parse(stored) : mockGalleryImages;
};

export const saveGalleryImage = (image) => {
  const images = getStoredGalleryImages();
  const newImage = {
    ...image,
    id: Date.now().toString()
  };
  images.push(newImage);
  localStorage.setItem('galleryImages', JSON.stringify(images));
  return newImage;
};

export const deleteGalleryImage = (id) => {
  const images = getStoredGalleryImages();
  const filtered = images.filter(img => img.id !== id);
  localStorage.setItem('galleryImages', JSON.stringify(filtered));
  return filtered;
};