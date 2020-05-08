from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger
from django.db.models import F


def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    # try:
    #     flight = Flight.objects.get(pk=flight_id)
    # except Flight.DoesNotExist:
    #     raise Http404("Flight does not exist")
    flight = get_object_or_404(Flight, pk=flight_id)
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all(),
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    seats = Flight.objects.get(pk=flight_id).seats
    if seats > 1:
        try:
            passenger_id = int(request.POST["passenger"])
            flight = Flight.objects.get(pk=flight_id)
            passenger = Passenger.objects.get(pk=passenger_id)
        except KeyError:
            return render(request, "flights/error.html", {"message": "No selection."})
        except Flight.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No Flight."})
        except Passenger.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No passenger."})
        passenger.flights.add(flight)
        flight.seats = F('seats') - 1
        flight.save()
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
    else:
        return HttpResponse("No seats available")