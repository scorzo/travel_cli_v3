# generic_agent.py

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.agents import AgentActionMessageLog, AgentFinish
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import json

class GenericAgent:
    def __init__(self, model_name="gpt-4o", pydantic_model=None, tools=None):
        self.model_name = model_name
        self.pydantic_model = pydantic_model
        self.tools = tools or []
        self._validate_tools()

    def _validate_tools(self):
        for tool in self.tools:
            if not hasattr(tool, 'name') or not hasattr(tool, 'description') or not hasattr(tool, 'args'):
                raise ValueError(f"Invalid tool: {tool}. Each tool must have 'name', 'description', and 'args' attributes.")


    def create_agent(self):
        agent_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(model=self.model_name, temperature=0)
        # Create a temporary list containing tools and the pydantic model
        tools_and_model = self.tools + [self.pydantic_model]
        llm_with_tools = llm.bind_functions(tools_and_model)


        agent = (
                {
                    "input": lambda x: x["input"],
                    # Format agent scratchpad from intermediate steps
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(
                        x["intermediate_steps"]
                    ),
                }
                | agent_prompt
                | llm_with_tools
                | self.parse
        )

        return agent

    def generate_response(self, prompt):

        # Create and use the agent
        agent = self.create_agent()
        agent_executor = AgentExecutor(tools=self.tools, agent=agent, verbose=True)

        response = agent_executor.invoke(
            {"input": prompt},
            return_only_outputs=True,
        )

        return response



    def parse(self, output):
        # If no function was invoked, return to user
        if "function_call" not in output.additional_kwargs:
            #return AgentFinish(return_values={"output": output.content}, log=output.content)
            # convert json formatted output string to python dictionary
            return AgentFinish(return_values=json.loads(output.content), log=output.content)



        # Parse out the function call
        function_call = output.additional_kwargs["function_call"]
        name = function_call["name"]
        inputs = json.loads(function_call["arguments"])

        # If the function corresponding to pydantic_model was invoked, return to the user with the function inputs
        if name == self.pydantic_model.__name__:
            return AgentFinish(return_values=inputs, log=str(function_call))
        # Otherwise, return an agent action
        else:
            return AgentActionMessageLog(
                tool=name, tool_input=inputs, log="", message_log=[output]
            )
