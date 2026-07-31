# Pending Pod Runbook

## Meaning

A Kubernetes pod in Pending state means the pod has been accepted by the API server, but it has not been scheduled onto a node yet.

This usually means the Kubernetes scheduler cannot find a suitable node for the pod.

## Common Causes

- Insufficient CPU or memory on available nodes
- Pod resource requests are too high
- Node selector does not match any node
- Node affinity or anti-affinity rules cannot be satisfied
- Node has taints that the pod does not tolerate
- PersistentVolumeClaim is not bound
- StorageClass or CSI provisioner issue
- Namespace resource quota exceeded
- Node is NotReady or unschedulable
- Cluster autoscaler is not adding nodes

## Useful Commands

- kubectl get pods -n <namespace>
- kubectl get pods -A --field-selector=status.phase=Pending
- kubectl describe pod <pod-name> -n <namespace>
- kubectl get events -n <namespace> --sort-by=.lastTimestamp
- kubectl describe nodes
- kubectl get nodes --show-labels
- kubectl describe node <node-name>
- kubectl get pvc -n <namespace>
- kubectl describe pvc <pvc-name> -n <namespace>
- kubectl describe resourcequota -n <namespace>

## What To Check

- Check the Events section in kubectl describe pod
- Look for FailedScheduling events
- Check for Insufficient cpu or Insufficient memory messages
- Check if the pod has a nodeSelector
- Check node affinity or anti-affinity rules
- Check node taints and pod tolerations
- Check if a PersistentVolumeClaim is stuck in Pending
- Check namespace resource quota
- Check if nodes are Ready and schedulable
- Check if resource requests are too high

## Safe Next Steps

- Describe the pod and read scheduling events first
- Compare pod resource requests with node allocatable resources
- Reduce resource requests only after validating actual needs
- Add capacity or scale node pool if resources are genuinely exhausted
- Fix node labels if nodeSelector or affinity is wrong
- Add toleration only if scheduling to tainted nodes is intended
- Fix PVC or StorageClass issues before retrying workload
- Check quota usage before increasing workload size

## What Not To Do

- Do not delete the namespace
- Do not randomly remove taints from production nodes
- Do not blindly reduce resource requests without understanding workload needs
- Do not increase quota or node count without approval
- Do not ignore FailedScheduling events