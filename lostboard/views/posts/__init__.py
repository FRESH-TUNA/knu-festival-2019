from lostboard.views import BaseGenericViewSet
from lostboard.paginators.posts import LostboardPostsPaginator
from lostboard.serializers.posts import (
    LostboardPostsIndexSerializer
)
from lostboard.models import Post

class LostboardPostsViewSet(BaseGenericViewSet):
    pagination_class = LostboardPostsPaginator
    model = Post

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        found = self.request.GET.get('found', True)
        if found == 'false': found=False
        return self.model.objects.filter(found=found)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LostboardPostsIndexSerializer
        else:
            return LostboardPostsShowSerializer



def find(request):
    foundposts = Post.objects.filter(found=True).order_by('-created_at')
    paginator = Paginator(foundposts, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    foundposts = paginator.get_page(page)
    form = PostForm()
    return render(request,'lostboard.html', {'foundposts':foundposts, 'form':form})

def lost(request):
    findingposts = Post.objects.filter(found=False).order_by('-created_at')
    paginator = Paginator(findingposts, 10) # Show 25 contacts per page
    page = request.GET.get('page')
    findingposts = paginator.get_page(page)
    form = PostForm()
    return render(request,'lostboard.html', {'findingposts':findingposts, 'form':form})