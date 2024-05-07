from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView
from products.models import ProductsModel, CategoryModel, CartModel, LikeModel
from products.forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from products.handler import bot


def home_page(request):
    products = ProductsModel.objects.order_by('id')
    categories = CategoryModel.objects.order_by('id')

    # Search
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        if get_product:
            exact_product = ProductsModel.objects.filter(product_name__icontains=get_product)
            context = {'products': products, 'categories': categories, 'search_product': exact_product}
            return render(request, template_name='index.html', context=context)
    else:
        context = {'products': products, 'categories': categories}
        return render(request, template_name='index.html', context=context)

    # products = ProductsModel.objects.values_list('product_name')
    context = {'products': products, 'categories': categories}
    return render(request, template_name='index.html', context=context)


def search_products(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')  # То что искал пользователь iphone

        try:
            exact_product = ProductsModel.objects.get(product_name__icontains=get_product)
            print(f'Yeeeah we found for you this product {exact_product}')
            return redirect(f'product/{exact_product.id}')  # 5
        except:
            print('Not Found')
            return redirect('/')


def single_product(request, id):
    product = ProductsModel.objects.get(id=id)
    context = {'product': product}
    return render(request, 'single-product.html', context=context)


# class MyModelListView(ListViews):
#     model = ProductsModel
#     template_name = 'products.html'
#     context_object_name = 'products'

# class MyModelDetailView(DetailViews):
#     model = ProductsModel
#     template_name = 'single-product.html'
#     context_object_name = 'product'

# class MyModelCreateView(CreateViews):
#     model = ProductsModel
#     template_name = 'product_create.html'
#     fields = ['title','price',.......]


class MyFormView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login'


# Login html logina
class MyLoginFormView(CreateView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'


def logout_view(request):
    logout(request)
    return redirect('/')


class LogoutTemplate(TemplateView):
    template_name = 'logout.html'


def category_page(request, id):
    categories = CategoryModel.objects.get(id=id)
    products = ProductsModel.objects.filter(category=categories)

    context = {'categories': categories, 'products': products}
    return render(request, template_name='category_products.html', context=context)


def add_product_to_cart(request, id):
    if request.method == 'POST':
        checker = ProductsModel.objects.get(id=id)

        if checker.count >= int(request.POST.get('pr_count')):
            CartModel.objects.create(user_id=request.user.id,
                                     user_product=checker,
                                     user_product_quantity=int(request.POST.get('pr_count'))).save()
            return redirect('/user_cart')
        else:
            # message
            return redirect('/')

def user_cart(request):
    cart = CartModel.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        main_text = 'Новый заказ\n'

        for i in cart:
            main_text += f'Товар: {i.user_product}\n'\
            f'Кол-во: {i.user_product_quantity}\n'\
            f'ID пользователя: {i.user_id}\n'\
            f'Цена: {i.user_product.price}\n'\

            bot.send_message(-4281007230, main_text)
            cart.delete()
            return redirect('/')

    else:
        return render(request, 'cart.html', {'cart': cart})

def add_to_favorites(request, id):
    if request.method == 'POST':
        checker = ProductsModel.objects.get(id=id)

        if checker in request.POST.get('pr_name'):
            LikeModel.objects.create(user_id=request.user.id,
                                     user_product=checker).save()
            return redirect('/favorites')
        else:
            # message
            return redirect('/')

def liked_items(request):
    favorites = LikeModel.objects.filter(user_id=request.user.id)
    return render(request, 'favorites.html', {'favorites': favorites})



