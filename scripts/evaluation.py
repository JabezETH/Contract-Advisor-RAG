# Importing libraries
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from datasets import Dataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from dotenv import load_dotenv
load_dotenv()

def generate_syntetic_testdata(file_path):
    loader = DirectoryLoader(file_path)
    documents = loader.load()
    # generator with openai models
    generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
    critic_llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    embeddings = OpenAIEmbeddings()

    generator = TestsetGenerator.from_langchain(
        # rag_chain,
        generator_llm,
        critic_llm,
        embeddings
    )

    # generate testset
    testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25})
    test_data = testset.to_pandas()
    test_data.to_csv("/home/jabez/week_11/Contract-Advisor-RAG/test_data/test_data.csv", index=False)
    return test_data

def adding_answer_to_testdata(test_data, rag_pipeline, vector, retriever):
    questions = test_data['question'].to_list()
    ground_truth = test_data['ground_truth'].to_list()
    data = {'question': [], 'answer': [], 'contexts': [], 'ground_truth': ground_truth}
    
    for query in questions:
        data['question'].append(query)
        
        # Generate the chatbot response
        data['answer'].append(rag_pipeline(vector, query))
        
        # Retrieve relevant documents
        data['contexts'].append([doc.page_content for doc in retriever.get_relevant_documents(query)])
    
    df = pd.DataFrame(data)
    dataset = Dataset.from_pandas(df)
    return dataset

def ragas_evaluator(dataset):
    from ragas.metrics import (
        answer_relevancy,
        faithfulness,
        context_recall,
        context_precision,
    )

    from ragas import evaluate

    result = evaluate(
        dataset = dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevancy,
            context_recall,
        ],
    )
    result
    evaluation_result = result.to_pandas()
    return evaluation_result

def heatmap_plot(evaluation_result):
    heatmap_data = evaluation_result[['context_precision', 'faithfulness', 'answer_relevancy', 'context_recall']]
    cmap = LinearSegmentedColormap.from_list('green_red', ['red','green'])
    plt.figure(figsize=(10,8))
    sns.heatmap(heatmap_data, annot=True, fmt='.2f', linewidths=5, cmap=cmap)
    plt.yticks(ticks=range(len(evaluation_result['question'])), labels=evaluation_result['question'], rotation=0)
    plt.show

# preparing test dataset from the given file
generated_test_data ={
'question':[
'Under what circumstances and to what extent the Sellers are responsible for a breach of representations and warranties?',
'How much is the escrow amount?',
'Is escrow amount grete then the Retention Amount ?',
'What is the purpose of the escrow?',
'May the Escrow Amount serve as a recourse for the Buyer in case of breach of representations by the Company?',
'Are there any conditions to the closing?',
'Are Change of Control Payments considered a Seller Transaction Expense?',
'Would the aggregate amount payable by the Buyer to the Sellers be affected if it is determined that the actual Closing Debt Amount is greater the estimated Closing Debut Amount?',
'Does the Buyer need to pay the Employees Closing Bonus Amount directly to the Company employees?',
'Does any of the Sellers provide a representation with respect to any Tax matters related to the Company?',
'Is any of the Sellers bound by a non-competition covenant after the Closing?',
'Whose consent is required for the assignment of the Agreement by the Buyer?',
'Does the Buyer needs the Sellers consent in the event of an assignment of the Agreement to a third party who is not a Buyer’s Affiliates?'
],
'ground_truth':[
'Except in the case of fraud, the Sellers have no liability for breach of representations and warranties',
'The escrow amount is equal to $1,000,000.',
'No.',
'To serve as a recourse of the Buyer in case of post-closing adjustments of the purchase price.',
'No',
'No, as the signing and closing are simultaneous.',
'Yes.',
'Yes.',
'No.',
'No. Only the Company provides such a representation.',
'No.',
'If the assignment is to an Affiliate or purchaser of all of the Buyers assets, no consent is required. Otherwise, the consent of the Company and the Seller Representative is required.',
'No. If the assignment is not part of a sale of all or substantially all of the Buyer’s assets, the assignment requires the consent of the Company and the Seller’s Representative.'
]
}
generated_test_df = pd.DataFrame(generated_test_data)
generated_test_df.to_csv("/home/jabez/week_11/Contract-Advisor-RAG/test_data/generated_test_data.csv", index=False) 