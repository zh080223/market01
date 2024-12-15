from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response


def goods_list_cache_set(expire):
    def _cache_set(func):
        def wrapper(request, *args, **kwargs):
            login_user = request.user
            full_path = request.get_full_path()
            if login_user.is_superuser:
                cache_key = 'goods_list_cache_super_%s' % full_path
            else:
                cache_key = 'goods_list_cache_%s' % full_path
            print(cache_key)
            # 如果有
            res = cache.get(cache_key)
            if res:
                print('cache in')
                return Response(res, status=status.HTTP_200_OK)

            res = func(request, *args, **kwargs)
            cache.set(cache_key, res.data, expire)
            return res

        return wrapper

    return _cache_set
