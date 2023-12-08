from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DonorUserForm, DonorForm, DonationForm
from .models import Donor, BloodDonate

def your_view(request):
    if request.method == 'POST':
        user_form = DonorUserForm(request.POST)
        donor_form = DonorForm(request.POST)
        donation_form = DonationForm(request.POST)
        if user_form.is_valid() and donor_form.is_valid() and donation_form.is_valid():
            # Save the user form data without committing to the database yet
            user = user_form.save(commit=False)
            # Set the password for the user
            user.set_password(user_form.cleaned_data['password'])
            user.save()  # Save the user to the database now

            donor = donor_form.save(commit=False)
            donor.user = user
            donor.save()

            donation = donation_form.save(commit=False)
            donation.donor = donor
            donation.save()

            # Sending email to the donor
            subject = 'Thank you for your donation!'
            message = 'Dear {},\n\nThank you for your generous donation.'.format(user.first_name)
            sender_email = 'your_email@example.com'  # Update with your sender email
            send_mail(subject, message, sender_email, [user.email])

            # Redirect to a success page or do something else
            return HttpResponseRedirect('/thank-you/')  # Redirect to a 'thank you' page
    else:
        user_form = DonorUserForm()
        donor_form = DonorForm()
        donation_form = DonationForm()

    return render(request, 'your_template.html', {
        'user_form': user_form,
        'donor_form': donor_form,
        'donation_form': donation_form,
    })
