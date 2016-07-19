from django.contrib import admin

class DeleteNotAllowedModelAdmin(admin.ModelAdmin):
    # Other stuff here
    def has_delete_permission(self, request, obj=None):
        return False


class AddNotAllowedModelAdmin(admin.ModelAdmin):
    # Other stuff here
    def has_add_permission(self, request):
        return False