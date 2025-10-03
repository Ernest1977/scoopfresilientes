from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from . models import Blog, Category, Gallery, Contact, Comment
from django.contrib import messages
from . forms import ContactForm

def index(request):
    post = Blog.objects.order_by('-id')
    main_post = Blog.objects.order_by('-id').filter(Main_post=True)[0:1]
    recent_news = Blog.objects.filter(section='Recent').order_by('-id')[:5]
    popular = Blog.objects.filter(section='Popular').order_by('-id')[0:5]
    edition = Blog.objects.order_by('-id').filter(Main_post=True)[0:1]
    prodserv = edition = Blog.objects.order_by('-id').filter(section='Prodserv')[0:4]
    prodserv1 = edition = Blog.objects.order_by('-id').filter(section='Prodserv1')[0:4]
    category = Category.objects.all()
    blog_cat = Category.objects.all()
    context = {
        'post' : post,
        'recent_news': recent_news,
        'category' : category,
        'main_post' : main_post,
        'blog_cat' : blog_cat,
        'popular' : popular,
        'edition' : edition,
        'prodserv' : prodserv,
        'prodserv1' : prodserv1
    }
    


    return render(request, 'index.html', context)

def blog_detail(request, slug):
    posts = Blog.objects.order_by('-id')[:5]
    if not posts:
        raise Http404
    
    category = Category.objects.all()
    recent_news = Blog.objects.filter(section='Recent_news').order_by('-id')[:5]
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:5]
    prodserv = Blog.objects.filter(section='Prodserv').order_by('-id')[:2]
    prodserv1 = Blog.objects.filter(section='Prodserv1').order_by('-id')[:2]
    edition = Blog.objects.filter(section='Edition').order_by('-id')[:1]
    share_url = request.build_absolute_uri(reverse('blog_detail', args=[slug]))
    post = get_object_or_404(Blog, blog_slug=slug)

    comments = Comment.objects.filter(blog_id=post.id).order_by('-date')   
    # Handling the comment section here.


    
    context = {
        'post': post,
        'share_url': share_url,
        'posts': posts,
        'category': category,
        'Recent_news': recent_news, 
        'comments': comments,
        'popular': popular,
        'prodserv' : prodserv,
        'prodserv1' : prodserv1,
        'edition' : edition
    }

    return render(request, "blog_detail.html", context)


def category(request, slug):

       cat = Category.objects.all()
       blog_cat = Category.objects.filter(slug=slug)
       context = {
       'cat' : cat,
       'active_category' :slug,
       'blog_cat' : blog_cat,              
       }

        
       return render(request, 'category.html', context)


def add_comment(request,slug):
     
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug = slug)
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        website = request.POST.get('InputWeb')
        comment_text = request.POST.get('InputComment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None
        
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post= post,
            name=name,
            email=email,
            website=website,
            comment=comment_text,
            parent=parent_comment
        )
        return redirect('blog_detail',slug=post.blog_slug)
    return redirect('blog_detail')
    
 
def about(request):
    return render(request, 'about.html', {'about': about})

def produits(request):
    return render(request, 'produits.html', {'produits': produits})

#def contact(request):
#   if request.method=="POST":
#       fname= request.POST.get("name")
#       femail= request.POST.get("email")
#       phone= request.POST.get("phone")
#       desc= request.POST.get("desc")
#       query = Contact(name=fname, email=femail, phoneNumber=phone, description=desc)
#       query.save()
#       messages.info(request,"Merci de nous avoir contacté! Nous vous répondrons sous peu...")
#       return redirect('contact')
#   return render(request, 'contact.html')

def contact(request):
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Merci de nous avoir contacté! Nous vous répondrons sous peu...")
            return redirect('index')
    form = ContactForm
    context = {'form' : form,}
    return render(request, 'contact.html', context)

def gallery(request):
    gallery = Gallery.objects.order_by('-id')

    context = {
        'gallery': gallery,
    }

   
    return render(request, 'gallery.html', context)
