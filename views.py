import os
import json
from time import sleep
from .chat_logic import get_chat_response



@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        response_text, is_tableview = get_chat_response(user_input, request.session)

        print(f"###   {is_tableview}   ###")

        print(response_text)
        return JsonResponse({"response": response_text})
        
    return JsonResponse({"message": "Welcome to the ennoda chatapp😁"})