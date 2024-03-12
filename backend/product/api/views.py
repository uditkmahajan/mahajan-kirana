from product.models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from .pagination import CategoryPagination, ProductPagination, ReviewPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView


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


# Category View - checked
class CategoryView(ListAPIView, ViewSet) :
    permission_classes = [IsAuthenticated]
    pagination_class = CategoryPagination
    queryset = Category.objects.all().order_by('name')
    
    # get all the category data
    def getCategory(self, request) :    
        category = Category.objects.all().order_by('name')
        result = get_paginated_data(self, CategorySerializer, category)
        return Response({'data' : result['results'], 'count' : result['count'], 'success' : True})
 
   
# products view  - checked
class ProductView(ListAPIView, ViewSet) :
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination
    queryset = Product.objects.all()
    
    # get all the products of the given category
    def getProducts(self, request, category) :
        products = Product.objects.filter(category__slug = category).order_by('name')
        print(products)
        if len(products) == 0 :
            return Response({'error_message' : 'Invalid category!'})
        result = get_paginated_data(self, ProductSerializer, products)
        return Response({"data" : result['results'], "count" : result['count'], "success" : True})

    # get a single product
    def getProduct(self, request, product) :
        print('getProduct product => ',product)
        try : 
            product = Product.objects.get(slug = product)
            serializer = ProductSerializer(product)
            return Response({'data' : serializer.data})
        except Exception as e :
            print('getProduct exception => ', e)
            return Response({'error_message' : 'Invalid product!'})
   

# get the selected products - checked
class SnapNShop(ViewSet) :
    permission_classes = [IsAuthenticated]
    
    def SnapNShop(self, request) :
        print('SnapNShop request.data => ', request.data)
        try :
            if len(request.data) == 0 :
                return Response({'error_message' : 'Please enter products!'})
            data = []
            for product_name in request.data :
                product = Product.objects.get(name = product_name)
                serializer = ProductSerializer(product)
                data.append(serializer.data)
            return Response({'data' : data, 'success' : True})
        except Exception as e :
            print('SnapNShop exception => ',e)
            return Response({'error_message' : 'Invalid products!'})


# product reviews views - checked
class ReviewView(ListAPIView, ViewSet) :
    permission_classes = [IsAuthenticated]
    pagination_class = ReviewPagination
    queryset = Review.objects.all().order_by('-rating')
    
    # get all the reviews of a product
    def getReviews(self, request, product) :
        reviewd = False
        reviews = Review.objects.filter(product__slug = product).order_by('-rating', '-id')
        if len(reviews) == 0 :
            return Response({'error_message' : 'No reviews!'})
        result = get_paginated_data(self, ReviewSerializer, reviews)
        if Review.objects.filter(user = request.user.id, product__slug = product).exists() :
            reviewd = True
        return Response({'data' : result['results'], 'is_reviewd' : reviewd})
    
    # create a review for a product
    def createReview(self, request, product) :
        print('createReview request.data and product => ', request.data, product)
        try :
            Review.objects.get(user = request.user.id, product__slug = product)
            return Response({'error_message' : 'User already reviewed!'})
        except Exception as e :
            try :    
                id = Product.objects.get(slug = product).id
                request.data['product'] = id
                request.data['user'] = request.user.id
                serializer = ReviewSerializer(data= request.data)
                if serializer.is_valid() :
                    serializer.save()
                    return Response({ "success" : 'Thanks for the review!' })
                return Response({"error_message" : validation_error(serializer)})
            except Exception as e :
               print('createReview exception => ',e)
               return Response({"error_message" : "Invalid product!"})
    