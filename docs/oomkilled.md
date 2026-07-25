# OOMKilled Runbook

## Meaning

OOMKilled means a Kubernetes container was terminated because it used more memory than its configured memory limit.

This usually means the container exceeded its memory limit and was killed by the Linux Out-Of-Memory killer.

## Common Causes

- Memory limit is too low
- Application memory leak
- Sudden traffic or workload spike
- Batch job using too much memory
- Inefficient application memory usage
- JVM, Python, Node.js, or Go runtime memory not tuned correctly
- Memory request and memory limit are not configured properly
- Node memory pressure

## Useful Commands

- kubectl get pods -n <namespace>
- kubectl describe pod <pod-name> -n <namespace>
- kubectl logs <pod-name> -n <namespace>
- kubectl logs <pod-name> -n <namespace> --previous
- kubectl top pod <pod-name> -n <namespace>
- kubectl top pod -n <namespace> --sort-by=memory
- kubectl get events -n <namespace> --sort-by=.lastTimestamp
- kubectl get pod <pod-name> -n <namespace> -o yaml
- kubectl describe node <node-name>

## What To Check

- Check if pod status or last state shows OOMKilled
- Check if exit code is 137
- Check current and previous container logs
- Check memory usage using kubectl top
- Compare memory usage with configured memory requests and limits
- Check recent traffic or workload spikes
- Check for memory leaks in the application
- Check node memory pressure
- Check whether other pods on the node are consuming too much memory

## Safe Next Steps

- Check pod describe output first
- Check previous logs before the container restarts again
- Review memory requests and limits
- Increase memory limit only after checking actual usage
- Right-size memory request based on observed usage
- Investigate possible memory leaks
- Check if recent deployment changed memory behavior
- Scale workload carefully if traffic increased
- Use monitoring to observe memory growth over time

## What Not To Do

- Do not delete the namespace
- Do not restart random workloads without checking memory evidence
- Do not blindly increase memory limits without understanding usage
- Do not change production resource limits without approval
- Do not ignore repeated OOMKilled events