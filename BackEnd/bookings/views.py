from datetime import timedelta
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from .models import Apartment, ResidentialComplex, ALL_AMENITIES, AMENITIES_TRANSLATION, Favourite, Complaint, Feedback, Review, Booking, TopPromotion, PromotionOption, Notification
from .forms import ApartmentForm, ApartmentCreateForm, BookingForm
from django.views.generic import DetailView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY
class ResidentialComplexView(DetailView):
    model = ResidentialComplex
    template_name = "complex/complex_details.html"  # You can customize this template name
    context_object_name = "complex"  # Object name for the context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        residential_complex = self.object

        existing_amenities = residential_complex.get_existing_amenities()

        # Translate amenities to Russian (if needed)
        all_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in ALL_AMENITIES]
        existing_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in existing_amenities]

        # Find missing amenities
        missing_amenities = [amenity for amenity in all_amenities_ru if amenity not in existing_amenities_ru]

        context["existing_amenities"] = existing_amenities_ru
        context["missing_amenities"] = missing_amenities
        context["available_apartments_count"] = residential_complex.available_apartments_count()  # Number of available apartments


class ResidentalComplexListView(ListView):
    model = ResidentialComplex
    template_name = "complex/complex_list.html"
    context_object_name = "complexes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_feedbacks'] = Feedback.objects.order_by('-created_at')[:3]
        return context


class ApartmentListView(ListView):
    model = Apartment
    template_name = "complex/complex_list.html"
    context_object_name = "apartments"


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = "complex/apartment_details_new.html"
    context_object_name = "apartment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartment = self.object

        # Отзывы
        context["reviews"] = apartment.reviews.select_related('author').order_by('-created_at')

        # Занятые даты
        bookings = Booking.objects.filter(apartment=apartment)
        taken_dates = []
        for booking in bookings:
            current_date = booking.start_date
            while current_date <= booking.end_date:
                taken_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

        context["taken_dates"] = taken_dates
        context["taken_dates_json"] = json.dumps(taken_dates)

        # Удобства
        existing_amenities = apartment.amenities or []
        all_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in ALL_AMENITIES]
        existing_amenities_ru = [AMENITIES_TRANSLATION.get(amenity, amenity) for amenity in existing_amenities]
        missing_amenities = [amenity for amenity in all_amenities_ru if amenity not in existing_amenities_ru]

        context["existing_amenities"] = existing_amenities_ru
        context["missing_amenities"] = missing_amenities

        # Владелец и пользователь
        context["landlord"] = apartment.landlord
        context["user"] = self.request.user

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        apartment = self.object

        text = request.POST.get("message")
        rating = request.POST.get("rating")

        if request.user.is_authenticated and text and rating:
            Review.objects.create(
                author=request.user,
                apartment=apartment,
                text=text,
                rating=int(rating)
            )

        return redirect(apartment.get_absolute_url())


