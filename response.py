import google.generativeai as ggi
class Analyst:
    def __init__(self):
        self.model_name = "gemini-pro"
        ggi.configure(api_key="AIzaSyALcnkPFMjR09S3kiqrsdJpon71JR7yPUY")
        model = ggi.GenerativeModel(self.model_name) 
        self.chat = model.start_chat()
        self.prompt_template = """Give a very detailed analysis of the content provided delimited by triple backticks '''{user_input}''' 
        
        Give detailed analysis in this format
        Name: 
        Experience:
        Overall Analysis:
        
        """
        
    def generate_response(self, user_input):
        formatted_prompt = self.prompt_template.format(user_input=user_input)
        response = self.chat.send_message(formatted_prompt)
        return response.text

        #  Give a very detailed analysis of the content provided delimited by triple backticks.

