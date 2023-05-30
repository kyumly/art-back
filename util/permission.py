from rest_framework import permissions

from art.models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    글 작성자만 수정 및 삭제할 수 있도록 권한 설정
    """

    def has_object_permission(self, request, view, obj : Post):
        # GET, HEAD, OPTIONS 요청은 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # DELETE 요청을 하는 사용자가 글 작성자인지 확인
        return obj.user == request.user