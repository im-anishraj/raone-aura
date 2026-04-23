from __future__ import annotations

import os
from typing import Any, AsyncGenerator

from openai import AsyncOpenAI
# Import types needed for Vibe compatibility
from vibe.core.types import (
    LLMChunk,
    LLMMessage,
    LLMUsage,
    Role,
    ToolCall,
    FunctionCall,
)
from vibe.core.llm.backend.mistral import MistralBackend

class OpenAIBackend(MistralBackend):
    def __init__(self, provider: Any, timeout: float = 720.0) -> None: 
        
        # 1. Get Key
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        # 2. Initialize Client with Groq Base URL
        self.client = AsyncOpenAI(
            api_key=api_key, 
            base_url="https://api.groq.com/openai/v1",
            timeout=timeout
        )

    # --- HELPER: Safely extract data ---
    def _extract_data(self, args, kwargs):
        source = kwargs
        if len(args) > 0:
            source = args[0]
        elif "request" in kwargs:
            source = kwargs["request"]
        
        def get(name, default=None):
            if name in kwargs and kwargs[name] is not None:
                return kwargs[name]
            if isinstance(source, dict):
                return source.get(name, default)
            return getattr(source, name, default)

        return source, get

    # --- HELPER: Convert Tool Calls ---
    def _convert_tool_calls(self, tool_calls) -> list[ToolCall] | None:
        if not tool_calls:
            return None
        return [
            ToolCall(
                id=tc.id,
                function=FunctionCall(
                    name=tc.function.name,
                    arguments=tc.function.arguments
                ),
                index=tc.index if hasattr(tc, 'index') else 0
            )
            for tc in tool_calls
        ]

    # --- HELPER: Clean Schema ---
    def _clean_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Recursively remove 'title' keys from JSON schema."""
        if not isinstance(schema, dict):
            return schema
        
        # Create a copy to avoid modifying original
        clean = schema.copy()
        clean.pop("title", None)
        
        for key, value in clean.items():
            if isinstance(value, dict):
                clean[key] = self._clean_schema(value)
            elif isinstance(value, list):
                clean[key] = [
                    self._clean_schema(item) if isinstance(item, dict) else item
                    for item in value
                ]
        return clean


    def _resolve_refs(self, schema: dict[str, Any], defs: dict[str, Any] | None = None) -> dict[str, Any]:
        """Resolves $ref in schema by inlining $defs."""
        if not isinstance(schema, dict):
            return schema

        # If schema is root, extract $defs
        if defs is None:
             defs = schema.get("$defs", {})
        
        # Handle $ref
        if "$ref" in schema:
            ref = schema["$ref"]
            if ref.startswith("#/$defs/"):
                ref_name = ref.split("/")[-1]
                if defs and ref_name in defs:
                    # Resolve recursively
                    resolved = self._resolve_refs(defs[ref_name], defs)
                    return resolved
            return schema

        # Recurse
        resolved_schema = {}
        for k, v in schema.items():
            if k == "$defs":
                continue # Skip copying defs to output (we inline them)
            
            if isinstance(v, dict):
                resolved_schema[k] = self._resolve_refs(v, defs)
            elif isinstance(v, list):
                resolved_schema[k] = [
                    self._resolve_refs(i, defs) if isinstance(i, dict) else i
                    for i in v
                ]
            else:
                resolved_schema[k] = v
        
        return resolved_schema

    # --- MAIN FUNCTION ---
    async def complete(self, *args, **kwargs) -> LLMChunk:
        try:
            source, get = self._extract_data(args, kwargs)
            
            # 1. Use a high-performance model from Groq
            model = "llama-3.3-70b-versatile"
            
            # 2. Clean up messages
            raw_msgs = get("messages", [])
            messages = []
            for msg in raw_msgs:
                # Handle Role extraction
                role_val = getattr(msg, "role", None)
                if role_val is None and isinstance(msg, dict):
                    role_val = msg.get("role")
                
                # Convert Enum to string if needed
                role = str(role_val) if role_val else "user"
                
                # Handle Content extraction
                content_val = getattr(msg, "content", None)
                if content_val is None and isinstance(msg, dict):
                    content_val = msg.get("content")
                
                content = str(content_val) if content_val is not None else ""

                content = str(content_val) if content_val is not None else ""

                if role == "tool": 
                    role = "tool" # Keep as tool for modern APIs
                if role == "function":
                    role = "tool"
                
                m = {"role": role, "content": content}
                
                # Handle tool_call_id for role='tool'
                if role == "tool":
                    tid = getattr(msg, "tool_call_id", None) or (msg.get("tool_call_id") if isinstance(msg, dict) else None)
                    if not tid:
                        # Dummy ID if missing, though it should be there
                        tid = getattr(msg, "message_id", None) or "dummy_id"
                    m["tool_call_id"] = str(tid)
                
                # Handle tool_calls for role='assistant'
                if role == "assistant":
                    tcs = getattr(msg, "tool_calls", None) or (msg.get("tool_calls") if isinstance(msg, dict) else None)
                    if tcs:
                        m["tool_calls"] = []
                        for tc in tcs:
                            # Handle both object and dict
                            if isinstance(tc, dict):
                                f = tc.get("function", {})
                                m["tool_calls"].append({
                                    "id": str(tc.get("id", "dummy_id")),
                                    "type": "function",
                                    "function": {
                                        "name": f.get("name"),
                                        "arguments": f.get("arguments")
                                    }
                                })
                            else:
                                m["tool_calls"].append({
                                    "id": str(getattr(tc, "id", "dummy_id")),
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments
                                    }
                                })

                messages.append(m)

            # 3. Build Arguments
            req_args = {
                "model": model,
                "messages": messages,
                "temperature": get("temperature", 0.7),
            }
            
            mt = get("max_tokens", None)
            if mt is not None:
                req_args["max_tokens"] = mt

            # Handle Tools
            tools = get("tools")
            if tools:
                openai_tools = []
                for tool in tools:
                    fname = getattr(tool.function, "name", None) or tool.function.get("name")
                    fdesc = getattr(tool.function, "description", None) or tool.function.get("description")
                    fparams = getattr(tool.function, "parameters", None) or tool.function.get("parameters")

                    # Resolve Refs and Clean Schema
                    if fparams:
                        # Ensure we are working with a dict
                        params_dict = fparams if isinstance(fparams, dict) else (getattr(fparams, "model_dump", lambda: {})() if hasattr(fparams, "model_dump") else getattr(fparams, "__dict__", {}))
                        resolved = self._resolve_refs(params_dict)
                        cleaned = self._clean_schema(resolved)
                    else:
                        cleaned = {}

                    t = {
                        "type": "function",
                        "function": {
                            "name": fname,
                            "description": fdesc,
                            "parameters": cleaned
                        }
                    }
                    openai_tools.append(t)
                req_args["tools"] = openai_tools
                
                tool_choice = get("tool_choice")
                if tool_choice:
                    if isinstance(tool_choice, str):
                        req_args["tool_choice"] = tool_choice
                    elif hasattr(tool_choice, 'function'):
                         req_args["tool_choice"] = {
                            "type": "function",
                            "function": {"name": tool_choice.function.name}
                        }



            # 4. Call API
            response = await self.client.chat.completions.create(**req_args)
            
            # 5. Convert to LLMChunk
            choice = response.choices[0]
            msg = choice.message
            
            return LLMChunk(
                message=LLMMessage(
                    role=Role.assistant,
                    content=msg.content,
                    tool_calls=self._convert_tool_calls(msg.tool_calls)
                ),
                usage=LLMUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                ) if response.usage else None
            )

        except Exception as e:
            raise e

    # --- STREAMING FUNCTION ---
    async def complete_streaming(self, *args, **kwargs) -> AsyncGenerator[LLMChunk, None]:
        try:
            source, get = self._extract_data(args, kwargs)
            
            model = "llama-3.3-70b-versatile"
            
            raw_msgs = get("messages", [])
            messages = []
            for msg in raw_msgs:
                role_val = getattr(msg, "role", None)
                if role_val is None and isinstance(msg, dict):
                    role_val = msg.get("role")
                role = str(role_val) if role_val else "user"
                
                content_val = getattr(msg, "content", None)
                if content_val is None and isinstance(msg, dict):
                    content_val = msg.get("content")
                content = str(content_val) if content_val is not None else ""

                content = str(content_val) if content_val is not None else ""

                if role == "tool": 
                    role = "tool"
                if role == "function":
                    role = "tool"
                
                m = {"role": role, "content": content}

                # Handle tool_call_id for role='tool'
                if role == "tool":
                    tid = getattr(msg, "tool_call_id", None) or (msg.get("tool_call_id") if isinstance(msg, dict) else None)
                    if not tid:
                        tid = getattr(msg, "message_id", None) or "dummy_id"
                    m["tool_call_id"] = str(tid)

                # Handle tool_calls for role='assistant'
                if role == "assistant":
                    tcs = getattr(msg, "tool_calls", None) or (msg.get("tool_calls") if isinstance(msg, dict) else None)
                    if tcs:
                        m["tool_calls"] = []
                        for tc in tcs:
                            if isinstance(tc, dict):
                                f = tc.get("function", {})
                                m["tool_calls"].append({
                                    "id": str(tc.get("id", "dummy_id")),
                                    "type": "function",
                                    "function": {
                                        "name": f.get("name"),
                                        "arguments": f.get("arguments")
                                    }
                                })
                            else:
                                m["tool_calls"].append({
                                    "id": str(getattr(tc, "id", "dummy_id")),
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments
                                    }
                                })

                messages.append(m)

            req_args = {
                "model": model,
                "messages": messages,
                "temperature": get("temperature", 0.7),
                "stream": True
            }
            
            mt = get("max_tokens", None)
            if mt is not None:
                req_args["max_tokens"] = mt

            # Handle Tools
            tools = get("tools")
            if tools:
                openai_tools = []
                for tool in tools:
                    fname = getattr(tool.function, "name", None) or tool.function.get("name")
                    fdesc = getattr(tool.function, "description", None) or tool.function.get("description")
                    fparams = getattr(tool.function, "parameters", None) or tool.function.get("parameters")

                    # Resolve Refs and Clean Schema
                    if fparams:
                        # Ensure we are working with a dict
                        params_dict = fparams if isinstance(fparams, dict) else (getattr(fparams, "model_dump", lambda: {})() if hasattr(fparams, "model_dump") else getattr(fparams, "__dict__", {}))
                        resolved = self._resolve_refs(params_dict)
                        cleaned = self._clean_schema(resolved)
                    else:
                        cleaned = {}

                    t = {
                        "type": "function",
                        "function": {
                            "name": fname,
                            "description": fdesc,
                            "parameters": cleaned
                        }
                    }
                    openai_tools.append(t)
                req_args["tools"] = openai_tools

                tool_choice = get("tool_choice")
                if tool_choice:
                    if isinstance(tool_choice, str):
                        req_args["tool_choice"] = tool_choice
                    elif hasattr(tool_choice, 'function'):
                         req_args["tool_choice"] = {
                            "type": "function",
                            "function": {"name": tool_choice.function.name}
                        }

            stream = await self.client.chat.completions.create(**req_args)

            async for chunk in stream:
                if not chunk.choices:
                    continue
                    
                delta = chunk.choices[0].delta
                
                # Convert usage if present
                usage = None
                if getattr(chunk, "usage", None):
                    usage = LLMUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                    )

                yield LLMChunk(
                    message=LLMMessage(
                        role=Role.assistant,
                        content=delta.content,
                        tool_calls=self._convert_tool_calls(delta.tool_calls)
                    ),
                    usage=usage
                )
                
        except Exception as e:
            print(f"[ERROR] Groq Streaming Failed: {e}")
            raise e