"""
Corpus management for plagiarism detection.
Manages reference documents and sample databases.
"""
from typing import List, Dict


class CorpusManager:
    """
    Manages corpus of reference documents for plagiarism comparison.
    In production, this would interface with Elasticsearch or a vector database.
    """
    
    def __init__(self):
        """Initialize corpus with sample academic texts."""
        self.corpus = self._get_sample_corpus()
    
    def _get_sample_corpus(self) -> List[Dict[str, str]]:
        """
        Get sample corpus for demonstration.
        In production, this would query a real database.
        """
        return [
            {
                'id': 'sample_1',
                'title': 'Machine Learning Fundamentals',
                'text': """
                Machine learning is a subset of artificial intelligence that focuses on developing
                algorithms and statistical models that enable computers to learn from and make
                predictions or decisions based on data. The fundamental principle is to allow
                machines to learn from experience without being explicitly programmed for every
                specific task. Supervised learning involves training models on labeled data,
                where the algorithm learns to map inputs to known outputs. Unsupervised learning,
                on the other hand, deals with unlabeled data and seeks to find hidden patterns
                or structures within the dataset. Deep learning, a specialized branch of machine
                learning, utilizes artificial neural networks with multiple layers to extract
                high-level features from raw data. Common applications include image recognition,
                natural language processing, recommendation systems, and autonomous vehicles.
                """,
                'url': 'https://academic.example.com/ml-fundamentals'
            },
            {
                'id': 'sample_2',
                'title': 'Climate Change and Global Warming',
                'text': """
                Climate change refers to long-term shifts in global or regional climate patterns,
                primarily attributed to increased levels of atmospheric carbon dioxide produced
                by the use of fossil fuels. Global warming is a key aspect of climate change,
                characterized by the rising average temperature of Earth's climate system. The
                primary causes include greenhouse gas emissions from human activities such as
                burning coal, oil, and natural gas for energy, deforestation, and industrial
                processes. The effects of climate change are wide-ranging and include rising sea
                levels, more frequent extreme weather events, shifting wildlife populations and
                habitats, and changes in precipitation patterns. Mitigation strategies focus on
                reducing greenhouse gas emissions through renewable energy adoption, energy
                efficiency improvements, and carbon capture technologies. Adaptation measures
                involve preparing for and adjusting to the impacts of climate change that are
                already occurring or anticipated in the future.
                """,
                'url': 'https://academic.example.com/climate-change'
            },
            {
                'id': 'sample_3',
                'title': 'Quantum Computing Principles',
                'text': """
                Quantum computing represents a revolutionary approach to information processing
                that leverages the principles of quantum mechanics. Unlike classical computers
                that use bits representing either 0 or 1, quantum computers use quantum bits or
                qubits that can exist in multiple states simultaneously through superposition.
                This property, along with quantum entanglement, enables quantum computers to
                perform certain calculations exponentially faster than classical computers. The
                fundamental operations in quantum computing involve quantum gates that manipulate
                qubit states through unitary transformations. Quantum algorithms such as Shor's
                algorithm for factoring large numbers and Grover's algorithm for searching
                unsorted databases demonstrate the potential advantages of quantum computing.
                Current challenges include maintaining quantum coherence, error correction, and
                scaling up the number of qubits while minimizing decoherence and noise.
                """,
                'url': 'https://academic.example.com/quantum-computing'
            },
            {
                'id': 'sample_4',
                'title': 'Blockchain Technology and Cryptocurrencies',
                'text': """
                Blockchain is a distributed ledger technology that maintains a continuously
                growing list of records called blocks, which are linked and secured using
                cryptography. Each block contains a cryptographic hash of the previous block,
                a timestamp, and transaction data. This structure makes the blockchain inherently
                resistant to modification of data, as altering any single block would require
                changing all subsequent blocks. The decentralized nature of blockchain eliminates
                the need for a central authority, instead relying on a network of nodes to
                validate and record transactions through consensus mechanisms such as Proof of
                Work or Proof of Stake. Cryptocurrencies like Bitcoin and Ethereum are the most
                well-known applications of blockchain technology, but the technology has broader
                applications in supply chain management, digital identity verification, smart
                contracts, and decentralized finance. The immutability and transparency of
                blockchain make it particularly valuable for applications requiring trust and
                auditability without intermediaries.
                """,
                'url': 'https://academic.example.com/blockchain'
            },
            {
                'id': 'sample_5',
                'title': 'Artificial Neural Networks',
                'text': """
                Artificial neural networks are computing systems inspired by the biological
                neural networks that constitute animal brains. These networks consist of
                interconnected nodes or neurons organized in layers, typically including an
                input layer, one or more hidden layers, and an output layer. Each connection
                between neurons has an associated weight that adjusts as learning proceeds,
                strengthening or weakening the signal transmitted between neurons. The learning
                process involves adjusting these weights through algorithms like backpropagation,
                which minimizes the difference between the network's output and the desired
                output. Activation functions introduce non-linearity into the network, enabling
                it to learn complex patterns and relationships in data. Deep neural networks,
                which contain multiple hidden layers, have demonstrated remarkable success in
                various domains including computer vision, speech recognition, and natural
                language understanding. Modern architectures such as convolutional neural
                networks excel at processing grid-like data such as images, while recurrent
                neural networks are well-suited for sequential data like text and time series.
                """,
                'url': 'https://academic.example.com/neural-networks'
            }
        ]
    
    def get_all_texts(self) -> List[str]:
        """Get all corpus texts for comparison."""
        return [doc['text'] for doc in self.corpus]
    
    def get_metadata(self) -> List[Dict[str, str]]:
        """Get metadata for all corpus documents."""
        return [
            {
                'title': doc['title'],
                'url': doc['url']
            }
            for doc in self.corpus
        ]
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search corpus for relevant documents.
        In production, this would use Elasticsearch or similar.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of relevant documents
        """
        # For demo, return all documents
        # In production, implement proper search/ranking
        return self.corpus[:limit]
