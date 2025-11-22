"""
Enhanced Performance Monitor with Semantic Memory for Pattern Learning
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from enum import Enum
import json
import time
import statistics
from collections import defaultdict, deque
from threading import Lock, Thread
import asyncio

# Kafka integration (optional dependency)
try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    KafkaProducer = None
    KafkaError = Exception

from utils.logging import get_logger
from database import get_session
from database.models import (
    AgentRun, Run, ModelVersion, LearningEvent,
    AgentRunStatus, RunStatus
)
from enhanced_memory import SemanticMemory

logger = get_logger(__name__)


class MetricType(str, Enum):
    """Types of metrics tracked."""
    SUCCESS_RATE = "success_rate"
    LATENCY = "latency"
    TOKEN_USAGE = "token_usage"
    API_CALLS = "api_calls"
    COST = "cost"
    MEMORY = "memory"
    CPU = "cpu"
    ACCURACY = "accuracy"
    QUALITY = "quality"
    ERROR_RATE = "error_rate"


class AlertLevel(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    
    # Success metrics
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    partial_tasks: int = 0
    success_rate: float = 0.0
    
    # Timing metrics
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    
    # Resource metrics
    total_tokens: int = 0
    total_api_calls: int = 0
    total_cost: float = 0.0
    avg_memory_mb: float = 0.0
    avg_cpu_ms: float = 0.0
    
    # Quality metrics
    avg_quality_score: float = 0.0
    avg_confidence: float = 0.0
    avg_accuracy: float = 0.0
    
    # Error metrics
    error_rate: float = 0.0
    timeout_rate: float = 0.0
    retry_rate: float = 0.0
    
    # Trend indicators
    success_rate_trend: str = "stable"  # "improving", "stable", "degrading"
    latency_trend: str = "stable"
    cost_trend: str = "stable"
    
    # Metadata
    window_start: Optional[str] = None
    window_end: Optional[str] = None
    sample_size: int = 0


@dataclass
class AgentPerformance:
    """Performance metrics for a specific agent."""
    agent_name: str
    agent_type: str
    metrics: PerformanceMetrics
    last_run: Optional[str] = None
    status: str = "active"
    
    # Agent-specific insights
    specialization_score: float = 0.0  # How well agent performs its specialty
    reliability_score: float = 0.0  # Consistency of performance
    efficiency_score: float = 0.0  # Speed vs quality balance
    
    
@dataclass
class PerformanceAlert:
    """Alert for performance issues."""
    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    message: str
    current_value: Any
    threshold: Any
    agent_name: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    recommendation: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccuracyMeasurement:
    """Measurement of model/agent accuracy against real outcomes."""
    measurement_id: str
    agent_name: str
    task_id: str
    predicted_outcome: Any
    actual_outcome: Any
    accuracy_score: float  # 0-1
    timestamp: str
    feedback_source: str  # "user", "automated", "system"
    metadata: Dict[str, Any] = field(default_factory=dict)


class PerformanceMonitor:
    """
    Enhanced Performance Monitor with Semantic Memory for pattern learning.
    """
    
    def __init__(
        self,
        window_size_minutes: int = 60,
        alert_thresholds: Optional[Dict[str, Any]] = None,
        enable_auto_alerts: bool = True,
        enable_trend_analysis: bool = True,
        enable_auto_retraining: bool = True,
        model_updater = None,
        db_session_factory=None,
        kafka_servers: Optional[str] = None,
        kafka_topic: str = "agent-outcomes"
    ):
        """
        Initialize Enhanced Performance Monitor.
        """
        self.window_size_minutes = window_size_minutes
        self.enable_auto_alerts = enable_auto_alerts
        self.enable_trend_analysis = enable_trend_analysis
        self.enable_auto_retraining = enable_auto_retraining
        self.model_updater = model_updater
        self.db_session_factory = db_session_factory or get_session
        self.kafka_topic = kafka_topic
        
        # ENHANCED: Initialize semantic memory for pattern learning
        self.semantic_memory = SemanticMemory()
        
        # Initialize Kafka producer (if available and configured)
        self.producer = None
        if KAFKA_AVAILABLE and kafka_servers:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=kafka_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    acks='all',
                    retries=3,
                    max_in_flight_requests_per_connection=1
                )
                logger.info(f"✅ Kafka producer initialized (servers={kafka_servers}, topic={kafka_topic})")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {e}")
                self.producer = None
        elif not KAFKA_AVAILABLE:
            logger.warning(
                "⚠️  Kafka not available. Install kafka-python to enable event streaming to RealTimeModelUpdater. "
                "Run: pip install kafka-python"
            )
        elif not kafka_servers:
            logger.warning(
                "⚠️  Kafka servers not configured. PerformanceMonitor will not produce events to Kafka. "
                "Set kafka_servers parameter to enable streaming to RealTimeModelUpdater."
            )
        
        # Default alert thresholds
        self.alert_thresholds = {
            "success_rate_min": 0.80,
            "error_rate_max": 0.15,
            "latency_p95_max_ms": 5000,
            "cost_per_task_max": 1.0,
            "accuracy_min": 0.70,
            "memory_max_mb": 1024,
            "token_per_task_max": 5000,
        }
        if alert_thresholds:
            self.alert_thresholds.update(alert_thresholds)
        
        # In-memory metric storage
        self._lock = Lock()
        self._metrics_buffer: deque = deque(maxlen=10000)
        self._agent_metrics: Dict[str, List[Dict]] = defaultdict(list)
        self._accuracy_measurements: deque = deque(maxlen=1000)
        self._alerts: deque = deque(maxlen=100)
        
        # Running statistics
        self._running_stats: Dict[str, Any] = defaultdict(dict)
        
        # Background processing
        self._monitoring_active = False
        self._monitor_thread: Optional[Thread] = None
        
        logger.info(
            f"Enhanced PerformanceMonitor initialized with semantic memory "
            f"(window={window_size_minutes}m, auto_alerts={enable_auto_alerts})"
        )
    
    def start(self):
        """Start background monitoring thread."""
        if self._monitoring_active:
            logger.warning("PerformanceMonitor already running")
            return
        
        self._monitoring_active = True
        self._monitor_thread = Thread(target=self._background_monitor, daemon=True)
        self._monitor_thread.start()
        logger.info("PerformanceMonitor background thread started")
    
    def stop(self):
        """Stop background monitoring."""
        self._monitoring_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        
        if self.producer:
            try:
                self.producer.flush()
                self.producer.close()
                logger.info("Kafka producer closed")
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {e}")
        
        logger.info("PerformanceMonitor stopped")
    
    def _background_monitor(self):
        """Background thread for periodic monitoring tasks."""
        while self._monitoring_active:
            try:
                # Perform periodic analysis
                self._analyze_trends()
                self._check_alerts()
                self._cleanup_old_data()
                
                # ENHANCED: Learn patterns from recent data
                self._learn_performance_patterns()
                
                # Sleep for a minute
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in background monitor: {e}", exc_info=True)
    
    def _learn_performance_patterns(self):
        """Learn performance patterns using semantic memory."""
        try:
            # Get recent agent runs
            with self._lock:
                recent_runs = list(self._metrics_buffer)[-100:]  # Last 100 runs
            
            for run in recent_runs:
                agent_type = run.get('agent_type', 'unknown')
                agent_name = run.get('agent_name', 'unknown')
                status = run.get('status', 'unknown')
                
                # Learn agent-type patterns
                self.semantic_memory.record_pattern(
                    f"agent_type_{agent_type}",
                    agent_name,
                    status == 'success'
                )
                
                # Learn time-based patterns (hour of day)
                timestamp = run.get('timestamp', '')
                if timestamp:
                    try:
                        hour = datetime.fromisoformat(timestamp).hour
                        self.semantic_memory.record_pattern(
                            f"hour_{hour}",
                            agent_type,
                            status == 'success'
                        )
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Error learning performance patterns: {e}", exc_info=True)
    
    def record_agent_run(
        self,
        run_id: str,
        agent_name: str,
        agent_type: str,
        status: str,
        duration_ms: float,
        tokens_used: Optional[int] = None,
        cost: Optional[float] = None,
        memory_mb: Optional[float] = None,
        cpu_ms: Optional[float] = None,
        quality_score: Optional[float] = None,
        confidence: Optional[float] = None,
        error_type: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Record an agent run event with enhanced pattern learning.
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": run_id,
            "agent_name": agent_name,
            "agent_type": agent_type,
            "status": status,
            "duration_ms": duration_ms,
            "tokens_used": tokens_used or 0,
            "cost": cost or 0.0,
            "memory_mb": memory_mb or 0.0,
            "cpu_ms": cpu_ms or 0.0,
            "quality_score": quality_score,
            "confidence": confidence,
            "error_type": error_type,
            "metadata": metadata or {}
        }
        
        with self._lock:
            self._metrics_buffer.append(event)
            self._agent_metrics[agent_name].append(event)
            
            if len(self._agent_metrics[agent_name]) > 1000:
                self._agent_metrics[agent_name] = self._agent_metrics[agent_name][-1000:]
        
        # ENHANCED: Learn agent-task patterns in semantic memory
        task_type = metadata.get('task_type', 'general') if metadata else 'general'
        self.semantic_memory.record_pattern(
            f"task_{task_type}",
            agent_name,
            status == 'success'
        )
        
        # Produce to Kafka
        if self.producer:
            try:
                self.producer.send(self.kafka_topic, value=event)
                logger.debug(f"📤 Produced event to Kafka topic '{self.kafka_topic}': {agent_name} ({status})")
            except Exception as e:
                logger.error(f"❌ Failed to produce performance event to Kafka: {e}")
        
        # Check for immediate alerts
        if self.enable_auto_alerts:
            self._check_event_alerts(event)
        
        logger.debug(f"Recorded performance event for {agent_name}: {status}")
    
    def get_optimal_agent_for_task(self, task_type: str) -> Optional[str]:
        """
        ENHANCED: Get the best performing agent for a specific task type.
        """
        return self.semantic_memory.get_best_action(f"task_{task_type}")
    
    def get_agent_success_rate(self, agent_name: str, task_type: str = "all") -> float:
        """
        ENHANCED: Get agent success rate for specific task type using semantic memory.
        """
        if task_type == "all":
            # Calculate overall success rate
            with self._lock:
                agent_runs = self._agent_metrics.get(agent_name, [])
                if not agent_runs:
                    return 0.0
                successful = sum(1 for run in agent_runs if run.get('status') == 'success')
                return successful / len(agent_runs)
        else:
            # Use semantic memory for task-specific success rate
            pattern_key = f"task_{task_type}_{agent_name}"
            stats = self.semantic_memory.success_rates.get(pattern_key, {'success': 0, 'total': 0})
            if stats['total'] == 0:
                return 0.0
            return stats['success'] / stats['total']
    
    def record_accuracy(
        self,
        agent_name: str,
        task_id: str,
        predicted_outcome: Any,
        actual_outcome: Any,
        feedback_source: str = "user",
        metadata: Optional[Dict] = None
    ):
        """
        Record accuracy measurement against real-world outcome.
        """
        accuracy_score = self._calculate_accuracy_score(predicted_outcome, actual_outcome)
        
        measurement = AccuracyMeasurement(
            measurement_id=f"{task_id}_{int(time.time()*1000)}",
            agent_name=agent_name,
            task_id=task_id,
            predicted_outcome=predicted_outcome,
            actual_outcome=actual_outcome,
            accuracy_score=accuracy_score,
            timestamp=datetime.utcnow().isoformat(),
            feedback_source=feedback_source,
            metadata=metadata or {}
        )
        
        with self._lock:
            self._accuracy_measurements.append(asdict(measurement))
        
        # ENHANCED: Learn accuracy patterns
        task_type = metadata.get('task_type', 'general') if metadata else 'general'
        self.semantic_memory.record_pattern(
            f"accuracy_{task_type}",
            agent_name,
            accuracy_score > 0.7  # Consider above 70% as success
        )
        
        logger.info(
            f"Recorded accuracy for {agent_name}: {accuracy_score:.2f} "
            f"(source={feedback_source})"
        )
    
    def _calculate_accuracy_score(self, predicted: Any, actual: Any) -> float:
        """Calculate accuracy score between predicted and actual outcomes."""
        try:
            if predicted == actual:
                return 1.0
            
            if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
                if actual == 0:
                    return 0.0 if predicted != 0 else 1.0
                error = abs(predicted - actual) / abs(actual)
                return max(0.0, 1.0 - error)
            
            if isinstance(predicted, str) and isinstance(actual, str):
                pred_words = set(predicted.lower().split())
                actual_words = set(actual.lower().split())
                if not actual_words:
                    return 0.0
                overlap = len(pred_words & actual_words)
                return overlap / len(actual_words)
            
            if isinstance(predicted, dict) and isinstance(actual, dict):
                if not actual:
                    return 1.0 if not predicted else 0.0
                key_overlap = len(set(predicted.keys()) & set(actual.keys()))
                key_score = key_overlap / len(actual.keys())
                
                value_scores = []
                for key in set(predicted.keys()) & set(actual.keys()):
                    value_scores.append(
                        self._calculate_accuracy_score(predicted[key], actual[key])
                    )
                value_score = statistics.mean(value_scores) if value_scores else 0.0
                
                return (key_score + value_score) / 2
            
            if isinstance(predicted, list) and isinstance(actual, list):
                if not actual:
                    return 1.0 if not predicted else 0.0
                overlap = len(set(predicted) & set(actual))
                return overlap / len(actual)
            
            return 0.3 if type(predicted) == type(actual) else 0.0
            
        except Exception as e:
            logger.warning(f"Error calculating accuracy: {e}")
            return 0.0
    
    def get_system_metrics(
        self,
        time_window_minutes: Optional[int] = None
    ) -> PerformanceMetrics:
        """Get system-wide performance metrics."""
        window = time_window_minutes or self.window_size_minutes
        cutoff_time = datetime.utcnow() - timedelta(minutes=window)
        
        with self._lock:
            events = [
                e for e in self._metrics_buffer
                if datetime.fromisoformat(e["timestamp"]) >= cutoff_time
            ]
        
        return self._calculate_metrics(events)
    
    def get_agent_metrics(
        self,
        agent_name: str,
        time_window_minutes: Optional[int] = None
    ) -> AgentPerformance:
        """Get performance metrics for a specific agent."""
        window = time_window_minutes or self.window_size_minutes
        cutoff_time = datetime.utcnow() - timedelta(minutes=window)
        
        with self._lock:
            if agent_name not in self._agent_metrics:
                return AgentPerformance(
                    agent_name=agent_name,
                    agent_type="unknown",
                    metrics=PerformanceMetrics()
                )
            
            events = [
                e for e in self._agent_metrics[agent_name]
                if datetime.fromisoformat(e["timestamp"]) >= cutoff_time
            ]
        
        if not events:
            return AgentPerformance(
                agent_name=agent_name,
                agent_type="unknown",
                metrics=PerformanceMetrics(),
                status="inactive"
            )
        
        metrics = self._calculate_metrics(events)
        agent_type = events[0]["agent_type"]
        last_run = events[-1]["timestamp"]
        
        specialization_score = self._calculate_specialization_score(events)
        reliability_score = metrics.success_rate
        efficiency_score = self._calculate_efficiency_score(metrics)
        
        return AgentPerformance(
            agent_name=agent_name,
            agent_type=agent_type,
            metrics=metrics,
            last_run=last_run,
            status="active",
            specialization_score=specialization_score,
            reliability_score=reliability_score,
            efficiency_score=efficiency_score
        )
    
    def _calculate_metrics(self, events: List[Dict]) -> PerformanceMetrics:
        """Calculate performance metrics from event list."""
        if not events:
            return PerformanceMetrics()
        
        total = len(events)
        successful = sum(1 for e in events if e["status"] == "success")
        failed = sum(1 for e in events if e["status"] == "failure")
        partial = sum(1 for e in events if e["status"] == "partial")
        
        latencies = [e["duration_ms"] for e in events]
        latencies.sort()
        
        total_tokens = sum(e.get("tokens_used", 0) for e in events)
        total_cost = sum(e.get("cost", 0.0) for e in events)
        memory_values = [e.get("memory_mb", 0) for e in events if e.get("memory_mb")]
        cpu_values = [e.get("cpu_ms", 0) for e in events if e.get("cpu_ms")]
        
        quality_values = [
            e["quality_score"] for e in events
            if e.get("quality_score") is not None
        ]
        confidence_values = [
            e["confidence"] for e in events
            if e.get("confidence") is not None
        ]
        
        accuracy_values = self._get_accuracy_for_events(events)
        
        return PerformanceMetrics(
            total_tasks=total,
            successful_tasks=successful,
            failed_tasks=failed,
            partial_tasks=partial,
            success_rate=successful / total if total > 0 else 0.0,
            
            avg_latency_ms=statistics.mean(latencies) if latencies else 0.0,
            p50_latency_ms=latencies[len(latencies)//2] if latencies else 0.0,
            p95_latency_ms=latencies[int(len(latencies)*0.95)] if latencies else 0.0,
            p99_latency_ms=latencies[int(len(latencies)*0.99)] if latencies else 0.0,
            max_latency_ms=max(latencies) if latencies else 0.0,
            
            total_tokens=total_tokens,
            total_api_calls=total,
            total_cost=total_cost,
            avg_memory_mb=statistics.mean(memory_values) if memory_values else 0.0,
            avg_cpu_ms=statistics.mean(cpu_values) if cpu_values else 0.0,
            
            avg_quality_score=statistics.mean(quality_values) if quality_values else 0.0,
            avg_confidence=statistics.mean(confidence_values) if confidence_values else 0.0,
            avg_accuracy=statistics.mean(accuracy_values) if accuracy_values else 0.0,
            
            error_rate=failed / total if total > 0 else 0.0,
            timeout_rate=sum(1 for e in events if e.get("error_type") == "timeout") / total if total > 0 else 0.0,
            retry_rate=sum(1 for e in events if e.get("metadata", {}).get("retry_count", 0) > 0) / total if total > 0 else 0.0,
            
            window_start=events[0]["timestamp"] if events else None,
            window_end=events[-1]["timestamp"] if events else None,
            sample_size=total
        )
    
    def _get_accuracy_for_events(self, events: List[Dict]) -> List[float]:
        """Get accuracy measurements matching the given events."""
        with self._lock:
            accuracies = []
            event_ids = {e["run_id"] for e in events}
            
            for measurement in self._accuracy_measurements:
                if measurement["task_id"] in event_ids:
                    accuracies.append(measurement["accuracy_score"])
            
            return accuracies
    
    def _calculate_specialization_score(self, events: List[Dict]) -> float:
        """Calculate how well an agent performs its specialized tasks."""
        if not events:
            return 0.0
        
        success_count = 0
        quality_sum = 0.0
        
        for event in events:
            if event["status"] == "success":
                success_count += 1
                quality_sum += event.get("quality_score", 0.5)
        
        if success_count == 0:
            return 0.0
        
        avg_quality = quality_sum / success_count
        success_rate = success_count / len(events)
        
        return (success_rate + avg_quality) / 2
    
    def _calculate_efficiency_score(self, metrics: PerformanceMetrics) -> float:
        """Calculate efficiency score (balance of speed and quality)."""
        if metrics.total_tasks == 0:
            return 0.0
        
        latency_score = max(0.0, 1.0 - (metrics.avg_latency_ms - 1000) / 4000)
        quality_score = metrics.avg_quality_score
        success_score = metrics.success_rate
        
        efficiency = (
            0.3 * latency_score +
            0.4 * quality_score +
            0.3 * success_score
        )
        
        return max(0.0, min(1.0, efficiency))
    
    def _check_event_alerts(self, event: Dict):
        """Check if single event triggers any alerts."""
        alerts = []
        
        if event["duration_ms"] > self.alert_thresholds["latency_p95_max_ms"]:
            alerts.append(PerformanceAlert(
                alert_id=f"latency_{event['run_id']}",
                level=AlertLevel.WARNING,
                metric_type=MetricType.LATENCY,
                message=f"High latency detected for {event['agent_name']}",
                current_value=event["duration_ms"],
                threshold=self.alert_thresholds["latency_p95_max_ms"],
                agent_name=event["agent_name"],
                recommendation="Check agent workload and LLM performance"
            ))
        
        if event.get("memory_mb", 0) > self.alert_thresholds["memory_max_mb"]:
            alerts.append(PerformanceAlert(
                alert_id=f"memory_{event['run_id']}",
                level=AlertLevel.CRITICAL,
                metric_type=MetricType.MEMORY,
                message=f"High memory usage by {event['agent_name']}",
                current_value=event["memory_mb"],
                threshold=self.alert_thresholds["memory_max_mb"],
                agent_name=event["agent_name"],
                recommendation="Investigate memory leaks or optimize data structures"
            ))
        
        if alerts:
            with self._lock:
                self._alerts.extend(alerts)
            
            for alert in alerts:
                logger.warning(f"ALERT: {alert.message}")
    
    def _check_alerts(self):
        """Periodic alert checking based on aggregated metrics."""
        if not self.enable_auto_alerts:
            return
        
        try:
            metrics = self.get_system_metrics()
            
            alerts = []
            
            if metrics.success_rate < self.alert_thresholds["success_rate_min"]:
                alerts.append(PerformanceAlert(
                    alert_id=f"success_rate_{int(time.time())}",
                    level=AlertLevel.CRITICAL,
                    metric_type=MetricType.SUCCESS_RATE,
                    message="System success rate below threshold",
                    current_value=metrics.success_rate,
                    threshold=self.alert_thresholds["success_rate_min"],
                    recommendation="Review recent failures and adjust agent configurations"
                ))
            
            if metrics.error_rate > self.alert_thresholds["error_rate_max"]:
                alerts.append(PerformanceAlert(
                    alert_id=f"error_rate_{int(time.time())}",
                    level=AlertLevel.WARNING,
                    metric_type=MetricType.ERROR_RATE,
                    message="High error rate detected",
                    current_value=metrics.error_rate,
                    threshold=self.alert_thresholds["error_rate_max"],
                    recommendation="Check logs for common error patterns"
                ))
            
            if metrics.total_tasks > 0:
                cost_per_task = metrics.total_cost / metrics.total_tasks
                if cost_per_task > self.alert_thresholds["cost_per_task_max"]:
                    alerts.append(PerformanceAlert(
                        alert_id=f"cost_{int(time.time())}",
                        level=AlertLevel.WARNING,
                        metric_type=MetricType.COST,
                        message="High cost per task detected",
                        current_value=cost_per_task,
                        threshold=self.alert_thresholds["cost_per_task_max"],
                        recommendation="Optimize LLM prompts or consider cheaper models"
                    ))
            
            if metrics.avg_accuracy > 0 and metrics.avg_accuracy < self.alert_thresholds["accuracy_min"]:
                alerts.append(PerformanceAlert(
                    alert_id=f"accuracy_{int(time.time())}",
                    level=AlertLevel.CRITICAL,
                    metric_type=MetricType.ACCURACY,
                    message="Low accuracy against real-world outcomes",
                    current_value=metrics.avg_accuracy,
                    threshold=self.alert_thresholds["accuracy_min"],
                    recommendation="Review model training data and retrain if necessary"
                ))
                
                if self.enable_auto_retraining and self.model_updater:
                    logger.warning(
                        f"🚨 Accuracy degraded to {metrics.avg_accuracy:.1%} "
                        f"(threshold: {self.alert_thresholds['accuracy_min']:.1%}) - "
                        f"Triggering autonomous retraining..."
                    )
                    
                    try:
                        from core.online_learning import ModelType
                        
                        retrain_result = self.model_updater.trigger_retraining(
                            model_type=ModelType.AGENT_SELECTION,
                            reason=f"Accuracy dropped to {metrics.avg_accuracy:.1%}",
                            force_full_retrain=False
                        )
                        
                        if retrain_result.get('success'):
                            logger.info(
                                f"✅ Autonomous retraining completed: "
                                f"{retrain_result.get('events_processed', 0)} events processed"
                            )
                            
                            alerts.append(PerformanceAlert(
                                alert_id=f"retrain_success_{int(time.time())}",
                                level=AlertLevel.INFO,
                                metric_type=MetricType.ACCURACY,
                                message="Autonomous retraining completed successfully",
                                current_value=retrain_result.get('events_processed', 0),
                                threshold=0,
                                recommendation="Monitor accuracy over next hour to verify improvement",
                                details=retrain_result
                            ))
                        else:
                            logger.error(f"Autonomous retraining failed: {retrain_result.get('error')}")
                            
                    except Exception as e:
                        logger.error(f"Failed to trigger autonomous retraining: {e}", exc_info=True)
            
            if alerts:
                with self._lock:
                    self._alerts.extend(alerts)
                
                for alert in alerts:
                    logger.warning(f"PERIODIC ALERT: {alert.message}")
        
        except Exception as e:
            logger.error(f"Error checking alerts: {e}", exc_info=True)
    
    def _analyze_trends(self):
        """Analyze performance trends."""
        if not self.enable_trend_analysis:
            return
        
        try:
            current_metrics = self.get_system_metrics(time_window_minutes=60)
            previous_metrics = self.get_system_metrics(time_window_minutes=120)
            
            success_rate_trend = self._calculate_trend(
                previous_metrics.success_rate,
                current_metrics.success_rate
            )
            
            latency_trend = self._calculate_trend(
                previous_metrics.avg_latency_ms,
                current_metrics.avg_latency_ms,
                inverse=True
            )
            
            cost_trend = self._calculate_trend(
                previous_metrics.total_cost / max(previous_metrics.total_tasks, 1),
                current_metrics.total_cost / max(current_metrics.total_tasks, 1),
                inverse=True
            )
            
            current_metrics.success_rate_trend = success_rate_trend
            current_metrics.latency_trend = latency_trend
            current_metrics.cost_trend = cost_trend
            
            with self._lock:
                self._running_stats["trends"] = {
                    "success_rate": success_rate_trend,
                    "latency": latency_trend,
                    "cost": cost_trend,
                    "updated_at": datetime.utcnow().isoformat()
                }
        
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}", exc_info=True)
    
    def _calculate_trend(
        self,
        previous_value: float,
        current_value: float,
        inverse: bool = False
    ) -> str:
        """Calculate trend direction."""
        if previous_value == 0:
            return "stable"
        
        change_pct = (current_value - previous_value) / previous_value
        
        if abs(change_pct) < 0.05:
            return "stable"
        
        if inverse:
            return "improving" if change_pct < 0 else "degrading"
        else:
            return "improving" if change_pct > 0 else "degrading"
    
    def generate_report(
        self,
        include_agents: bool = True,
        time_window_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance report with enhanced insights.
        """
        system_metrics = self.get_system_metrics(time_window_minutes)
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "time_window_minutes": time_window_minutes or self.window_size_minutes,
            "system_metrics": asdict(system_metrics),
            "health_score": self._calculate_health_score(system_metrics),
            # ENHANCED: Add semantic memory insights
            "learned_patterns": {
                "total_patterns": len(self.semantic_memory.patterns),
                "top_agent_patterns": dict(list(self.semantic_memory.patterns.items())[:10])
            }
        }
        
        if include_agents:
            with self._lock:
                agent_names = list(self._agent_metrics.keys())
            
            report["agent_metrics"] = {
                agent_name: asdict(self.get_agent_metrics(agent_name, time_window_minutes))
                for agent_name in agent_names
            }
        
        recent_alerts = self.get_alerts(limit=20)
        report["recent_alerts"] = [asdict(alert) for alert in recent_alerts]
        
        report["recommendations"] = self._generate_recommendations(system_metrics)
        
        return report
    
    def _calculate_health_score(self, metrics: PerformanceMetrics) -> float:
        """Calculate overall system health score (0-100)."""
        if metrics.total_tasks == 0:
            return 100.0
        
        success_score = metrics.success_rate * 40
        latency_score = max(0, 30 - (metrics.avg_latency_ms / 1000) * 3)
        error_score = max(0, 20 - (metrics.error_rate * 100))
        accuracy_score = metrics.avg_accuracy * 10 if metrics.avg_accuracy > 0 else 10
        
        health_score = success_score + latency_score + error_score + accuracy_score
        
        return min(100.0, max(0.0, health_score))
    
    def _generate_recommendations(self, metrics: PerformanceMetrics) -> List[str]:
        """Generate actionable recommendations based on metrics."""
        recommendations = []
        
        if metrics.success_rate < 0.90:
            recommendations.append(
                f"Success rate is {metrics.success_rate:.1%}. "
                "Review failure logs and consider adjusting agent prompts or retry strategies."
            )
        
        if metrics.avg_latency_ms > 3000:
            recommendations.append(
                f"Average latency is {metrics.avg_latency_ms:.0f}ms. "
                "Consider using faster LLM models or implementing caching."
            )
        
        if metrics.total_tasks > 0:
            cost_per_task = metrics.total_cost / metrics.total_tasks
            if cost_per_task > 0.50:
                recommendations.append(
                    f"Cost per task is ${cost_per_task:.2f}. "
                    "Optimize prompts, reduce token usage, or switch to cheaper models."
                )
        
        if metrics.avg_accuracy > 0 and metrics.avg_accuracy < 0.75:
            recommendations.append(
                f"Accuracy is {metrics.avg_accuracy:.1%}. "
                "Consider retraining models with recent feedback data."
            )
        
        if metrics.error_rate > 0.10:
            recommendations.append(
                f"Error rate is {metrics.error_rate:.1%}. "
                "Implement better error handling and increase retry limits."
            )
        
        # ENHANCED: Add recommendations based on learned patterns
        if hasattr(self, 'semantic_memory'):
            low_success_agents = [
                agent for agent in self._agent_metrics.keys()
                if self.get_agent_success_rate(agent) < 0.7
            ]
            if low_success_agents:
                recommendations.append(
                    f"Agents with low success rates: {', '.join(low_success_agents)}. "
                    "Consider retraining or replacing these agents."
                )
        
        if not recommendations:
            recommendations.append("System is performing well. No immediate actions needed.")
        
        return recommendations
    
    def get_alerts(
        self,
        level: Optional[AlertLevel] = None,
        agent_name: Optional[str] = None,
        limit: int = 50
    ) -> List[PerformanceAlert]:
        """Get recent alerts."""
        with self._lock:
            alerts = list(self._alerts)
        
        if level:
            alerts = [a for a in alerts if a.level == level]
        if agent_name:
            alerts = [a for a in alerts if a.agent_name == agent_name]
        
        return alerts[-limit:]
    
    def sync_with_database(self, lookback_hours: int = 24):
        """Sync performance metrics from database."""
        try:
            db = self.db_session_factory()
            cutoff_time = datetime.utcnow() - timedelta(hours=lookback_hours)
            
            agent_runs = db.query(AgentRun).filter(
                AgentRun.created_at >= cutoff_time
            ).all()
            
            logger.info(f"Syncing {len(agent_runs)} agent runs from database")
            
            for agent_run in agent_runs:
                status = "success" if agent_run.status == AgentRunStatus.COMPLETED else "failure"
                
                self.record_agent_run(
                    run_id=agent_run.run_id,
                    agent_name=agent_run.agent_name,
                    agent_type=agent_run.agent_type,
                    status=status,
                    duration_ms=agent_run.execution_time_ms or 0,
                    metadata=agent_run.output_data or {}
                )
            
            db.close()
            logger.info("Database sync completed")
            
        except Exception as e:
            logger.error(f"Error syncing with database: {e}", exc_info=True)
    
    def _cleanup_old_data(self):
        """Clean up old data to prevent memory bloat."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            with self._lock:
                self._metrics_buffer = deque(
                    [e for e in self._metrics_buffer
                     if datetime.fromisoformat(e["timestamp"]) >= cutoff_time],
                    maxlen=10000
                )
                
                for agent_name in list(self._agent_metrics.keys()):
                    self._agent_metrics[agent_name] = [
                        e for e in self._agent_metrics[agent_name]
                        if datetime.fromisoformat(e["timestamp"]) >= cutoff_time
                    ]
                
                self._accuracy_measurements = deque(
                    [m for m in self._accuracy_measurements
                     if datetime.fromisoformat(m["timestamp"]) >= cutoff_time],
                    maxlen=1000
                )
        
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}", exc_info=True)
    
    def trigger_retraining(
        self,
        reason: str = "Manual trigger from PerformanceMonitor",
        force_full_retrain: bool = False
    ) -> Dict[str, Any]:
        """Manually trigger model retraining."""
        if not self.model_updater:
            logger.error("Cannot trigger retraining: model_updater not configured")
            return {
                'success': False,
                'error': 'No model updater configured'
            }
        
        try:
            from core.online_learning import ModelType
            
            logger.info(f"Manually triggering retraining: {reason}")
            
            result = self.model_updater.trigger_retraining(
                model_type=ModelType.AGENT_SELECTION,
                reason=reason,
                force_full_retrain=force_full_retrain
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to trigger retraining: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get monitor statistics."""
        with self._lock:
            return {
                "events_buffered": len(self._metrics_buffer),
                "agents_tracked": len(self._agent_metrics),
                "accuracy_measurements": len(self._accuracy_measurements),
                "active_alerts": len(self._alerts),
                "monitoring_active": self._monitoring_active,
                "auto_retraining_enabled": self.enable_auto_retraining,
                "model_updater_connected": self.model_updater is not None,
                "kafka_producer_connected": self.producer is not None,
                "kafka_topic": self.kafka_topic if self.producer else None,
                # ENHANCED: Add semantic memory stats
                "learned_patterns": len(self.semantic_memory.patterns),
                "success_rates_tracked": len(self.semantic_memory.success_rates)
            }
    
    def __repr__(self) -> str:
        """String representation."""
        stats = self.get_stats()
        return (
            f"<EnhancedPerformanceMonitor(events={stats['events_buffered']}, "
            f"agents={stats['agents_tracked']}, patterns={stats['learned_patterns']})>"
        )


# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
        _performance_monitor.start()
    return _performance_monitor


def init_performance_monitor(
    kafka_servers: Optional[str] = None,
    kafka_topic: str = "agent-outcomes",
    **kwargs
) -> PerformanceMonitor:
    """
    Initialize global performance monitor with custom settings.
    """
    global _performance_monitor
    if _performance_monitor is not None:
        _performance_monitor.stop()
    
    _performance_monitor = PerformanceMonitor(
        kafka_servers=kafka_servers,
        kafka_topic=kafka_topic,
        **kwargs
    )
    _performance_monitor.start()
    return _performance_monitor
