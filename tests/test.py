import unittest
from unittest.mock import MagicMock, patch
from langchain_core.schema import Document

class TestPipelines(unittest.TestCase):

    def setUp(self):
        # Mock vectorstore
        self.mock_vectorstore = MagicMock()
        self.mock_retriever = MagicMock()
        self.mock_vectorstore.as_retriever.return_value = self.mock_retriever

        # Mock documents returned by the retriever
        self.mock_docs = [Document(page_content=f"Content of document {i}") for i in range(6)]
        self.mock_retriever.map.return_value = [self.mock_docs]
        self.mock_retriever.return_value = self.mock_docs

    @patch('your_module_path.ChatOpenAI', autospec=True)
    def test_simple_pipeline(self, MockChatOpenAI):
        # Mock LLM response
        mock_llm = MockChatOpenAI.return_value
        mock_llm.invoke.return_value = "Mocked LLM Answer"

        question = "What is the contract duration?"

        # Call the function
        answer = simple_pipeline(self.mock_vectorstore, question)

        # Assertions
        self.assertEqual(answer, "Mocked LLM Answer")
        MockChatOpenAI.assert_called_once()

    @patch('your_module_path.ChatOpenAI', autospec=True)
    def test_multi_query_pipeline(self, MockChatOpenAI):
        # Mock LLM response
        mock_llm = MockChatOpenAI.return_value
        mock_llm.invoke.return_value = "Mocked multi-query LLM Answer"

        question = "What are the payment terms?"

        # Call the function
        answer = multi_query_pipeline(self.mock_vectorstore, question)

        # Assertions
        self.assertEqual(answer, "Mocked multi-query LLM Answer")
        MockChatOpenAI.assert_called_once()

    @patch('your_module_path.ChatOpenAI', autospec=True)
    def test_rag_fusion(self, MockChatOpenAI):
        # Mock LLM response
        mock_llm = MockChatOpenAI.return_value
        mock_llm.invoke.return_value = "Mocked RAG Fusion Answer"

        question = "Is there a termination clause?"

        # Call the function
        answer = rag_fusion(self.mock_vectorstore, question)

        # Assertions
        self.assertEqual(answer, "Mocked RAG Fusion Answer")
        MockChatOpenAI.assert_called_once()


if __name__ == '__main__':
    unittest.main()
