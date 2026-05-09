from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate

load_dotenv()

PERSIST_DIR = "./chroma_db"


class RetrievalAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=self.embeddings,
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

    def retrieve(self, query, k=5):
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs

    def build_context(self, docs):
        context = []

        for i, doc in enumerate(docs):
            context.append(
                f"""
Document {i+1}
Source: {doc.metadata.get('source')}
Content:
{doc.page_content}
"""
            )

        return "\n\n".join(context)

    def answer(self, query):
        docs = self.retrieve(query)

        context = self.build_context(docs)

        prompt = ChatPromptTemplate.from_template(
            """
你是企业级代码架构助手。

请基于以下内部规范、历史 PR 与架构文档回答问题。

上下文：
{context}

用户问题：
{query}

要求：
1. 必须优先遵守内部规范
2. 给出明确技术建议
3. 如果发现架构风险，需要指出
4. 尽量参考历史 PR 的最佳实践
"""
        )

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "query": query,
            }
        )

        return {
            "query": query,
            "retrieved_docs": [
                {
                    "source": d.metadata.get("source"),
                    "content": d.page_content
                }
                for d in docs
            ],
            "answer": response.content,
        }
