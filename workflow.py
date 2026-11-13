"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    trials = []
    for case in data['cases']:
        for version in data['versions']:
            prompt = 'Answer briefly.' if version == 'brief' else 'Answer precisely and name the returned data type.'
            answer = await agent.ask(version + '_' + case['id'], prompt, case['question'], 'Glob returns file paths.')
            trials.append({'case': case['id'], 'version': version, 'passed': case['required'] in answer.lower()})
    scores = {v: sum(t['passed'] for t in trials if t['version'] == v) for v in data['versions']}
    return {'trials': trials, 'scores': scores, 'decision': 'Keep the baseline when both versions tie; gather more evidence.'}
