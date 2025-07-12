from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .ai_agent import chat_with_agent

# Create your views here.

class GenAIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question is required"}, status=400)
        
        try:
            answer = chat_with_agent(question)
            return Response({"question": question, "answer": answer})
        except Exception as e:
            return Response({"error": f"AI Agent error: {str(e)}"}, status=500)
        






