"""
Enhanced Adaptive Memory Agent with Episodic and Semantic Memory
"""

from enhanced_memory import EpisodicMemory, SemanticMemory


class AdaptiveMemoryAgent:
    def __init__(self):
        self.episodic_memory = EpisodicMemory(capacity=1000)
        self.semantic_memory = SemanticMemory()
        
    def load(self):
        """Load recent memories"""
        return self.episodic_memory.get_recent(10)
    
    def update(self, context, out):
        """Update memory with new experience"""
        # Store in episodic memory
        self.episodic_memory.store(context, "memory_update", out)
        
        # Learn patterns in semantic memory
        success = out.get('success', False) if isinstance(out, dict) else True
        task_type = context.get('task_type', 'unknown')
        self.semantic_memory.record_pattern(task_type, 'memory_operation', success)
    
    def run(self, context):
        """Run with enhanced memory capabilities"""
        # Retrieve similar past experiences
        similar_experiences = self.episodic_memory.retrieve_similar(
            context.get('task', ''), k=3
        )
        
        # Get best actions for current context
        best_action = self.semantic_memory.get_best_action(
            context.get('task_type', 'general')
        )
        
        return {
            "memory_size": len(self.episodic_memory.episodes),
            "similar_experiences": len(similar_experiences),
            "success_patterns": len(self.semantic_memory.patterns),
            "recommended_action": best_action,
            "memory_type": "enhanced"
        }
    
    def get_similar_experiences(self, query, k=3):
        """Get similar past experiences"""
        return self.episodic_memory.retrieve_similar(query, k)
    
    def get_success_patterns(self, context):
        """Get success patterns for specific context"""
        return self.semantic_memory.patterns.get(context, [])
