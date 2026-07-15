# CrashLoopBackOff Runbook

## Meaning

CrashLoopBackOff means a Kubernetes container starts, crashes, and Kubernetes repeatedly tries to restart it with an increasing delay.

## Common Causes

- Application startup error
- Missing environment variable
- Bad configuration
- Missing Secret or ConfigMap
- Application cannot connect to a dependency
- Wrong container command or arguments
- Permission issue
- Port binding issue

## Useful Commands

- kubectl get pods -n <namespace>
- kubectl describe pod <pod-name> -n <namespace>
- kubectl logs <pod-name> -n <namespace>
- kubectl logs <pod-name> -n <namespace> --previous
- kubectl get events -n <namespace> --sort-by=.lastTimestamp

## Safe Next Steps

- Check pod status
- Describe the pod and inspect events
- Check current and previous container logs
- Check recent deployment or config changes
- Verify Secrets and ConfigMaps exist
- Check application startup configuration

## What Not To Do

- Do not delete the namespace
- Do not restart random workloads without understanding the cause
- Do not change production configuration without approval