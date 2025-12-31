
class HuggingFaceAI:
    """Service to interact with Groq API for generating answers."""

    def __init__(self):
        self.groq_key = config('GROQ_API_KEY', default='')
        self.hf_key = settings.HUGGINGFACE_API_KEY

    def get_answer(self, question_text):
        """Generate answer for electrical machines question using Groq API."""

        # Use Groq API (fast and reliable)
        if self.groq_key:
            try:
                groq_url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "llama-3.1-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert in electrical machines, motors, transformers, and power systems. Provide clear, accurate, technical answers with examples when helpful."
                        },
                        {
                            "role": "user",
                            "content": question_text
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "top_p": 0.9
                }

                logger.info(f"Sending request to Groq API for question: {question_text[:50]}...")

                response = requests.post(
                    groq_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=30
                )

                logger.info(f"Groq API Response Status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    answer = result['choices'][0]['message']['content'].strip()

                    logger.info(f"Successfully got answer from Groq AI")

                    return {
                        'success': True,
                        'answer': answer,
                        'source': 'Llama 3.1 AI (Groq)',
                        'confidence': 0.95
                    }

                elif response.status_code == 401:
                    logger.error("Groq API: Invalid API key")
                    return {
                        'success': False,
                        'answer': 'API authentication failed. Please check your Groq API key in .env file.',
                        'error': 'Invalid API key'
                    }

                elif response.status_code == 429:
                    logger.error("Groq API: Rate limit exceeded")
                    return {
                        'success': False,
                        'answer': 'Too many requests. Please wait a moment and try again.',
                        'error': 'Rate limit'
                    }

                else:
                    logger.error(f"Groq API Error: {response.status_code} - {response.text}")
                    return {
                        'success': False,
                        'answer': f'API Error (Status {response.status_code}). Please try again.',
                        'error': response.text
                    }

            except requests.exceptions.Timeout:
                logger.error("Groq API: Request timeout")
                return {
                    'success': False,
                    'answer': 'Request timed out. Please try again.',
                    'error': 'Timeout'
                }

            except Exception as e:
                logger.error(f"Groq API Exception: {str(e)}")
                return {
                    'success': False,
                    'answer': f'Error: {str(e)}. Please check your API key and internet connection.',
                    'error': str(e)
                }
        else:
            logger.error("No Groq API key found in environment")
            return {
                'success': False,
                'answer': 'Groq API key is missing. Please add GROQ_API_KEY to your .env file.',
                'error': 'No API key'
            }
