"""Синхронизация промптов с Langfuse."""

from typing import List, Dict
from .prompts import create_chat_prompt, get_prompt, update_prompt, create_prompt, load_prompt_file


class PromptSync:
    """Класс для синхронизации промптов с Langfuse."""

    def sync_chat_prompt(
        self,
        name: str,
        system_file: str,
        user_file: str,
        labels: List[str],
    ) -> Dict:
        """Синхронизировать chat промпт."""
        system_content = load_prompt_file(system_file)
        user_content = load_prompt_file(user_file)

        chat_prompt = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]

        try:
            existing = get_prompt(name, label=labels[0])
            result = update_prompt(
                name=name,
                version=existing.version,
                prompt=chat_prompt,
                labels=labels,
            )
            return {
                "action": "updated",
                "name": name,
                "version": result.version,
                "previous_version": existing.version,
                "labels": result.labels,
            }
        except Exception:
            result = create_chat_prompt(
                name=name,
                prompt=chat_prompt,
                labels=labels,
            )
            return {
                "action": "created",
                "name": name,
                "version": result.version,
                "labels": result.labels,
            }

    def sync_text_prompt(
        self,
        name: str,
        prompt_file: str,
        labels: List[str],
    ) -> Dict:
        """Синхронизировать text промпт."""
        prompt_content = load_prompt_file(prompt_file)

        try:
            existing = get_prompt(name, label=labels[0])
            result = update_prompt(
                name=name,
                version=existing.version,
                prompt=prompt_content,
                labels=labels,
            )
            return {
                "action": "updated",
                "name": name,
                "version": result.version,
                "previous_version": existing.version,
                "labels": result.labels,
            }
        except Exception:
            result = create_prompt(
                name=name,
                prompt=prompt_content,
                labels=labels,
            )
            return {
                "action": "created",
                "name": name,
                "version": result.version,
                "labels": result.labels,
            }
