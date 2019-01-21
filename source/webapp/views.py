from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from webapp.models import Food, Order, OrderFoods
from webapp.forms import FoodForm, OrderForm, OrdersFoodForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import User


class FoodListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Food


"""

redirect to login form for it we override dispatch method

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        else:
            return super().dispatch(request, *args, **kwargs)


"""


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    template_name = 'create_food.html'
    form_class = FoodForm
    success_url = reverse_lazy('webapp:index')


class FoodUpdateView(LoginRequiredMixin, UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm
    success_url = reverse_lazy('index')


class FoodDeleteView(LoginRequiredMixin, DeleteView):
    model = Food
    template_name = 'food_delete.html'
    success_url = reverse_lazy('webapp:index')


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.operator = self.request.user
        return super().form_valid(form)

#Order Food create view with page reloading
class OrderCreateFoodView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderFoods
    template_name = 'order_food_create.html'
    form_class = OrdersFoodForm
    permission_required = 'webapp.add_orderfoods'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return super().form_valid(form)


#Order Food create view with AJAX
class OrderFoodAjaxCreateView(CreateView, FormView):
    model = OrderFoods
    form_class = OrdersFoodForm
    permission_required = 'webapp.add_orderfoods'

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        form.instance.order = order
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk,
            'edit_url': reverse('webapp:order_ajax_update', kwargs={'pk': order_food.pk}),
            'delete_url': reverse('webapp:order_delete_food', kwargs={'pk': order_food.pk})
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
        }, status='422')




#Order Food update view with AJAX
class OrderFoodAjaxUpdateView(UpdateView, FormView):
    model = OrderFoods
    form_class = OrdersFoodForm
    permission_required = 'webapp.change_orderfoods'

    def form_valid(self, form):
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
        }, status=422)



#Order Food update view with reloading
class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderFoods
    template_name = 'order_update.html'
    form_class = OrdersFoodForm
    permission_required = 'webapp.change_orderfoods'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})


class OrderDataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_data_update.html'
    form_class = OrderForm
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView, FormView):
    model = Order
    template_name = 'order_view.html'
    form_class = OrdersFoodForm
    permission_required = 'webapp.view_order'


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'order_list.html'
    model = Order
    permission_required = 'webapp.view_order'


def delete_view(request, food_pk):
    foods = get_object_or_404(OrderFoods, pk=food_pk)
    foods.delete()
    return redirect('webapp:order_list')




class OrderFoodAjaxDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderFoods

    def delete(self, request, *args, **kwargs):
        delete_food = get_object_or_404(OrderFoods, pk=self.kwargs.get('pk'))
        print(delete_food)
        return JsonResponse({
            'pk': delete_food.pk
        })

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': get_object_or_404(OrderFoods, pk=self.kwargs.get('pk')).order.pk})




def canceled_view(request, order_pk):
    orders = get_object_or_404(Order, pk=order_pk)
    if orders:
        orders.status = 'canceled'
        orders.save()
        return redirect('webapp:order_list')


def delivery_view(request, order_pk):
    orders = get_object_or_404(Order, pk=order_pk)
    orders.courier = request.user
    if orders.status == 'preparing':
        orders.status = 'on_way'
        orders.save()
        return redirect('webapp:order_list')
    elif orders.status == 'on_way':
        orders.status = 'delivered'
        orders.save()
        return redirect('webapp:order_list')