def share_with_others(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    return render(request, "complex/share_with_others.html", {"apartment": apartment})


def main_page(request, pk):
    user = get_object_or_404(User, id=pk)
    apartments = Apartment.objects.filter(status="available")  # Только доступные

    # Забираем фильтры из формы
    city = request.GET.get("city")
    complex_id = request.GET.get("complex_id")
    max_price = request.GET.get("max_price")
    room_count = request.GET.get("rooms")
    rental_type = request.GET.get("rental_type")

    # Применяем фильтры
    if city:
        apartments = apartments.filter(complex__city__icontains=city)

    if complex_id:
        apartments = apartments.filter(complex_id=complex_id)

    if max_price:
        if rental_type == "month":
            apartments = apartments.filter(price_per_month__lte=max_price)
        elif rental_type == "day":
            apartments = apartments.filter(price_per_day__lte=max_price)

    if room_count:
        if room_count == "4":
            apartments = apartments.filter(room_count__gte=4)
        else:
            apartments = apartments.filter(room_count=room_count)

    complexes = ResidentialComplex.objects.all()

    # Добавляем список ID избранных квартир
    favourite_ids = []
    if request.user.is_authenticated:
        favourite_ids = Favourite.objects.filter(user=request.user).values_list("apartment_id", flat=True)

    return render(request, "bookings/index.html", {
        "user": user,
        "apartments": apartments,
        "complexes": complexes,
        "favourite_ids": favourite_ids,
    })




class ApartmentCreateView(LoginRequiredMixin, CreateView):
    model = Apartment
    form_class = ApartmentCreateForm  # меняем на новую форму
    template_name = 'apartments/add_advertisement.html'
    success_url = reverse_lazy('apartment_list')

    def form_valid(self, form):
        form.instance.landlord = self.request.user  # Привязываем хозяина
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk  # Передаем ID пользователя
        return context



class ApartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'apartments/advertisement.html'
    success_url = reverse_lazy('booking:index')

    def get_queryset(self):
        return Apartment.objects.filter(landlord=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk  # Передаем ID пользователя
        return context


class ApartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    template_name = 'apartments/advertisement.html'
    success_url = reverse_lazy('apartment_list')

    def get_queryset(self):
        return Apartment.objects.filter(landlord=self.request.user)



def landlord_apartments(request, pk):
    apartments = Apartment.objects.filter(landlord_id=pk)
    return render(request, "apartments/advertisement.html", {
        "apartments": apartments,
    })


def delete_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)

    if request.method == 'POST':
        # Если форма подтверждения удаления была отправлена
        apartment.delete()
        return redirect('booking:index')  # После удаления редиректим на список квартир

    return render(request, 'apartments/delete.html', {'apartment': apartment})



def remove_from_favourites(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    Favourite.objects.filter(user=request.user, apartment=apartment).delete()
    return redirect('booking:favourites')  # Перенаправление на страницу избранных квартир



def favourites_view(request):
    # Получаем все избранные квартиры текущего пользователя
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'bookings/favourites.html', {'favourites': favourites})



def add_to_favourites(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user, apartment=apartment)

    if created:
        # Отправим уведомление владельцу квартиры
        Notification.objects.create(
            recipient=apartment.landlord,  # предполагаем, что есть поле owner
            sender=request.user,
            apartment=apartment,
            type='favourite',
            message=f"{request.user.username} added your apartment to favourites."
        )

    return redirect(request.META.get('HTTP_REFERER', 'booking:index'))



def toggle_favourite(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    fav, created = Favourite.objects.get_or_create(user=request.user, apartment=apartment)

    if not created:
        fav.delete()
        is_favourite = False
    else:
        is_favourite = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favourite': is_favourite})
    else:
        return redirect(request.META.get('HTTP_REFERER', 'favourites'))


def complain_clients(request, pk):
    apartment = get_object_or_404(Apartment, id=pk)


def submit_complaint(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        if not reason:
            messages.error(request, 'Пожалуйста, выберите причину жалобы.')
            return redirect('submit_complaint', apartment_id=apartment_id)

        # Проверка на уже существующую жалобу от пользователя
        if Complaint.objects.filter(user=request.user, apartment=apartment).exists():
            messages.error(request, 'Вы уже отправили жалобу на это объявление.')
            return redirect('booking:apartment_detail', pk=apartment_id)

        # Создание жалобы
        Complaint.objects.create(
            user=request.user,
            apartment=apartment,
            reason=reason
        )
        messages.success(request, 'Жалоба успешно отправлена.')
        return redirect('booking:apartment_detail', pk=apartment_id)

    # GET-запрос — показываем форму
    return render(request, 'profile/complaint.html', {'apartment': apartment})



@csrf_exempt
def submit_site_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        message = data.get('message')
        rating = data.get('rating')

        if not all([name, phone, message, rating]):
            return JsonResponse({'error': 'Все поля обязательны.'}, status=400)

        Feedback.objects.create(
            name=name,
            phone=phone,
            message=message,
            rating=int(rating)
        )
        return JsonResponse({'success': 'Фидбек успешно отправлен.'})
    return JsonResponse({'error': 'Только POST-запросы разрешены.'}, status=405)


@csrf_exempt
def submit_apartment_review(request, apartment_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        text = data.get('text')
        rating = data.get('rating')

        if not text or not rating:
            return JsonResponse({'error': 'Все поля обязательны.'}, status=400)

        apartment = Apartment.objects.get(id=apartment_id)

        Review.objects.create(
            author=user,
            apartment=apartment,
            text=text,
            rating=int(rating)
        )
        return JsonResponse({'success': 'Отзыв добавлен.'})
    return JsonResponse({'error': 'Только POST-запросы разрешены.'}, status=405)


def confirm_booking(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        type_of_booking = request.POST.get('type_of_booking')
        comment = request.POST.get('comment')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Сохраняем данные в модель Booking
        Booking.objects.create(
            apartment=apartment,
            name=name,
            status=status,
            type_of_booking=type_of_booking,
            comment=comment,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('booking:success', apartment_id=apartment.id)  # после отправки формы

    # Если GET-запрос (например, открытие шаблона), рендерим форму
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    return render(request, 'bookings/confirm_booking.html', {
        'apartment': apartment,
        'start_date': start_date,
        'end_date': end_date
    })


def successful_after_booking(request, apartment_id):
    return render(request, "bookings/successfull_booking.html", {'apartment_id': apartment_id})




def promote_success(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    option_id = request.GET.get('option_id')

    if option_id:
        option = get_object_or_404(PromotionOption, pk=option_id)

        # Проверка: есть ли уже активная промо
        active_promo = TopPromotion.objects.filter(
            apartment=apartment,
            end_date__gt=timezone.now()
        ).first()

        if not active_promo:
            apartment.is_top = True
            apartment.save()

            TopPromotion.objects.create(
                apartment=apartment,
                end_date=timezone.now() + timedelta(days=option.duration)
            )

    return redirect('apartment_create', pk=apartment_id)

def promote_cancel(request):
    return render(request, 'promotion/promotion_cancel.html')


def choose_promotion_plan(request, apartment_id):
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    options = PromotionOption.objects.all()
    descriptions = [
        "Do you want your ad to be the first? Your offer will be displayed in the top positions within 3 days!",
        "Ads marked as 'Premium' have been in the top for 15 days. These stand out and guarantee visibility.",
        "Ads marked as 'Most Premium' are in the top for 30 days and are the most visible on the platform."
    ]
    return render(request, 'payment/payment_choose.html', {
        'apartment': apartment,
        'options': zip(options, descriptions)
    })





def create_checkout_session(request, apartment_id):
    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        option = get_object_or_404(PromotionOption, pk=option_id)
        apartment = get_object_or_404(Apartment, pk=apartment_id)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'kzt',
                    'unit_amount': int(option.discounted_price * 100),
                    'product_data': {
                        'name': f'Promotion: {option.duration} дней',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('booking:promotion_success', args=[apartment_id]) + f'?option_id={option.id}'
            ),
            cancel_url=request.build_absolute_uri(
                reverse('booking:promotion_cancel')
            ),
        )
        return redirect(session.url, code=303)

    return redirect('booking:choose_promotion_plan', apartment_id=apartment_id)


def notifications_view(request):
    # Получаем все уведомления текущего пользователя
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    notifications.update(is_read=True)
    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'user_id': request.user.pk
    })


@csrf_exempt  # Применяется, чтобы обойти CSRF на момент тестирования (для улучшения безопасности уберем это позже)
def submit_review(request, apartment_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        message = data.get('message')
        rating = int(data.get('rating'))
        apartment = Apartment.objects.get(id=apartment_id)

        if not name or not phone or not message:
            return JsonResponse({'success': False, 'message': 'All fields are required!'})

        # Создание отзыва
        user, created = User.objects.get_or_create(username=name, email=phone)  # Примерно, можно улучшить логику
        review = Review.objects.create(
            author=user,
            apartment=apartment,
            text=message,
            rating=rating
        )

        return JsonResponse({'success': True, 'message': 'Review submitted successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})