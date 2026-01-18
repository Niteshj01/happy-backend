import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { 
  LogOut, Calendar, Users, Image as ImageIcon, Trash2, 
  CheckCircle, XCircle, Clock, Upload, X
} from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminPanel = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('appointments');
  const [appointments, setAppointments] = useState([]);
  const [galleryImages, setGalleryImages] = useState([]);
  const [imageUploadUrl, setImageUploadUrl] = useState('');
  const [imageTitle, setImageTitle] = useState('');
  const [imageCategory, setImageCategory] = useState('clinic');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [appointmentsRes, galleryRes] = await Promise.all([
        axios.get(`${API}/appointments`),
        axios.get(`${API}/gallery`)
      ]);
      setAppointments(appointmentsRes.data);
      setGalleryImages(galleryRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('Failed to load data');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('adminAuth');
    onLogout(false);
    toast.success('Logged out successfully');
  };

  const handleStatusChange = async (id, status) => {
    try {
      await axios.patch(`${API}/appointments/${id}/status`, { status });
      loadData();
      toast.success(`Appointment ${status}`);
    } catch (error) {
      console.error('Error updating status:', error);
      toast.error('Failed to update appointment status');
    }
  };

  const handleImageUpload = async (e) => {
    e.preventDefault();
    if (!imageUploadUrl || !imageTitle) {
      toast.error('Please fill in all fields');
      return;
    }
    
    setLoading(true);
    try {
      await axios.post(`${API}/gallery`, {
        url: imageUploadUrl,
        title: imageTitle,
        category: imageCategory
      });
      setImageUploadUrl('');
      setImageTitle('');
      setImageCategory('clinic');
      loadData();
      toast.success('Image added to gallery');
    } catch (error) {
      console.error('Error uploading image:', error);
      toast.error('Failed to add image');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteImage = async (id) => {
    if (window.confirm('Are you sure you want to delete this image?')) {
      try {
        await axios.delete(`${API}/gallery/${id}`);
        loadData();
        toast.success('Image deleted');
      } catch (error) {
        console.error('Error deleting image:', error);
        toast.error('Failed to delete image');
      }
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'confirmed': return 'bg-green-100 text-green-700';
      case 'cancelled': return 'bg-red-100 text-red-700';
      default: return 'bg-yellow-100 text-yellow-700';
    }
  };

  const stats = {
    total: appointments.length,
    pending: appointments.filter(a => a.status === 'pending').length,
    confirmed: appointments.filter(a => a.status === 'confirmed').length,
    images: galleryImages.length
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
              <p className="text-sm text-gray-600">Happy Teeth Dental Clinic</p>
            </div>
            <Button onClick={handleLogout} variant="outline" className="border-red-600 text-red-600 hover:bg-red-50">
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">Total Appointments</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">Pending</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">Confirmed</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-green-600">{stats.confirmed}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-gray-600">Gallery Images</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-blue-600">{stats.images}</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('appointments')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'appointments'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Calendar className="w-5 h-5 inline mr-2" />
                Appointments
              </button>
              <button
                onClick={() => setActiveTab('gallery')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'gallery'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <ImageIcon className="w-5 h-5 inline mr-2" />
                Gallery Management
              </button>
            </nav>
          </div>

          <div className="p-6">
            {/* Appointments Tab */}
            {activeTab === 'appointments' && (
              <div className="space-y-4">
                {appointments.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">No appointments yet</p>
                ) : (
                  appointments.map((appointment) => (
                    <Card key={appointment.id} className="border-2">
                      <CardContent className="p-6">
                        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-3">
                              <h3 className="text-lg font-semibold text-gray-900">{appointment.name}</h3>
                              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                                {appointment.status}
                              </span>
                            </div>
                            <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-600">
                              <div>
                                <p><strong>Phone:</strong> {appointment.phone}</p>
                                <p><strong>Email:</strong> {appointment.email || 'N/A'}</p>
                              </div>
                              <div>
                                <p><strong>Date:</strong> {appointment.date}</p>
                                <p><strong>Time:</strong> {appointment.time || 'N/A'}</p>
                              </div>
                            </div>
                            <p className="mt-3 text-sm"><strong>Service:</strong> {appointment.service}</p>
                            {appointment.message && (
                              <p className="mt-2 text-sm text-gray-600"><strong>Message:</strong> {appointment.message}</p>
                            )}
                          </div>
                          <div className="flex md:flex-col gap-2 mt-4 md:mt-0 md:ml-6">
                            <Button 
                              onClick={() => handleStatusChange(appointment.id, 'confirmed')}
                              size="sm"
                              className="bg-green-600 hover:bg-green-700 text-white"
                              disabled={appointment.status === 'confirmed'}
                            >
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Confirm
                            </Button>
                            <Button 
                              onClick={() => handleStatusChange(appointment.id, 'cancelled')}
                              size="sm"
                              variant="outline"
                              className="border-red-600 text-red-600 hover:bg-red-50"
                              disabled={appointment.status === 'cancelled'}
                            >
                              <XCircle className="w-4 h-4 mr-1" />
                              Cancel
                            </Button>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            )}

            {/* Gallery Tab */}
            {activeTab === 'gallery' && (
              <div>
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle>Add New Image</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleImageUpload} className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Image URL</label>
                        <Input 
                          type="url"
                          value={imageUploadUrl}
                          onChange={(e) => setImageUploadUrl(e.target.value)}
                          placeholder="https://example.com/image.jpg"
                          required
                        />
                        <p className="text-xs text-gray-500 mt-1">Enter the URL of the image you want to add</p>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Image Title</label>
                          <Input 
                            type="text"
                            value={imageTitle}
                            onChange={(e) => setImageTitle(e.target.value)}
                            placeholder="e.g., Modern Treatment Room"
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                          <select
                            value={imageCategory}
                            onChange={(e) => setImageCategory(e.target.value)}
                            className="w-full h-10 px-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          >
                            <option value="clinic">Clinic</option>
                            <option value="equipment">Equipment</option>
                            <option value="team">Team</option>
                            <option value="patients">Patients</option>
                          </select>
                        </div>
                      </div>
                      <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                        <Upload className="w-4 h-4 mr-2" />
                        Add Image
                      </Button>
                    </form>
                  </CardContent>
                </Card>

                <div className="grid md:grid-cols-3 gap-6">
                  {galleryImages.map((image) => (
                    <Card key={image.id} className="overflow-hidden">
                      <div className="relative">
                        <img 
                          src={image.url} 
                          alt={image.title} 
                          className="w-full h-48 object-cover"
                        />
                        <Button
                          onClick={() => handleDeleteImage(image.id)}
                          size="sm"
                          variant="destructive"
                          className="absolute top-2 right-2 bg-red-600 hover:bg-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                      <CardContent className="p-4">
                        <h3 className="font-semibold text-gray-900">{image.title}</h3>
                        <p className="text-sm text-gray-600 capitalize">{image.category}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;