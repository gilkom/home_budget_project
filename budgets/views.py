from django.shortcuts import render

# Create your views here.
def index(request):
    """Main page for budgets app."""
    return render(request, 'budgets/index.html')
