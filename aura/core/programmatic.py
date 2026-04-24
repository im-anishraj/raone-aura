from __future__ import annotations

import asyncio

from aura.core.agent_loop import AgentLoop
from aura.core.agents.models import BuiltinAgentName
from aura.core.config import AuraConfig
from aura.core.output_formatters import create_formatter
from aura.core.tools.builtins.ask_user_question import AskUserQuestionResult
from aura.core.types import AssistantEvent, LLMMessage, OutputFormat, Role
from aura.core.utils import ConversationLimitException, logger


def run_programmatic(
    config: AuraConfig,
    prompt: str,
    max_turns: int | None = None,
    max_price: float | None = None,
    output_format: OutputFormat = OutputFormat.TEXT,
    previous_messages: list[LLMMessage] | None = None,
    agent_name: str = BuiltinAgentName.AUTO_APPROVE,
) -> str | None:
    formatter = create_formatter(output_format)

    agent_loop = AgentLoop(
        config,
        agent_name=agent_name,
        message_observer=formatter.on_message_added,
        max_turns=max_turns,
        max_price=max_price,
        enable_streaming=False,
    )
    logger.info("USER: %s", prompt)

    async def _async_run() -> str | None:
        async def _interactive_callback(_: Any) -> AskUserQuestionResult:
            return AskUserQuestionResult(answers=[], cancelled=True)

        if previous_messages:
            non_system_messages = [
                msg for msg in previous_messages if not (msg.role == Role.system)
            ]
            agent_loop.messages.extend(non_system_messages)
            logger.info(
                "Loaded %d messages from previous session", len(non_system_messages)
            )

        agent_loop.user_input_callback = _interactive_callback

        async for event in agent_loop.act(prompt):
            formatter.on_event(event)
            if isinstance(event, AssistantEvent) and event.stopped_by_middleware:
                raise ConversationLimitException(event.content)

        return formatter.finalize()

    return asyncio.run(_async_run())
