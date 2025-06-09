from django.utils.deprecation import MiddlewareMixin

class PreventAdminSessionHijackMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            request.session["admin_logged_in"] = True
            request.session.save()
            request.session.set_expiry(3600)  # 1 час сессии для админки
            request.COOKIES["sessionid"] = request.COOKIES.get("sessionid_admin", "")
        else:
            if request.session.get("admin_logged_in"):
                request.session.flush()  # Очистка сессии при выходе из админки
