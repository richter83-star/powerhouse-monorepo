"""
Enhanced Orchestrator with Autonomous Goal-Driven Agent and Memory Systems
"""

from typing import Dict, Any, Optional
from datetime import datetime

from utils.logging import get_logger
from core.orchestrator_with_forecasting import OrchestratorWithForecasting
from core.goal_driven_agent import GoalDrivenAgent
from enhanced_memory import SemanticMemory

logger = get_logger(__name__)


class OrchestratorWithAutonomousAgent(OrchestratorWithForecasting):
    """
    Enhanced orchestrator with fully autonomous goal-driven behavior and memory systems.
    """
    
    def __init__(
        self,
        performance_monitor_config: Optional[Dict[str, Any]] = None,
        config_manager_config: Optional[Dict[str, Any]] = None,
        forecasting_config: Optional[Dict[str, Any]] = None,
        executor_config: Optional[Dict[str, Any]] = None,
        agent_config: Optional[Dict[str, Any]] = None
    ):
        # Initialize parent (includes forecasting)
        super().__init__(
            performance_monitor_config,
            config_manager_config,
            forecasting_config
        )
        
        # ENHANCED: Initialize semantic memory for task-agent matching
        self.semantic_memory = SemanticMemory()
        
        # Initialize autonomous agent
        # Reuse the forecasting engine from parent
        self.autonomous_agent = GoalDrivenAgent(
            forecasting_config=None,  # Will use existing engine
            executor_config=executor_config,
            agent_config=agent_config
        )
        
        # Replace agent's forecasting engine with ours (shared instance)
        self.autonomous_agent.forecasting_engine = self.forecasting_engine
        
        # Start autonomous agent
        self.autonomous_agent.start()
        
        logger.info("Enhanced OrchestratorWithAutonomousAgent initialized with semantic memory")
    
    async def execute_with_autonomous_behavior(
        self,
        agent_name: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute agent task with enhanced autonomous behavior and memory-based optimization.
        """
        # ENHANCED: Use semantic memory to find optimal agent for this task
        task_type = context.get('task_type', 'general') if context else 'general'
        optimal_agent = self.semantic_memory.get_best_action(f"task_{task_type}")
        
        # If we have a better agent recommendation, use it
        if optimal_agent and optimal_agent != agent_name:
            logger.info(f"Using learned optimal agent {optimal_agent} for task type {task_type}")
            agent_name = optimal_agent
        
        # Record the execution event
        self.autonomous_agent.record_event(
            f"agent_execution_{agent_name}",
            metadata={"task": task_description, "task_type": task_type}
        )
        
        # Execute with forecasting (from parent class)
        result = await self.execute_with_forecasting(
            agent_name,
            task_description,
            context
        )
        
        # ENHANCED: Learn from this execution in semantic memory
        success = result.get('status') == 'success'
        self.semantic_memory.record_pattern(
            f"task_{task_type}",
            agent_name,
            success
        )
        
        # Record metrics for the autonomous agent
        if "metrics" in result:
            for metric_name, value in result["metrics"].items():
                self.autonomous_agent.record_metric(metric_name, value)
        
        # Add enhanced information to result
        agent_status = self.autonomous_agent.get_agent_status()
        result["autonomous_agent"] = {
            "running": agent_status["running"],
            "active_goals": agent_status["active_goals"],
            "uptime_seconds": agent_status["uptime_seconds"],
            "used_optimal_agent": optimal_agent is not None,
            "recommended_agent": optimal_agent
        }
        
        return result
    
    async def select_optimal_agent(
        self,
        task_description: str,
        required_capabilities: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        ENHANCED: Select optimal agent using semantic memory and capability matching.
        """
        task_type = context.get('task_type', 'general') if context else 'general'
        
        # First, try semantic memory for learned optimal agents
        optimal_agent = self.semantic_memory.get_best_action(f"task_{task_type}")
        
        if optimal_agent:
            logger.info(f"Using learned optimal agent {optimal_agent} for {task_type}")
            return optimal_agent
        
        # Fall back to capability-based selection
        # This would use your existing agent selection logic
        capable_agents = self._find_agents_by_capability(required_capabilities)
        
        if capable_agents:
            # Use the first capable agent, or implement more sophisticated selection
            return capable_agents[0]
        
        # Default fallback
        return "general_agent"
    
    def record_agent_success(
        self,
        agent_name: str,
        task_type: str,
        success: bool,
        metrics: Optional[Dict[str, Any]] = None
    ):
        """
        ENHANCED: Record agent success patterns for future optimization.
        """
        self.semantic_memory.record_pattern(f"task_{task_type}", agent_name, success)
        
        if metrics:
            # Learn from performance metrics
            latency = metrics.get('duration_ms', 0)
            if latency < 1000:  # Good performance
                self.semantic_memory.update_preference(
                    f"fast_{task_type}", 1.0, weight=0.1
                )
    
    def get_autonomous_report(self) -> Dict[str, Any]:
        """Get comprehensive autonomous agent report with enhanced insights."""
        base_report = self.autonomous_agent.get_comprehensive_report()
        
        # ENHANCED: Add semantic memory insights
        base_report["orchestrator_insights"] = {
            "learned_task_patterns": {
                task_type: self.semantic_memory.get_best_action(task_type)
                for task_type in list(self.semantic_memory.patterns.keys())[:10]
            },
            "total_learned_patterns": len(self.semantic_memory.patterns)
        }
        
        return base_report
    
    def get_goal_overview(self) -> Dict[str, Any]:
        """Get goal overview."""
        return self.autonomous_agent.get_goal_overview()
    
    def force_autonomous_analysis(self) -> Dict[str, Any]:
        """Manually trigger autonomous analysis."""
        return self.autonomous_agent.force_analysis()
    
    def set_autonomous_mode(self, enabled: bool):
        """Enable/disable autonomous mode."""
        self.autonomous_agent.set_autonomous_mode(enabled)
    
    def _find_agents_by_capability(self, capabilities: List[str]) -> List[str]:
        """
        Find agents by required capabilities.
        This would integrate with your existing agent registry.
        """
        # This is a placeholder - integrate with your actual agent discovery
        try:
            from core.agent_registry import get_agent_registry
            registry = get_agent_registry()
            matching_agents = registry.search(capabilities=capabilities)
            return [agent.name for agent in matching_agents]
        except:
            return []
    
    def shutdown(self):
        """Shutdown orchestrator and all components."""
        logger.info("Shutting down enhanced orchestrator with autonomous agent...")
        
        if self.autonomous_agent:
            self.autonomous_agent.stop()
        
        # Call parent shutdown
        super().shutdown()
        
        logger.info("Enhanced orchestrator shutdown complete")
