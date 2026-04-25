"""
knowledge_base.py
Builds the FAISS vector store from all product FAQ data.
Uses free HuggingFace embeddings — no API key needed.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from products import PRODUCTS, PRODUCT_FAQ


def build_documents() -> list:
    """Convert all FAQ data into LangChain Document objects."""
    docs = []

    # System context document
    product_names = ", ".join(p["name"] for p in PRODUCTS.values())
    docs.append(Document(
        page_content=(
            f"You are an expert Apple product support agent. "
            f"You support the following products: {product_names}. "
            "Always be helpful, friendly, and give step-by-step instructions. "
            "If you cannot answer from the knowledge base, say so and direct the "
            "customer to Apple Support at 1-800-APL-CARE or apple.com/support."
        ),
        metadata={"source": "system", "product": "all"},
    ))

    # Per-product FAQ documents
    for product_id, categories in PRODUCT_FAQ.items():
        product_name = PRODUCTS[product_id]["name"]
        for cat_data in categories:
            for item in cat_data["questions"]:
                content = (
                    f"Product: {product_name}\n"
                    f"Category: {cat_data['category']}\n"
                    f"Question: {item['q']}\n"
                    f"Answer: {item['a']}"
                )
                docs.append(Document(
                    page_content=content,
                    metadata={
                        "source":       "faq",
                        "product":      product_id,
                        "product_name": product_name,
                        "category":     cat_data["category"],
                        "question":     item["q"],
                    },
                ))

    return docs


def build_vector_store() -> FAISS:
    """Build and return the FAISS vector store from all FAQ documents."""
    documents = build_documents()

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks   = splitter.split_documents(documents)

    print(f"   📚 {len(chunks)} knowledge chunks from {len(documents)} documents")
    print("   🔄 Loading HuggingFace embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    store = FAISS.from_documents(chunks, embeddings)
    print(f"   ✅ FAISS index ready — {len(PRODUCTS)} products indexed")
    return store
