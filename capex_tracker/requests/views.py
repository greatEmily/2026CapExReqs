from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Request, Theatre
from .forms import RequestForm
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta


# Create your views here.

login_required
def submit_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.requested_by = request.user
            # Assign user's theatre if applicable
            new_request.theatre = Theatre.objects.get(...)  # We'll customize this later
            new_request.save()
            return redirect('dashboard')
    else:
        form = RequestForm()
    return render(request, 'requests/submit_request.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Leadership').exists():
        requests = Request.objects.all()
    elif user.groups.filter(name='RVP').exists():
        # Filter by region (we’ll need to associate region with user or RVP)
        requests = Request.objects.filter(theatre__region='SomeRegion')  # Customize this
    elif user.groups.filter(name='Theatre').exists():
        requests = Request.objects.filter(requested_by=user)
    else:
        requests = Request.objects.none()

    return render(request, 'requests/dashboard.html', {'requests': requests})


@login_required
def reports(request):
    user = request.user
    today = now().date()

    # Base queryset
    requests_qs = Request.objects.all()

    # Role-based filtering
    if user.groups.filter(name='RVP').exists():
        # Filter by region (customize based on user-region mapping)
        requests_qs = requests_qs.filter(theatre__region='SomeRegion')
    elif user.groups.filter(name='Theatre').exists():
        requests_qs = requests_qs.filter(requested_by=user)

    # Total spend
    total_spend = sum([r.total_price for r in requests_qs])

    # Monthly spend
    start_of_month = today.replace(day=1)
    monthly_spend = sum([r.total_price for r in requests_qs.filter(request_date__gte=start_of_month)])

    # Quarterly spend (last 3 months)
    three_months_ago = today - timedelta(days=90)
    quarterly_spend = sum([r.total_price for r in requests_qs.filter(request_date__gte=three_months_ago)])

    context = {
        'total_spend': total_spend,
        'monthly_spend': monthly_spend,
        'quarterly_spend': quarterly_spend,
    }

    return render(request, 'requests/reports.html', context)
