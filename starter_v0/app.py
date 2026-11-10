from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import now_iso, run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)


def _new_transcript(provider_name: str, model: str | None) -> tuple[dict, Path]:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    version = "v3"
    artifact_version = build_artifact_version(
        version,
        ARTIFACTS_DIR / "system_prompt.md",
        ARTIFACTS_DIR / "tools.yaml",
    )
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", None)
    transcript_id = f"{version}_{provider_name}_{timestamp}"
    transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": "artifacts/system_prompt.md",
        "tools": "artifacts/tools.yaml",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    return transcript, TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"


st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")
st.title("🔎 Research Agent")
st.caption("Research the web and social posts, read URLs, and organize source material.")

with st.sidebar:
    st.header("Session")
    provider_name = st.selectbox("Model provider", ["gemini", "openrouter", "openai", "anthropic"])
    model_override = st.text_input("Model override (optional)", placeholder="Use provider default")
    if st.button("Clear conversation"):
        st.session_state.pop("research_transcript", None)
        st.session_state.pop("research_transcript_path", None)
        st.session_state.pop("research_history", None)
        st.rerun()

if "research_transcript" not in st.session_state:
    transcript, transcript_path = _new_transcript(provider_name, model_override.strip() or None)
    st.session_state.research_transcript = transcript
    st.session_state.research_transcript_path = str(transcript_path)
    st.session_state.research_history = []

for turn in st.session_state.research_transcript["turns"]:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn.get("assistant_text") or "(No response text)")
        if turn.get("tool_events"):
            with st.expander("Tool activity"):
                st.json(turn["tool_events"])
        if turn.get("error"):
            st.error(turn["error"])

user_text = st.chat_input("Ask for research, a social search, or a URL summary")
if user_text:
    with st.chat_message("user"):
        st.markdown(user_text)

    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    provider = make_provider(provider_name)
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.research_history, 5),
        {"role": "user", "content": user_text},
    ]

    turn_record = {
        "turn_index": len(st.session_state.research_transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=to_openai_tools(declarations),
                    model=model_override.strip() or None,
                    max_tool_rounds=4,
                )
                turn_record.update(result)
                assistant_text = result["assistant_text"] or "I could not produce a text response."
                st.markdown(assistant_text)
                if result.get("tool_events"):
                    with st.expander("Tool activity"):
                        st.json(result["tool_events"])
                st.session_state.research_history.extend([
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": assistant_text},
                ])
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                turn_record.update({"status": "provider_error", "error": error})
                assistant_text = "The request could not be completed. Check the provider key, quota, and connection, then try again."
                st.error(assistant_text)

    turn_record["ended_at"] = now_iso()
    st.session_state.research_transcript["turns"].append(turn_record)
    write_transcript(Path(st.session_state.research_transcript_path), st.session_state.research_transcript)

st.caption(f"Transcript: {Path(st.session_state.research_transcript_path).name}")
