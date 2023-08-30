# admin_detection_middleware.py

class AdminDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/login/':
            # Check if the submitted username and password belong to an admin
            if request.POST.get('username') == 'admin_username' and request.POST.get('password') == 'admin_password':
                request.session['is_admin'] = True
            else:
                request.session['is_admin'] = False

        response = self.get_response(request)
        return response
