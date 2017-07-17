from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from .models import Post
def search(request):
    query = request.GET.get('search')
    if query:
        posts = Post.objects.all()

        search_result = posts.filter(
                                    Q(title__icontains=query)|
                                    Q(content__icontains=query)

        )

        if search_result:
            return {'search_result':search_result,}
        else:
            return {'search_result':'custom_not_found',}
    else:
        return {'search_result':None,}