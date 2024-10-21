import os
import re
from openAI_client_base import OpenAIClientBase
from openai import OpenAI
import pandas as pd
import tiktoken
from tqdm import tqdm

class Embed_Deck(OpenAIClientBase):

    def __init__(self):
        super().__init__()
        self.OPENAI_API_KEY_ENV_VAR = 'OPENAI_API_KEY'
        self.DECK_TXT = 'anki.txt'
        self.MAX_TOKENS = 8000
        self.EMBEDDING_ENCODING = "cl100k_base"
        self.EMBEDDING_MODEL = "text-embedding-ada-002"

    def load_dataset(self, input_datapath):
        assert os.path.exists(input_datapath), f"{input_datapath} does not exist. Please check your file path."
        df = pd.read_csv(input_datapath, sep='\t', header=None, usecols=[0,1], names=["guid", "card"], comment='#').dropna()
        return df

    def filter_by_tokens(self, df, encoding):
        df["tokens"] = df.card.apply(lambda x: len(encoding.encode(x)))
        return df[df.tokens <= self.MAX_TOKENS]
    
    """
    Function to get embeddings for a batch of texts
    """
    def get_batch_embeddings(self, texts):
        response = self.client.embeddings.create(
            input=texts,
            model=self.EMBEDDING_MODEL
        )
        return [data.embedding for data in response.data]

    """
    Calculate embeddings for a DataFrame using batching
    """
    def calculate_embeddings(self, df, batch_size=10):
        embeddings = []
        for i in tqdm(range(0, len(df.card), batch_size), desc="Calculating embeddings", dynamic_ncols=True):
            batch = df.card[i:i+batch_size].tolist()
            embeddings.extend(self.get_batch_embeddings(batch))
        return embeddings
    
    def save_embeddings(self, df):
        output_prefix = re.search(r'.*(?=.txt$)', self.DECK_TXT).group()
        output_path = os.path.join(os.getcwd(), f'{output_prefix}_embeddings.csv')
        df.to_csv(output_path, index=False)

    def main(self):
        # Load and preprocess dataset
        input_datapath = os.path.join(os.getcwd(), self.DECK_TXT)
        df = self.load_dataset(input_datapath)
        encoding = tiktoken.get_encoding(self.EMBEDDING_ENCODING)
        df = self.filter_by_tokens(df, encoding)

        # Calculate embeddings for cards
        df["emb"] = self.calculate_embeddings(df)

        # Save embeddings to file
        self.save_embeddings(df)

deck_embedder = Embed_Deck()
deck_embedder.main()