import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Payment  # Assuming you have a Payment model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
import json
import logging

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Initialize logger
logger = logging.getLogger(__name__)

class SubView(APIView):
    def get(self, request):
        return render(request, "sub.html")

class HomeView(APIView):
    def get(self, request):
        return render(request, "home.html", {"razorpay_key": settings.RAZORPAY_KEY_ID})

class CreateOrderView(APIView):
    def post(self, request, plan):
        amount = int(request.data.get("amount", 0))  # Amount in paise
        if amount <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        currency = "INR"
        receipt = f"receipt_{plan}_{amount}"

        logger.debug(f"CreateOrderView: amount={amount}, currency={currency}, receipt={receipt}")

        try:
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": currency,
                "receipt": receipt,
                "payment_capture": "1"
            })

            payment = Payment.objects.create(
                razorpay_order_id=razorpay_order['id'],
                amount=amount,
                currency=currency,
                status=razorpay_order['status']
            )
            payment.save()

            logger.debug(f"CreateOrderView: Order created successfully with id={razorpay_order['id']}")

            return Response({"order_id": razorpay_order['id'], "amount": amount, "currency": currency}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"CreateOrderView: Error creating order - {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    def post(self, request):
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.status = "paid"
                payment.save()

                return Response({"message": "Payment successful", "status": payment.status}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({"error": "Invalid order ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    def get(self, request):
        logger.debug("UserView: GET request received")
        return render(request, "user.html")
    
    def post(self, request, *args, **kwargs):
        logger.debug("UserView: POST request received")
        try:
            logger.debug(f"UserView: Incoming request headers - {request.headers}")  # Log the incoming request headers
            logger.debug(f"UserView: Incoming request body - {request.body}")  # Log the incoming request body
            logger.debug(f"UserView: Incoming request data - {request.body}")  # Log the incoming request data
            user_details = json.loads(request.body)  # Log the user details received
            logger.debug(f"UserView: Received user details - {user_details}")
            name = user_details.get('name')
            address = user_details.get('address')
            email = user_details.get('email')
            company = user_details.get('company')
            price = user_details.get('price')
            plan = user_details.get('plan')
            phone = user_details.get('phone')
            password = user_details.get('password')

            logger.debug(f"UserView: Received user details - {user_details}")

            # Check if all required fields are provided and validate price
            if not all([name, address, email, company, price, plan, phone, password]) or int(price) <= 0:
                logger.error("UserView: Missing required fields")  # Log missing fields
                return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

            # Check if user already exists
            user = User.objects.filter(email=email).first()

            if user:
                logger.debug("UserView: User already registered")  # Log user registration status
                return JsonResponse({"success": True, "message": "User already registered! Logging in..."})
            else:
                # Register the new user
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()

                # Save user details to the database
                user_profile = UserProfile.objects.create(
                    user=user,
                    address=address,
                    company=company,
                    phone=phone,
                    plan=plan
                )
                user_profile.save()

                # Create an order with Razorpay
                amount = int(price) * 100  # Convert to paise
                currency = "INR"
                receipt = f"receipt_{email}"  # Use email for the receipt

                try:
                    razorpay_order = razorpay_client.order.create({
                        "amount": amount,
                        "currency": currency,
                        "receipt": receipt,
                        "payment_capture": "1"
                    })

                    logger.debug(f"UserView: Order created successfully with id={razorpay_order['id']}")

                    # Save payment details to the database (if required)
                    Payment.objects.create(
                        razorpay_order_id=razorpay_order['id'],
                        amount=amount,
                        currency=currency,
                        status=razorpay_order['status'],
                        user=user
                    )

                    return JsonResponse({
                        "success": True,
                        "message": "User registered successfully! Proceed to payment.",
                        "order_id": razorpay_order['id']
                    })
                except Exception as e:
                    logger.error(f"UserView: Error creating order - {str(e)}")  # Log order creation error
                    return JsonResponse({"success": False, "error": str(e)}, status=400)

        except Exception as e:
            logger.error(f"UserView: Error processing request - {str(e)}")  # Log request processing error
            return JsonResponse({"success": False, "error": str(e)}, status=500)

        return Response({"message": "Subscription successful"}, status=status.HTTP_200_OK)
