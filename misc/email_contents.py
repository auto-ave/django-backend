def EMAIL_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'email': booking.booked_by.user.email,
        'subject': 'Booking confirmed at {}'.format(store.name),
        'html_content': 'Your booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        
    }