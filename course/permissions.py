from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCourseTeacherOrAdmin(BasePermission):
    """
    SAFE methods (GET/HEAD/OPTIONS) → anyone.
    POST              → authenticated teacher OR admin.
    PUT/PATCH/DELETE  → the teacher who owns the course OR an admin.
    """
#     When a request hits /api/courses/{id}/ or /api/courses/:

#     ✅ Step 1: has_permission(request, view) runs first

    def has_permission(self, request, view): #permission check
        # autheticated users 
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        # You can swap `.role` for groups/flags—keep the logic identical.
        return request.user.role in ("teacher", "admin")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: # read-only access
            return True

        user = request.user
        if user.role == "admin": # admin can modify any course
            return True

        return user.role == "teacher" and obj.instructor_id == user.id
        #only the teacher who owns the course can modify it
        #or an admin can modify any course

