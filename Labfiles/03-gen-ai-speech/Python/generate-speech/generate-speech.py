import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider



def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        endpoint=os.getenv("MODEL_ENDPOINT")
        model_deployment=os.getenv("MODEL_NAME")
        speech_file_path = Path(__file__).parent / "speech.mp3"


        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(                    
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider = token_provider,
            api_version="2025-03-01-preview"
        )
        


        # Generate speech and save to file
        with client.audio.speech.with_streaming_response.create(
                    model=model_deployment,
                    #Supported values are: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 'coral', 'verse', 'ballad', 'ash', 'sage', 'marin', 'cedar', 'amuch', 'aster', 'brook', 'clover', 'dan', 'elan', 'marilyn', 'meadow', 'jazz', 'rio', 'breeze', 'cove', 'ember', 'fathom', 'glimmer', 'harp', 'juniper', 'maple', 'orbit', 'vale', 'megan-wetherall', 'jade-hardy', 'megan-wetherall-2025-03-07', and 'jade-hardy-2025-03-07'.", 'type': 'invalid_request_error', 'param': 'voice', 'code': 'invalid_value'
                    voice="dan",
                    input="My voice is my passport. I am working as Software Technical Expert in Amdocs. I have around 20 years of experience in Software Development in enterprize industry!",
                    instructions="Speak in a serious tone.",
                ) as response:
            response.stream_to_file(speech_file_path)
        


        # Play the generated speech file
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main() 
