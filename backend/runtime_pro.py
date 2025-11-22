
"""
POWERHOUSE Runtime-Pro
Advanced runtime with enterprise governance, policies, and monitoring
"""
import os
import time
from typing import Dict, Any, List, Optional
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from telemetry.events import TelemetryClient

class RuntimeProPolicy:
    """Pro runtime policy (more flexible than Lite)"""
    
    def __init__(self, tenant_overrides: Optional[Dict[str, Any]] = None):
        # Default limits (higher than Lite)
        self.max_cpu = int(os.getenv('PH_DEFAULT_CPU_LIMIT', 4))
        self.max_mem_mb = int(os.getenv('PH_DEFAULT_MEM_MB', 8192))
        self.max_duration_s = int(os.getenv('PH_DEFAULT_TIMEOUT_S', 3600))
        
        # Allowed domains (more permissive)
        self.allowed_domains = [
            'api.openai.com',
            'cdn.dracanus.app',
            # Enterprises can add custom domains via tenant_overrides
        ]
        
        # Allowed permissions (more than Lite)
        self.allowed_permissions = [
            'filesystem.read',
            'filesystem.write',  # Allowed in Pro
            'network.http',
            'network.https',
            'database.read',
            'database.write',
            # email.send and payment.charge still require explicit approval
        ]
        
        # Apply tenant-specific overrides
        if tenant_overrides:
            self.apply_overrides(tenant_overrides)
    
    def apply_overrides(self, overrides: Dict[str, Any]):
        """Apply tenant-specific policy overrides"""
        if 'max_cpu' in overrides:
            self.max_cpu = overrides['max_cpu']
        if 'max_mem_mb' in overrides:
            self.max_mem_mb = overrides['max_mem_mb']
        if 'max_duration_s' in overrides:
            self.max_duration_s = overrides['max_duration_s']
        if 'allowed_domains' in overrides:
            self.allowed_domains.extend(overrides['allowed_domains'])
        if 'allowed_permissions' in overrides:
            self.allowed_permissions.extend(overrides['allowed_permissions'])

class RuntimePro:
    """
    Pro runtime for Powerhouse
    Enterprise-grade with governance, audit, and advanced policies
    """
    
    def __init__(
        self,
        org_id: str,
        user_id: str,
        policy: Optional[RuntimeProPolicy] = None,
        telemetry: Optional[TelemetryClient] = None
    ):
        self.org_id = org_id
        self.user_id = user_id
        self.policy = policy or RuntimeProPolicy()
        self.telemetry = telemetry or TelemetryClient()
    
    def validate_manifest(self, manifest: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate agent manifest against Pro policy"""
        violations = []
        
        # Check resources
        resources = manifest.get('resources', {})
        if resources.get('cpu', 0) > self.policy.max_cpu:
            violations.append(f"CPU limit exceeded: {resources['cpu']} > {self.policy.max_cpu}")
        
        if resources.get('mem_mb', 0) > self.policy.max_mem_mb:
            violations.append(f"Memory limit exceeded: {resources['mem_mb']} > {self.policy.max_mem_mb} MB")
        
        # Check permissions
        permissions = manifest.get('permissions', [])
        for perm in permissions:
            if perm not in self.policy.allowed_permissions:
                violations.append(f"Permission not allowed: {perm}")
        
        # Check domains (more lenient in Pro)
        domains = manifest.get('domains_allow', [])
        for domain in domains:
            if domain not in self.policy.allowed_domains:
                # In Pro, log a warning but don't block
                print(f"Warning: Domain {domain} not in default allowlist. Check tenant policy.")
        
        return len(violations) == 0, violations
    
    def execute(
        self,
        agent_id: str,
        manifest: Dict[str, Any],
        inputs: Dict[str, Any],
        deployment_id: str
    ) -> Dict[str, Any]:
        """
        Execute agent with Pro runtime governance
        
        Args:
            agent_id: Agent identifier
            manifest: Agent manifest
            inputs: Execution inputs
            deployment_id: Deployment identifier
        
        Returns:
            Execution result with audit trail
        """
        start_time = time.time()
        execution_id = self._generate_execution_id()
        
        try:
            # Step 1: Validate manifest
            is_valid, violations = self.validate_manifest(manifest)
            if not is_valid:
                error_msg = f"Policy violations: {', '.join(violations)}"
                self._audit_log(execution_id, 'BLOCKED', error_msg)
                self.telemetry.emit_runtime_blocked(self.user_id, agent_id, error_msg)
                return {
                    'success': False,
                    'execution_id': execution_id,
                    'error': 'POLICY_VIOLATION',
                    'violations': violations
                }
            
            # Step 2: Launch container with Pro resources
            self._audit_log(execution_id, 'STARTED', f'Agent {agent_id} execution started')
            
            container_result = self._launch_container(
                manifest=manifest,
                inputs=inputs,
                cpu_limit=self.policy.max_cpu,
                mem_limit_mb=self.policy.max_mem_mb,
                timeout_s=self.policy.max_duration_s
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            self._audit_log(
                execution_id,
                'COMPLETED' if container_result.get('success') else 'FAILED',
                f'Duration: {duration_ms}ms'
            )
            
            self.telemetry.emit_runtime_executed(
                self.user_id,
                agent_id,
                duration_ms,
                container_result.get('success', False)
            )
            
            return {
                **container_result,
                'execution_id': execution_id,
                'duration_ms': duration_ms
            }
        
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self._audit_log(execution_id, 'ERROR', str(e))
            self.telemetry.emit_runtime_executed(self.user_id, agent_id, duration_ms, False)
            
            return {
                'success': False,
                'execution_id': execution_id,
                'error': 'EXECUTION_FAILED',
                'message': str(e),
                'duration_ms': duration_ms
            }
    
    def _generate_execution_id(self) -> str:
        """Generate unique execution ID"""
        import uuid
        return f"exec_{uuid.uuid4().hex[:12]}"
    
    def _audit_log(self, execution_id: str, status: str, details: str):
        """Write to audit log"""
        # TODO: Implement actual audit logging to database or log service
        if os.getenv('PH_ENABLE_AUDIT_LOGS') == 'true':
            print(f"[AUDIT] {execution_id} | {status} | {details}")
    
    def _launch_container(
        self,
        manifest: Dict[str, Any],
        inputs: Dict[str, Any],
        cpu_limit: float,
        mem_limit_mb: int,
        timeout_s: int
    ) -> Dict[str, Any]:
        """
        Launch agent container with Pro resources
        This is a placeholder - implement actual container orchestration
        """
        # TODO: Implement actual container launch using Docker/Kubernetes
        # Pro runtime has more resources and capabilities than Lite
        
        return {
            'success': True,
            'outputs': {
                'message': 'Container execution not yet implemented (Pro runtime)'
            },
            'duration_ms': 100
        }
