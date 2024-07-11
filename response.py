import google.generativeai as ggi
class Analyst:
    def __init__(self):
        self.model_name = "gemini-pro"
        ggi.configure(api_key="AIzaSyALcnkPFMjR09S3kiqrsdJpon71JR7yPUY")
        model = ggi.GenerativeModel(self.model_name) 
        self.chat = model.start_chat()
        self.prompt_template = """You are a job resume analyser .Give a very detailed analysis of the content provided delimited by triple backticks '''{user_input}''' 
        Compare query that tells the requirement with the resume content and give highlights as a job recruiter and give suggestion about the capability for the required role based on query on overall analysis in the format. keep it concise max 5 points.
        query : {query}

        Give detailed analysis in this format
        Name: 
        Email:
        Location:
        Experience:
        Overall Analysis:
         
        
        
        """
        
    def generate_response(self, user_input,query):
        formatted_prompt = self.prompt_template.format(user_input=user_input,query = query)
        response = self.chat.send_message(formatted_prompt)
        return response.text
    def generate_list(self, query):
        prompt = """convert the given query to grouped terms.
        Instruction :
        - remove  stop words and unnecessary words
        - the query will be a description to fetch the right resume so group the terms appropriately in to a list and correct typo if necessary.
        - the list will be used for highlighting the importsant terms of resume so group them correctly
        - example1 : query = 'machine learning engineer with 3 years experience' output =  ['machine learning', 'engineer', '3 years' ]
        - example2 : query = 'aws engineer' output = ['aws engineer']
        query : {query}
        """
        formatted_prompt = prompt.format(query=query)
        response = self.chat.send_message(formatted_prompt)
        print(response.text)
        return response.text
    

        #  Give a very detailed analysis of the content provided delimited by triple backticks.

