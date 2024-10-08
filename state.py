from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class UserInfo(BaseModel):
    user_id: str = Field(..., description="customer_id in instwise customer support")
    organization_id: str = Field(
        ..., description="organization_id for instwise customer support"
    )
    zendesk_id: str = Field(..., description="zendesk id for the customer")
    hubspot_id: str = Field(..., description="hubspot id for the customer")
    churnzero_id: str = Field(..., description="churnzero id for the customer")
    salesforce_id: str = Field(..., description="salesforce id for the customer")


class AgentStateGraph(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: UserInfo
    crm_agent_response: str
    csm_agent_response: str
    helpdesk_agent_response: str
    chatdata_agent_response: str
