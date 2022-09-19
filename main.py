from tripadvisor.tripadvisor import TripAdvisor
from expedia.expedia import ExpediaMX
from expedia.expedia_com import ExpediaCOM
from bookings.bookings import Booking
from google.google_seadu import Google
from facebook.facebook import Facebook

from mysql.update_mysql import CargaSQL


if __name__ == '__main__':
    TripAdvisor()
    ExpediaMX()
    ExpediaCOM()
    Booking()
    Google()
    Facebook()
    CargaSQL()