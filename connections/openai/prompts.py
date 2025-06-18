

class OpenAIPrompts:

    def __init__(self, client):
        """Initialize an OpenAI Client"""
        self.client = client

    def generate_product_title_for_ebay(self, **kwargs):

        input_str = ""
        for key, value in kwargs.items():
            input_str += f"{key}: {value}\n"

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "You are a product title generator for an eCommerce store. "
                    "Ebay marketplace to be exact. The title has to be in German language."
                )},
                {"role": "user", "content": (
                    "Generate a product title with the following constraints:\n"
                    "- Make it as long as possible, up to 75 characters.\n"
                    "- Include: Product type, Compatibility, Brand, and Color.\n"
                    "- Prioritize clarity and SEO keywords.\n"
                    "- Output only the title, no extra text.\n\n"
                    "Input:\n"
                    f"{input_str}"
                )}
            ]
        )

        answer = response.choices[0].message.content
        print(answer)

        return answer