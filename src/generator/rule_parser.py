from typing import List

from langchain_openai import ChatOpenAI

from src.schemas import ComplianceSeed


class RuleParser:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2)

    def parse_raw_text(self, text: str) -> List[ComplianceSeed]:
        prompt = f"""
        你是一名合规专家。请阅读以下文本，提取出具体的、可测试的技术合规规则。
        对于每条规则，定义其领域和风险等级。
        文本内容: {text}

        请输出 JSON 格式列表。
        """
        return self.llm.with_structured_output(List[ComplianceSeed]).invoke(prompt)
