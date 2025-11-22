"""
Enhanced Memory Systems for Powerhouse
Episodic and Semantic memory patterns for improved learning
"""

import numpy as np
from collections import defaultdict
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class EpisodicMemory:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.episodes = []
      
    def store(self, state, action, outcome, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        episode = {
            'state': state,
            'action': action,
            'outcome': outcome,
            'timestamp': timestamp,
            'embedding': self._embed(state, action, outcome)
        }
        self.episodes.append(episode)
        if len(self.episodes) > self.capacity:
            self.episodes.pop(0)
  
    def _embed(self, state, action, outcome):
        text = f"{state} {action} {outcome}".lower()
        return hash(text) % 10000
  
    def retrieve_similar(self, query_state, k=3):
        if not self.episodes:
            return []
        query_emb = self._embed(query_state, "", "")
        scores = [(abs(ep['embedding'] - query_emb), ep) for ep in self.episodes]
        scores.sort(key=lambda x: x[0])
        return [ep for _, ep in scores[:k]]
  
    def get_recent(self, n=5):
        return self.episodes[-n:]


class SemanticMemory:
    def __init__(self):
        self.preferences = defaultdict(float)
        self.patterns = defaultdict(list)
        self.success_rates = defaultdict(lambda: {'success': 0, 'total': 0})
      
    def update_preference(self, key, value, weight=1.0):
        self.preferences[key] = 0.9 * self.preferences[key] + 0.1 * weight * value
  
    def record_pattern(self, context, action, success):
        pattern_key = f"{context}_{action}"
        self.patterns[context].append((action, success))
        self.success_rates[pattern_key]['total'] += 1
        if success:
            self.success_rates[pattern_key]['success'] += 1
  
    def get_best_action(self, context):
        if context not in self.patterns:
            return None
        action_scores = defaultdict(lambda: {'success': 0, 'total': 0})
        for action, success in self.patterns[context]:
            action_scores[action]['total'] += 1
            if success:
                action_scores[action]['success'] += 1
        best_action = max(action_scores.items(), key=lambda x: x[1]['success'] / max(x[1]['total'], 1))
        return best_action[0] if best_action[1]['total'] > 0 else None
  
    def get_preference(self, key):
        return self.preferences.get(key, 0.0)
