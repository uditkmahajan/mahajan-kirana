from order.models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from django.utils import timezone


# return the serializer.errors
def validation_error(serializer) : 
    for i,j in serializer.errors.items() :
            value = j[0]
            key = i 
    return key + ' : ' + value


# get the data after pagination
def get_paginated_data(self, serializer, data) :
    serializer = serializer(data, many = True)
    data = self.paginate_queryset(serializer.data)
    result = self.get_paginated_response(data).data
    return result

# order view - checked
class OrderView(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    # get all the order list
    def getAllOrder(self, request) :
        order = Order.objects.filter(user = request.user.id, is_completed = True).order_by('-created_at')
        if len(order) == 0 :
            return Response({'error_message' : 'You do not place any order yet!'})
        serializer = OrderSerializer(order , many = True)
        print(serializer.data)
        return Response({'data' : serializer.data, 'total_order' : len(order), 'success' : True})
    
    # get the items of order with id = pk
    def getOrderItems(self, request, pk) :
        # pk = order id
        print('getOrderItems pk => ', pk)
        try :
            items = OrderItem.objects.filter(order = pk)
            if len(items) == 0 :
                return Response({'error_message' : 'Oops! No item in the order!'})
            serializer = OrderItemSerializer(items, many = True)
            return Response({'data' : serializer.data, 'success' : True})
        except Exception as e :
            print('getOrderItems exception => ',e)
            return Response({'error_message' : 'Invalid Order Id!'})
       
       
# cart view - checked 
class CartView(ViewSet) :
    permission_classes = [IsAuthenticated]

    # get the cart items
    def getCartItems(self, request) :
        try : 
            order = Order.objects.get(user = request.user, is_completed = False)
            items = OrderItem.objects.filter(order = order.id)
            if len(items) == 0: 
                return Response({'error_message' : 'No item in the cart!'})
            serializer = OrderItemSerializer(items, many = True)
            return Response({'data' : serializer.data, 'total_price' : order.total_price, 'success' : True})
        except Exception as e :
            print('getCartItems exception => ', e)
            return Response({'error_message' : 'No item in the cart!'})
        
    # add items to the cart
    def addCartItem(self, request) : 
        print('addCartItem request.data => ', request.data) 
        try :
            int(request.data['product']) and int(request.data['quantity']) and Product.objects.get(pk=request.data['product'])
        except Exception as e :
            print('addCartItem exception => ', e)
            return Response({'error_message' : 'Invalid fields!'})
        order, created = Order.objects.get_or_create(user = request.user, is_completed = False)
        try :
            item = OrderItem.objects.filter(product = request.data['product'], order = order.id).first()
            if item != None : 
                product_price = Product.objects.get(pk = request.data['product']).price
                item.quantity = item.quantity + int(request.data['quantity'])
                item.price = item.price + (product_price * int(request.data['quantity']))
                order.total_price = order.total_price + ( product_price * int(request.data['quantity']))
                item.save(force_insert = True, using = "my db")
                order.save()
                return Response({'success' : 'Product updated!'})
            else :
                request.data['price'] = 10
                request.data['order'] = order.id
                serializer = OrderItemSerializer(data = request.data)
                if serializer.is_valid() :
                    serializer.save()
                    return Response({'success' : 'Product added!'})
                else :
                    return Response({"error_message" : validation_error(serializer)})
        except Exception as e :
            print('addCartItem exception => ',e)
            return Response({'error_message' : 'Oops! can not perform opertaion, Please try again.'})
            
    # delete the cart item
    def deleteCartItem(self, request) :
        print('deleteCartItem request.query_params => ', request.query_params) 
        try :
            if request.query_params.get('item') != None and request.query_params.get('order') != None :
                item_id = request.query_params['item']
                order_id = request.query_params['order']
                item = OrderItem.objects.get(pk = item_id, order = order_id)
                order = Order.objects.get(pk = order_id)
                order.total_price = order.total_price - item.price
                order.total_item = order.total_item - 1
                item.delete()
                order.save()
                return Response({'success' : 'Item deleted!'})
            else :
                return Response({'error_message' : 'All the fields are required!'})
        except Exception as e :
            print('deleteCartItem exception => ', e)
            return Response({'error_message' : 'Can not perform action! please try again.'})
     
        # 
   
    # increase or decrease item quantity    
    def updateCartItem(self, request) :
        print('updateCartItem request.query_params => ', request.query_params)
        try :
            if request.query_params.get('item') != None and request.query_params.get('type') and request.query_params.get('order') != None :   
                order = Order.objects.get(pk = request.query_params['order'])
                item = OrderItem.objects.get(order = request.query_params['order'], pk = request.query_params['item'])
                product_price = Product.objects.get(pk = item.product.id).price
                if request.query_params['type'] == 'inc' :
                    item.quantity = item.quantity + 1 
                    item.price = item.price + product_price
                    order.total_price = order.total_price + product_price 
                elif request.query_params['type'] == 'dec' and item.quantity > 1  :
                    item.quantity = item.quantity - 1 
                    item.price = item.price - product_price
                    order.total_price = order.total_price - product_price
                item.save(force_insert= True, using = "my db")
                order.save()
                return Response({'success' : 'Item updated!'})
            else :
                return Response({'error_message' : 'All the fields are required!'})
        except Exception as e :
            print('updateCartItem exception => ',e)
            return Response({'error_message' : 'Can not perform action! please try again.!'})
        

# complete the order view - checked
class OrderCompleteView(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    # order complete 
    def orderComplete(self, request) :
        print('orderComplete request.query_params => ', request.query_params)
        try : 
            order, created = Order.objects.get_or_create(user = request.user, is_completed = False)
            if request.data['additional'] == '' :
                del request.data['additional']
            request.data['is_completed'] = True
            request.data['created_at'] = timezone.now()
            serializer = OrderSerializer(order, data = request.data, partial = True) 
            if serializer.is_valid() :
                 serializer.save()
                 for i in OrderItem.objects.filter(order = order.id) :
                     print(i.product.offer)
                     i.item_offer = i.product.offer
                     i.save(force_insert= True, using = "my db")
                 return Response({'success' : 'Thank you for shopping!'})
            else :
                print('orderComplete exception => ',validation_error(serializer))
                return Response({'error_message' : validation_error(serializer)})
        except Exception as e :
            print('orderComplete exception => ', e)
            return Response({'error_message' : 'Invalid order id!'}) 
