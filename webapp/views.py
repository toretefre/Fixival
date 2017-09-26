from django.shortcuts import render

def post_list(request):
    return render(request, 'templates/oversiktsview_konserter', {})
