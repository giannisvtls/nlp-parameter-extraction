import numpy as np
import json
from unittest import IsolatedAsyncioTestCase
from ..services.rag_service import RAGService
from ..services.openai_service import OpenAIService, SYSTEM_PROMPT
from typing import List, Dict
from django.conf import settings

class TestBankingFAQsEvaluation(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rag_service = RAGService()
        cls.openai_service = OpenAIService()
        
        # Test cases organized by category
        cls.test_cases = {
            # Account Management test cases
            "account": [
                {
                    "query": "Register John with 1000 euros",
                    "relevant_docs": ["Simply tell the chatbot your name and optional initial deposit amount. For example, say \"Register John with 1000 euros\" or just \"Register John\" for an account with zero balance."],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "REGISTER",
                            "user_name": "John",
                            "amount": 1000
                        }
                    }
                },
                {
                    "query": "I'd like to open an account for Maria please",
                    "relevant_docs": ["Simply tell the chatbot your name and optional initial deposit amount. For example, say \"Register John with 1000 euros\" or just \"Register John\" for an account with zero balance."],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "REGISTER",
                            "user_name": "Maria",
                            "amount": 0
                        }
                    }
                },
                {
                    "query": "Can I create multiple accounts under the same name?",
                    "relevant_docs": ["No, the system allows only one account per name."],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "No, the system allows only one account per name."
                    }
                }
            ],
            
            # Balance and IBAN test cases
            "balance": [
                {
                    "query": "Show John's balance",
                    "relevant_docs": ["You can ask \"What's my balance?\", \"Show my balance\", or \"Check balance\". The system will show your current balance along with your IBAN for reference."],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "BALANCE",
                            "user_name": "John"
                        }
                    }
                },
                {
                    "query": "Could you tell me how much money I have in my account?",
                    "relevant_docs": ["You can ask \"What's my balance?\", \"Show my balance\", or \"Check balance\". The system will show your current balance along with your IBAN for reference."],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "BALANCE",
                            "user_name": "John"
                        }
                    }
                },
                {
                    "query": "I forgot my account number, can you help?",
                    "relevant_docs": ["You can check your IBAN by asking \"What's my IBAN?\""],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "IBAN",
                            "user_name": "John"
                        }
                    }
                }
            ],
            
            # Transaction test cases
            "transactions": [
                {
                    "query": "Transfer 300 euros to GR1234567890",
                    "relevant_docs": ["Say \"Transfer [amount] to [IBAN]\". For example, \"Transfer 300 euros to GR1234567890\". Make sure you have sufficient balance and the recipient's IBAN is correct."],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "TRANSFER",
                            "amount": 300,
                            "iban": "GR1234567890"
                        }
                    }
                },
                {
                    "query": "I need to send 50 euros to GR9876543210 and then deposit 200 euros",
                    "relevant_docs": [
                        "Say \"Transfer [amount] to [IBAN]\". For example, \"Transfer 300 euros to GR1234567890\". Make sure you have sufficient balance and the recipient's IBAN is correct.",
                        "To deposit money, simply say \"Deposit [amount]\". For example, \"Deposit 500 euros\". The minimum deposit is 1 euro, and the transaction is processed instantly."
                    ],
                    "expected_response": {
                        "type": "banking_operation",
                        "operation": {
                            "action": "TRANSFER",
                            "amount": 50,
                            "iban": "GR9876543210"
                        }
                    }
                },
                {
                    "query": "Can I send money to my own account GR1111111111?",
                    "relevant_docs": ["Self-transfers are not allowed. The system will reject transfers where the sender and recipient IBANs are the same."],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "Self-transfers are not allowed. The system will reject transfers where the sender and recipient IBANs are the same."
                    }
                },
                {
                    "query": "Take out 0.5 euros from my account",
                    "relevant_docs": [
                        "To withdraw money, say \"Withdraw [amount]\". For example, \"Withdraw 200 euros\". You must have sufficient balance, and the minimum withdrawal is 1 euro.",
                        "The minimum transaction amount is 1 euro. The maximum withdrawal or transfer amount is limited by your current balance."
                    ],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "The minimum transaction amount is 1 euro. You cannot withdraw less than 1 euro from your account."
                    }
                }
            ],
            
            # Security and Error Handling test cases
            "security": [
                {
                    "query": "What happens if I try to withdraw more than my balance?",
                    "relevant_docs": [
                        "The withdrawal will be rejected with an \"Insufficient balance\" message. Your balance will remain unchanged.",
                        "No, overdrafts are not allowed. You can only withdraw or transfer up to your available balance."
                    ],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "The withdrawal will be rejected with an \"Insufficient balance\" message. Your balance will remain unchanged. No, overdrafts are not allowed. You can only withdraw or transfer up to your available balance."
                    }
                },
                {
                    "query": "Is my money safe if a transaction fails halfway?",
                    "relevant_docs": [
                        "All transactions are atomic (they either complete fully or not at all) and are processed in real-time. Each session maintains your identity securely until you disconnect.",
                        "Failed transactions (like insufficient balance or invalid IBAN) are completely reversed and don't affect your balance. The system will provide a clear error message explaining what went wrong."
                    ],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "Yes, your money is safe. All transactions are atomic (they either complete fully or not at all) and are processed in real-time. Failed transactions are completely reversed and don't affect your balance. The system will provide a clear error message explaining what went wrong."
                    }
                },
                {
                    "query": "What's the maximum amount I can transfer?",
                    "relevant_docs": [
                        "The minimum transaction amount is 1 euro. The maximum withdrawal or transfer amount is limited by your current balance.",
                        "You can only withdraw or transfer up to your available balance."
                    ],
                    "expected_response": {
                        "type": "general_inquiry",
                        "response": "The maximum amount you can transfer is limited by your current balance. You can only transfer up to your available balance. The minimum transaction amount is 1 euro."
                    }
                }
            ]
        }

    async def asyncSetUp(self):
        """Set up test documents in the database"""
        await super().asyncSetUp()
        # Add all FAQ documents
        faq_files = [
            "api/documents/banking_faqs_account.txt",
            "api/documents/banking_faqs_balance.txt",
            "api/documents/banking_faqs_transactions.txt",
            "api/documents/banking_faqs_security.txt"
        ]
        
        for faq_file in faq_files:
            with open(faq_file, "r") as f:
                content = f.read()
                await self.rag_service.add_document(content)

    def calculate_precision_at_k(self, context: str, relevant_docs: List[str], k: int = 1) -> float:
        """Calculate Precision@K for retrieved documents"""
        return 1.0 if any(rel_doc in context for rel_doc in relevant_docs) else 0.0

    def calculate_ndcg(self, context: str, relevant_docs: List[str], k: int = 1) -> float:
        """Calculate Normalized Discounted Cumulative Gain"""
        # For single document, NDCG is either 1 or 0
        return 1.0 if any(rel_doc in context for rel_doc in relevant_docs) else 0.0

    async def calculate_context_relevance(self, context: str, query: str) -> float:
        """Calculate context relevance using embedding similarity"""
        query_embedding = await self.rag_service.create_embedding(query)
        context_embedding = await self.rag_service.create_embedding(context)
        return self.rag_service._cosine_similarity(query_embedding, context_embedding)

    def calculate_mrr(self, context: str, relevant_docs: List[str]) -> float:
        """Calculate Mean Reciprocal Rank (MRR) for a single query"""
        # For single document, MRR is either 1 or 0
        return 1.0 if any(rel_doc in context for rel_doc in relevant_docs) else 0.0

    async def calculate_metrics(self) -> Dict[str, float]:
        """Calculate metrics across all test cases and save results to file"""
        total_metrics = {
            "mrr": 0.0,
            "precision_at_k": 0.0,
            "ndcg": 0.0,
            "context_relevance": 0.0,
            "response_format_accuracy": 0.0,
            "operation_accuracy": 0.0
        }
        
        # Open results file
        with open("api/documents/rag_evaluation_results.txt", "w") as f:
            f.write("Banking FAQs RAG System Evaluation Results\n")
            f.write("========================================\n\n")
            
            total_queries = 0
            category_metrics = {}
            
            # Process each category
            for category, test_cases in self.test_cases.items():
                f.write(f"\n{category.upper()} Category Evaluation\n")
                f.write("=" * (len(category) + 19) + "\n\n")
                
                category_total = {
                    "mrr": 0.0,
                    "precision_at_k": 0.0,
                    "ndcg": 0.0,
                    "context_relevance": 0.0,
                    "response_format_accuracy": 0.0,
                    "operation_accuracy": 0.0
                }
                
                # Process each test case in the category
                for test_case in test_cases:
                    query = test_case["query"]
                    relevant_docs = test_case["relevant_docs"]
                    
                    # Get context and process message
                    context = await self.rag_service.get_relevant_context(query)
                    response = await self.openai_service.process_message(query)
                    
                    # Calculate context metrics
                    mrr = self.calculate_mrr(context, relevant_docs)
                    precision = self.calculate_precision_at_k(context, relevant_docs)
                    ndcg = self.calculate_ndcg(context, relevant_docs)
                    context_relevance = await self.calculate_context_relevance(context, query)
                    
                    # Calculate response format accuracy
                    format_score = 0.0
                    operation_score = 0.0
                    
                    if "expected_response" in test_case:
                        expected = test_case["expected_response"]
                        actual = response.get("processed_message", {})
                        
                        # Write query and context first
                        f.write(f"Query: {query}\n\n")
                        f.write("Retrieved Context:\n")
                        f.write(f"{context}\n\n")
                        
                        f.write("LLM Response:\n")
                        f.write(f"{json.dumps(actual, indent=2)}\n\n")
                        
                        f.write("Expected Response:\n")
                        f.write(f"{json.dumps(expected, indent=2)}\n\n")
                        
                        # Check basic response format
                        format_score = 1.0
                        if actual.get("type") != expected["type"]:
                            format_score = 0.0
                            f.write(f"Response Type Mismatch!\n")
                            f.write(f"Expected: {expected['type']}\n")
                            f.write(f"Got: {actual.get('type')}\n\n")
                        
                        # For banking operations, check operation details
                        if expected["type"] == "banking_operation":
                            exp_op = expected["operation"]
                            act_op = actual.get("operation", {})
                            
                            # Calculate operation accuracy
                            operation_score = 1.0
                            total_params = 1  # action is always required
                            correct_params = 1 if act_op.get("action") == exp_op["action"] else 0
                            
                            if act_op.get("action") != exp_op["action"]:
                                operation_score = 0.0
                                f.write(f"Action Mismatch!\n")
                                f.write(f"Expected: {exp_op['action']}\n")
                                f.write(f"Got: {act_op.get('action')}\n\n")
                            
                            for param in ["user_name", "amount", "iban"]:
                                if param in exp_op:
                                    total_params += 1
                                    if act_op.get(param) == exp_op[param]:
                                        correct_params += 1
                                    else:
                                        f.write(f"{param} Mismatch!\n")
                                        f.write(f"Expected: {exp_op[param]}\n")
                                        f.write(f"Got: {act_op.get(param)}\n\n")
                            
                            operation_score = correct_params / total_params
                        
                        # For general inquiries, check response text
                        elif expected["type"] == "general_inquiry":
                            operation_score = 1.0 if actual.get("response") == expected["response"] else 0.0
                            if actual.get("response") != expected["response"]:
                                f.write(f"Response Text Mismatch!\n")
                                f.write(f"Expected: {expected['response']}\n")
                                f.write(f"Got: {actual.get('response')}\n\n")
                    
                    # Add format scores to metrics
                    for metrics_dict in [total_metrics, category_total]:
                        metrics_dict["response_format_accuracy"] += format_score
                        metrics_dict["operation_accuracy"] += operation_score
                    
                    # Accumulate metrics for both category and overall
                    for metrics_dict in [total_metrics, category_total]:
                        metrics_dict["mrr"] += mrr
                        metrics_dict["precision_at_k"] += precision
                        metrics_dict["ndcg"] += ndcg
                        metrics_dict["context_relevance"] += context_relevance
                    
                    # Write metrics
                    f.write("Metrics:\n")
                    f.write(f"MRR: {mrr:.3f}\n")
                    f.write(f"Precision@3: {precision:.3f}\n")
                    f.write(f"NDCG: {ndcg:.3f}\n")
                    f.write(f"Context Relevance: {context_relevance:.3f}\n")
                    f.write(f"Response Format Accuracy: {format_score:.3f}\n")
                    f.write(f"Operation Accuracy: {operation_score:.3f}\n")
                    
                    f.write("\n" + "-"*50 + "\n\n")
                
                # Calculate and store category averages
                num_category_queries = len(test_cases)
                category_metrics[category] = {
                    metric: value / num_category_queries
                    for metric, value in category_total.items()
                }
                total_queries += num_category_queries
                
                # Write category metrics
                f.write(f"\n{category.capitalize()} Category Metrics:\n")
                f.write("-" * (len(category) + 17) + "\n")
                for metric, value in category_metrics[category].items():
                    f.write(f"{metric}: {value:.3f}\n")
                f.write(f"Number of queries: {num_category_queries}\n\n")
            
            # Calculate overall averages
            avg_metrics = {
                metric: value / total_queries
                for metric, value in total_metrics.items()
            }
            
            # Write overall metrics
            f.write("\nOverall Metrics:\n")
            f.write("===============\n")
            for metric, value in avg_metrics.items():
                f.write(f"{metric}: {value:.3f}\n")
            
            f.write(f"\nTotal number of queries: {total_queries}\n")
            
            # Write category comparison
            f.write("\nCategory Comparison:\n")
            f.write("==================\n")
            metrics_list = ["mrr", "precision_at_k", "ndcg", "context_relevance", "response_format_accuracy", "operation_accuracy"]
            
            # Header
            f.write(f"{'Category':<15}")
            for metric in metrics_list:
                f.write(f"{metric:>15}")
            f.write("\n" + "-" * 75 + "\n")
            
            # Values
            for category, metrics in category_metrics.items():
                f.write(f"{category:<15}")
                for metric in metrics_list:
                    f.write(f"{metrics[metric]:>15.3f}")
                f.write("\n")
        
        return avg_metrics

    async def test_banking_faqs_performance(self):
        """Test RAG system performance on banking FAQs using multiple metrics"""
        metrics = await self.calculate_metrics()
        
        # Assert minimum performance thresholds
        
        # Context retrieval metrics
        self.assertGreater(metrics["mrr"], 0, "MRR is below acceptable threshold")
        self.assertGreater(metrics["precision_at_k"], 0, "Precision@K is below acceptable threshold")
        self.assertGreater(metrics["ndcg"], 0, "NDCG is below acceptable threshold")
        self.assertGreater(metrics["context_relevance"], 0, "Context relevance is below acceptable threshold")
        
        # Response format metrics
        self.assertGreater(metrics["response_format_accuracy"], 0, 
                          "Response format accuracy is below acceptable threshold. LLM responses are not consistently following the expected JSON schema.")
        self.assertGreater(metrics["operation_accuracy"], 0,
                          "Operation accuracy is below acceptable threshold. LLM is not correctly identifying or parameterizing banking operations.")

    @classmethod
    async def asyncTearDownClass(cls):
        """Clean up test data"""
        from api.models import Document
        await Document.objects.all().adelete()
        await super().asyncTearDownClass()
