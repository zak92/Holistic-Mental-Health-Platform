from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ...views import * 


class TestUrls(SimpleTestCase):

  def test_client_booking_url_resolves(self):
    url = reverse('client-booking', args=['jack'])
    self.assertEquals(resolve(url).func, individualBooking)

  def test_confirm_booking_url_resolves(self):
    url = reverse('confirm-booking', args=['2'])
    self.assertEquals(resolve(url).func, bookingConfirmationByClient)

  def test_cancel_booking_url_resolves(self):
    url = reverse('cancel-booking', args=['5'])
    self.assertEquals(resolve(url).func, bookingCancellationByClient)

  def test_confirm_booking_sp_url_resolves(self):
    url = reverse('confirm-booking-sp', args=['4'])
    self.assertEquals(resolve(url).func, bookingConfirmationBySP)

  def test_cancel_booking_sp_url_resolves(self):
    url = reverse('cancel-booking-sp',  args=['4'])
    self.assertEquals(resolve(url).func, bookingCancellationBySP)

  def test_client_appointments_url_resolves(self):
    url = reverse('client-appointments', args=['tom'])
    self.assertEquals(resolve(url).func, clientAppointments)

  def test_schedule_appointments_url_resolves(self):
    url = reverse('schedule-appointments', args=['anna'] )
    self.assertEquals(resolve(url).func, serviceProviderScheduleAppointments)

  def test_booked_appointments_url_resolves(self):
    url = reverse('booked-appointments', args=['jamie'] )
    self.assertEquals(resolve(url).func, serviceProviderBookedAppointments)